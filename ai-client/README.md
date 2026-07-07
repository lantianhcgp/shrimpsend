# ShrimpSend AI Device Integration

## Overview

This project enables AI agents (like Omnibot) to act as virtual devices in the ShrimpSend ecosystem. AI agents can send files, text, and other content to physical devices registered in ShrimpSend.

## Features

- **Device Registration**: Register AI agent as a virtual device
- **Text Sending**: Send text content to target devices
- **File Sending**: Send files to target devices
- **Clipboard Sending**: Send clipboard content to target devices
- **Multi-path Transfer**: Supports HTTP direct push and S3 relay

## Quick Start

### 1. Install Dependencies

```bash
pip install requests
```

### 2. Login to ShrimpSend

```bash
python -m shrimpsend_ai.cli login \
  --server https://xiachuan.net \
  --email your@email.com \
  --password yourpassword
```

### 3. Register as Device

```bash
python -m shrimpsend_ai.cli register \
  --name "Omnibot AI Agent" \
  --type AI_AGENT
```

### 4. Send Content

```bash
# Send text
python -m shrimpsend_ai.cli send-text \
  --device "My Phone" \
  --text "Hello from AI!"

# Send file
python -m shrimpsend_ai.cli send-file \
  --device "My Laptop" \
  --file /path/to/document.pdf

# Send clipboard
python -m shrimpsend_ai.cli send-clipboard \
  --device "My Phone" \
  --content "Text copied from AI"
```

## Python API

```python
from shrimpsend_ai import ShrimpSendClient

# Create client
client = ShrimpSendClient.from_config()

# Send text
client.send_text(
    target_device="My Phone",
    text="Hello from AI agent!"
)

# Send file
client.send_file(
    target_device="My Laptop",
    file_path="/path/to/document.pdf"
)

# Send clipboard
client.send_clipboard(
    target_device="My Phone",
    content="Text copied from AI",
    content_type="text/plain"
)
```

## Integration with Omnibot

### Method 1: Command Line

```bash
# From Omnibot terminal
cd /workspace/projects/shrimpsend/ai-client
python -m shrimpsend_ai.cli send-text \
  --device "My Phone" \
  --text "Message from Omnibot"
```

### Method 2: Python Script

```python
# In Omnibot Python script
import sys
sys.path.insert(0, '/workspace/projects/shrimpsend/ai-client')

from shrimpsend_ai import ShrimpSendClient

client = ShrimpSendClient.from_config()
client.send_text(
    target_device="My Phone",
    text="Hello from Omnibot!"
)
```

### Method 3: Omnibot Skill

Copy the `omnibot-skill` directory to your Omnibot skills directory:

```bash
cp -r omnibot-skill /workspace/.omnibot/skills/shrimpsend-integration
```

## Architecture

```
ai-client/
├── shrimpsend_ai/          # Python client library
│   ├── __init__.py
│   ├── client.py           # Main client class
│   ├── auth.py             # Authentication manager
│   ├── device.py           # Device management
│   ├── transfer.py         # File transfer logic
│   └── cli.py              # Command line interface
├── omnibot-skill/          # Omnibot skill
│   └── SKILL.md
├── examples/               # Example scripts
│   └── basic_usage.py
└── README.md
```

## Transfer Protocol

The AI client supports multiple transfer paths:

1. **HTTP Direct Push**: For devices on the same network
2. **S3 Relay**: For devices on different networks
3. **Resume Support**: Large files can resume from interruption

## Security

- JWT tokens stored securely in `~/.shrimpsend-ai/`
- No credentials in logs or output
- HTTPS for all API calls
- File integrity verification using SHA-256

## Configuration

Configuration is stored in:
- `~/.shrimpsend-ai/config.json` (client configuration)
- `~/.shrimpsend-ai/auth.json` (authentication tokens)

## Troubleshooting

### Common Issues

1. **"Not logged in"**
   - Run: `python -m shrimpsend_ai.cli login ...`

2. **"Device not found"**
   - Run: `python -m shrimpsend_ai.cli list-devices`
   - Make sure target device is online

3. **"Transfer failed"**
   - Check network connectivity
   - Verify target device is reachable
   - Try sending smaller file first

## Development

### Adding New Features

1. Add new methods to `client.py`
2. Implement underlying logic in respective managers
3. Add CLI commands if needed
4. Update documentation

### Testing

```bash
# Run example
python examples/basic_usage.py

# Test CLI
python -m shrimpsend_ai.cli --help
```

## License

This project is part of ShrimpSend and follows the same AGPL-3.0-or-later license.

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## Support

- ShrimpSend Documentation: https://github.com/shrimpsend/shrimpsend
- Issues: https://github.com/shrimpsend/shrimpsend/issues