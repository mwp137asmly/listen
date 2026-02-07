#!/usr/bin/env python3
"""
Listen - Voice dictation app for Mac
Press configured hotkey to start/stop recording, transcribe with Whisper, auto-paste
"""

import os
import sys
import threading
import tempfile
import wave
import json
from pathlib import Path

import rumps
import sounddevice as sd
import numpy as np
from openai import OpenAI
import pyperclip
import subprocess

# Config
CONFIG_PATH = Path.home() / ".listen" / "config.json"
DEFAULT_HOTKEY = "cmd+shift+space"
SAMPLE_RATE = 16000
CHANNELS = 1

class ListenApp(rumps.App):
    def __init__(self):
        super(ListenApp, self).__init__("🎤", quit_button=None)
        
        # Load config
        self.config = self.load_config()
        self.api_key = self.config.get("openai_api_key", "")
        self.hotkey = self.config.get("hotkey", DEFAULT_HOTKEY)
        
        # State
        self.recording = False
        self.audio_data = []
        self.stream = None
        
        # Setup OpenAI
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
        
        # Menu items
        self.menu = [
            rumps.MenuItem("Status: Ready", callback=None),
            rumps.separator,
            rumps.MenuItem("Start Recording (⌘⇧Space)", callback=self.toggle_recording),
            rumps.separator,
            rumps.MenuItem("Settings", callback=self.show_settings),
            rumps.separator,
            rumps.MenuItem("Quit", callback=rumps.quit_application)
        ]
        
        # Register global hotkey (handled by system, shown in menu)
        self.setup_hotkey_hint()
    
    def load_config(self):
        """Load config from file"""
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH) as f:
                return json.load(f)
        return {}
    
    def save_config(self):
        """Save config to file"""
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_PATH, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def setup_hotkey_hint(self):
        """Display hotkey hint"""
        # Note: Global hotkey registration requires additional setup
        # For now, user triggers via menu or we'd need accessibility permissions
        pass
    
    def toggle_recording(self, _=None):
        """Start or stop recording"""
        if self.recording:
            self.stop_recording()
        else:
            self.start_recording()
    
    def start_recording(self):
        """Start recording audio"""
        if not self.api_key:
            rumps.alert("No API Key", "Please set your OpenAI API key in Settings")
            return
        
        self.recording = True
        self.audio_data = []
        self.title = "🔴"  # Red dot when recording
        self.menu["Status: Ready"].title = "Status: Recording..."
        self.menu["Start Recording (⌘⇧Space)"].title = "Stop Recording (⌘⇧Space)"
        
        # Start audio stream
        def audio_callback(indata, frames, time, status):
            if status:
                print(f"Audio status: {status}", file=sys.stderr)
            self.audio_data.append(indata.copy())
        
        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            callback=audio_callback,
            dtype=np.int16
        )
        self.stream.start()
        
        # Show notification
        self.notify("Recording started", "Speak now. Click menu or press hotkey to stop.")
    
    def stop_recording(self):
        """Stop recording and transcribe"""
        if not self.recording:
            return
        
        self.recording = False
        self.title = "🎤"
        self.menu["Status: Ready"].title = "Status: Transcribing..."
        self.menu["Start Recording (⌘⇧Space)"].title = "Start Recording (⌘⇧Space)"
        
        # Stop stream
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        
        # Process in background
        threading.Thread(target=self.process_audio, daemon=True).start()
    
    def process_audio(self):
        """Transcribe and paste"""
        try:
            # Combine audio data
            if not self.audio_data:
                rumps.notification("Listen", "No audio recorded", "Please try again")
                self.reset_status()
                return
            
            audio = np.concatenate(self.audio_data, axis=0)
            
            # Save to temp WAV file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp_path = tmp.name
            
            with wave.open(tmp_path, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(SAMPLE_RATE)
                wf.writeframes(audio.tobytes())
            
            # Transcribe with Whisper
            with open(tmp_path, 'rb') as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            
            # Clean up temp file
            os.unlink(tmp_path)
            
            # Clean up transcript (remove common filler words)
            text = self.cleanup_text(transcript)
            
            if text.strip():
                # Copy to clipboard
                pyperclip.copy(text)
                
                # Auto-paste
                self.paste_text()
                
                self.notify("Transcription complete", f"Pasted: {text[:50]}{'...' if len(text) > 50 else ''}")
            else:
                self.notify("No speech detected", "Please try again")
            
        except Exception as e:
            self.notify("Error", f"Transcription failed: {str(e)}")
            print(f"Error: {e}", file=sys.stderr)
        finally:
            self.reset_status()
    
    def cleanup_text(self, text):
        """Remove filler words and clean up text"""
        # Basic cleanup - remove common filler words
        fillers = ["um", "uh", "umm", "uhh", "like", "you know"]
        words = text.split()
        cleaned = []
        
        for word in words:
            if word.lower().strip(".,!?") not in fillers:
                cleaned.append(word)
        
        return " ".join(cleaned)
    
    def paste_text(self):
        """Simulate Cmd+V to paste"""
        # Use AppleScript for reliable paste
        script = 'tell application "System Events" to keystroke "v" using command down'
        subprocess.run(["osascript", "-e", script], check=True)
    
    def reset_status(self):
        """Reset UI to ready state"""
        self.title = "🎤"
        self.menu["Status: Ready"].title = "Status: Ready"
    
    def notify(self, title, message):
        """Show macOS notification"""
        rumps.notification("Listen", title, message)
    
    def show_settings(self, _):
        """Show settings dialog"""
        window = rumps.Window(
            message="Enter your OpenAI API key:",
            title="Listen Settings",
            default_text=self.api_key,
            ok="Save",
            cancel="Cancel",
            dimensions=(320, 24)
        )
        response = window.run()
        
        if response.clicked:
            new_key = response.text.strip()
            if new_key:
                self.api_key = new_key
                self.config["openai_api_key"] = new_key
                self.client = OpenAI(api_key=new_key)
                self.save_config()
                rumps.alert("Settings saved", "API key updated successfully")

if __name__ == "__main__":
    ListenApp().run()
