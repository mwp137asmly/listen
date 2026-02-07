# Listen 🎤

Voice dictation app for Mac. Press a hotkey, speak, get transcribed text pasted automatically.

## Features

- Menu bar app (stays out of the way)
- Click to record or use menu
- Whisper API transcription
- Auto-paste into any app
- Basic filler word removal (um, uh, etc.)

## Installation

### Option 1: Download Pre-built App (Easiest)

1. Download `Listen.app.zip` from Releases
2. Extract and move `Listen.app` to Applications
3. Right-click → Open (first time only)
4. Configure your OpenAI API key in Settings

### Option 2: Build from Source

See [BUILD.md](BUILD.md) for detailed build instructions.

### Option 3: Run from Python

1. Install dependencies:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. Run:
   ```bash
   source venv/bin/activate
   python3 listen.py
   ```

## Usage

### Recording
1. Click the 🎤 icon in your menu bar
2. Select "Start Recording"
3. Speak clearly
4. Click "Stop Recording" when done
5. Wait a moment for transcription
6. Text is automatically pasted into your active app

### Settings
- Click the menu icon → Settings to update your API key
- Default hotkey: Cmd+Shift+Space (shown in menu)

### Running at Startup

To launch Listen automatically when you log in:

1. Open System Preferences → Users & Groups
2. Click your user → Login Items
3. Click the + button
4. Add this script:

Create `~/Library/LaunchAgents/com.listen.app.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.listen.app</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/listen/venv/bin/python</string>
        <string>/path/to/listen/listen.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>
```

Replace `/path/to/listen` with the actual path.

## Cost

Whisper API pricing: ~$0.006 per minute of audio
- 10 minutes = $0.06
- 1 hour = $0.36
- Way cheaper than Wispr Flow subscription

## Troubleshooting

### "No audio recorded"
- Check microphone permissions in System Preferences → Security & Privacy → Microphone
- Make sure your mic is working (test in Voice Memos)

### "Transcription failed"
- Check your API key in Settings
- Verify you have API credits at platform.openai.com

### Auto-paste not working
- Grant Accessibility permissions: System Preferences → Security & Privacy → Privacy → Accessibility
- Add Terminal (or the Python app) to the allowed apps

## Limitations

Unlike Wispr Flow, Listen does NOT have:
- Per-app tone adjustment
- Auto-learning personal dictionary
- Multi-device sync
- Advanced AI editing

But it gets the job done for way less money.
