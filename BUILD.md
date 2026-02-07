# Building Listen.app

## Prerequisites
- Python 3.8+
- pip

## Build Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Build the app:
   ```bash
   python setup.py py2app
   ```

3. The app will be created in `dist/Listen.app`

4. Move it to Applications:
   ```bash
   mv dist/Listen.app /Applications/
   ```

## First Run

1. Launch Listen from Applications
2. Grant Microphone permission when prompted
3. Grant Accessibility permission:
   - System Preferences → Security & Privacy → Privacy → Accessibility
   - Click the lock to make changes
   - Click + and add Listen.app
4. Configure your OpenAI API key:
   - Click the 🎤 menu bar icon
   - Click Settings
   - Paste your API key

## Troubleshooting

**App won't open:**
- Right-click → Open (first time only, to bypass Gatekeeper)
- Or: System Preferences → Security & Privacy → General → "Open Anyway"

**No audio recording:**
- Check System Preferences → Security & Privacy → Privacy → Microphone
- Make sure Listen is checked

**Auto-paste not working:**
- Check System Preferences → Security & Privacy → Privacy → Accessibility
- Make sure Listen is checked
