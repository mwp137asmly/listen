"""
py2app setup script for Listen
"""
from setuptools import setup

APP = ['listen.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'iconfile': None,
    'plist': {
        'CFBundleName': 'Listen',
        'CFBundleDisplayName': 'Listen',
        'CFBundleIdentifier': 'com.listen.voicedictation',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSUIElement': True,  # Hide from Dock (menu bar only)
        'NSMicrophoneUsageDescription': 'Listen needs microphone access to record your voice for transcription.',
        'NSAppleEventsUsageDescription': 'Listen needs permission to paste transcribed text into other applications.',
    },
    'packages': ['rumps', 'sounddevice', 'numpy', 'openai', 'pyperclip'],
    'includes': ['subprocess', 'threading', 'tempfile', 'wave', 'json', 'pathlib'],
}

setup(
    name='Listen',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
