# ShrimpSend Integration Skill

## Description

This skill allows AI agents to send files and text to physical devices using ShrimpSend. It transforms the AI agent into a virtual device that can communicate with other devices in the ShrimpSend ecosystem.

## When to Use

- When you need to send files or text from the AI agent to a physical device
- When the user asks to "send to my phone", "send to my laptop", "transfer file to device"
- When you need to share content between the AI workspace and physical devices

## Capabilities

- **Device Registration**: Register AI agent as a virtual device in ShrimpSend
- **Text Sending**: Send text content to target devices
- **File Sending**: Send files to target devices
- **Clipboard Sending**: Send clipboard content to target devices

## Setup

### Prerequisites

1. A ShrimpSend account (https://xiachuan.net or https://shrimpsend.com)
2. Python 3.8+
3. `requests` library

### Installation

1. Copy the `shrimpsend_ai` directory to your workspace
2. Install dependencies:
   ```bash
   pip install requests
   ```

### Configuration

1. Login to ShrimpSend:
   ```bash
   python -m shrimpsend_ai.cli login --server https://xiachuan.net --email your@email.com --password yourpassword
   ```

2. Register as device:
   ```bash
   python -m shrimpsend_ai.cli register --name "Omnibot AI Agent"
   ```

## Usage

### Command Line

```bash
# List devices
python -m shrimpsend_ai.cli list-devices

# Send text
python -m shrimpsend_ai.cli send-text --device "My Phone" --text "Hello from AI!"

# Send file
python -m shrimpsend_ai.cli send-file --device "My Laptop" --file /path/to/document.pdf

# Send clipboard
python -m shrimpsend_ai.cli send-clipboard --device "My Phone" --content "Copied text"
```

### Python API

```python
from shrimpsend_ai import ShrimpSendClient

# Create client
client = ShrimpSendClient.from_config()

# Send text
client.send_text(
    target_device="My Phone",
    text="Hello from AI!"
)

# Send file
client.send_file(
    target_device="My Laptop",
    file_path="/path/to/document.pdf"
)

# Send clipboard
client.send_clipboard(
    target_device="My Phone",
    content="Copied text",
    content_type="text/plain"
)
```

## Integration with Omnibot

### Using in Terminal

```bash
# From Omnibot terminal
cd /workspace/projects/shrimpsend/ai-client
python -m shrimpsend_ai.cli send-text --device "My Phone" --text "Message from Omnibot"
```

### Using in Python Scripts

```python
# In Omnibot Python script
import sys
sys.path.insert(0, '/workspace/projects/shrimpsend/ai-client')

from shrimpsend_ai import ShrimpSendClient

client = ShrimpSendClient.from_config()
client.send_text(target_device="My Phone", text="Hello from Omnibot!")
```

## Architecture

The skill consists of:

1. **Python Client Library** (`shrimpsend_ai/`)
   - `client.py` - Main client class
   - `auth.py` - Authentication manager
   - `device.py` - Device management
   - `transfer.py` - File transfer logic
   - `cli.py` - Command line interface

2. **Transfer Protocol**
   - HTTP direct push for LAN transfers
   - S3 relay for remote transfers
   - Support for resume on large files

## Security

- JWT tokens stored securely in `~/.shrimpsend-ai/`
- No credentials in logs or output
- HTTPS for all API calls
- File integrity verification using SHA-256

## Troubleshooting

### Common Issues

1. **"Not logged in"**
   - Run: `python -m shrimpsend_ai.cli login --server ... --email ... --password ...`

2. **"Device not found"**
   - Run: `python -m shrimpsend_ai.cli list-devices` to see available devices
   - Make sure the target device is online

3. **"Transfer failed"**
   - Check network connectivity
   - Verify target device is reachable
   - Try sending a smaller file first

## Future Enhancements

1. **Bidirectional Communication**: Receive messages from devices
2. **WebRTC Support**: Direct peer-to-peer transfer
3. **Scheduled Transfers**: Queue files for later delivery
4. **Content Generation**: AI-generated content transfer

## License

This skill is part of the ShrimpSend project and follows the same AGPL-3.0-or-later license.