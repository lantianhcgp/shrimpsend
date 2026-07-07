# ShrimpSend AI Device Integration Design

## Overview

This document describes the design for integrating AI agents (like Omnibot) as virtual devices in the ShrimpSend ecosystem. The goal is to allow AI agents to send files, text, and other content to physical devices registered in ShrimpSend.

## Objectives

1. **Device Registration**: AI agents can register as virtual devices in ShrimpSend
2. **Content Sending**: AI agents can send text, files, and other content to target devices
3. **Message Handling**: AI agents can receive messages from other devices (optional)
4. **Authentication**: Secure authentication using existing ShrimpSend auth system

## Architecture

### Components

1. **Python Client Library** (`shrimpsend-ai-client`)
   - Core library for interacting with ShrimpSend API
   - Handles authentication, device management, and file transfer
   - Supports multiple transfer paths (HTTP direct, relay, etc.)

2. **CLI Tool** (`shrimpsend-ai`)
   - Command-line interface for AI agents
   - Simple commands for sending files/text to devices
   - Integration with Omnibot workspace

3. **Omnibot Skill** (`shrimpsend-integration`)
   - Omnibot skill for native integration
   - Allows AI agents to use ShrimpSend as a device

### API Endpoints Used

Based on the existing ShrimpSend API:

1. **Authentication**:
   - `POST /api/auth/register` - Register new user
   - `POST /api/auth/login` - Login and get JWT token

2. **Device Management**:
   - `POST /api/devices` - Register AI agent as a device
   - `GET /api/devices` - List devices
   - `PATCH /api/devices/{deviceId}` - Update device info
   - `POST /api/devices/{deviceId}/presence` - Update device presence

3. **File Transfer**:
   - Based on the multi-path protocol (HTTP direct, reverse pull, WebRTC, S3 relay)
   - AI agent will implement HTTP direct push and S3 relay paths

## Implementation Plan

### Phase 1: Core Client Library

1. Create Python package structure
2. Implement authentication module
3. Implement device management
4. Implement basic file transfer (HTTP direct)

### Phase 2: CLI Tool

1. Create command-line interface
2. Implement send command (text and files)
3. Implement device listing
4. Add configuration management

### Phase 3: Omnibot Integration

1. Create Omnibot skill
2. Implement skill commands
3. Add to Omnibot workspace

## Technical Details

### Device Registration

AI agent will register with:
- Device type: "AI_AGENT"
- Device name: "Omnibot AI Agent"
- Platform: "Linux/Alpine"
- Capabilities: ["text", "file_transfer"]

### Authentication Flow

1. User provides ShrimpSend credentials or JWT token
2. AI agent authenticates and stores token
3. Token used for subsequent API calls

### File Transfer Protocol

For simplicity, initial implementation will use:
1. HTTP direct push when possible
2. S3 relay as fallback
3. Support for resume on large files

### Security Considerations

1. JWT token stored securely in workspace
2. No credentials in logs or output
3. HTTPS for all API calls
4. File integrity verification using SHA-256

## Usage Examples

### Command Line

```bash
# Register AI agent
shrimpsend-ai register --server https://xiachuan.net --user user@example.com --password pass

# Send text to device
shrimpsend-ai send-text --device "My Phone" --text "Hello from AI!"

# Send file to device
shrimpsend-ai send-file --device "My Laptop" --file /path/to/document.pdf

# List devices
shrimpsend-ai list-devices
```

### Python API

```python
from shrimpsend_ai import ShrimpSendClient

client = ShrimpSendClient(
    server="https://xiachuan.net",
    token="jwt_token_here"
)

# Register as device
device = client.register_device(
    name="Omnibot AI Agent",
    type="AI_AGENT"
)

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
```

## Future Enhancements

1. **Bidirectional Communication**: Receive messages from devices
2. **WebRTC Support**: Direct peer-to-peer transfer
3. **Multi-user Support**: Multiple AI agents per user
4. **Scheduled Transfers**: Queue files for later delivery
5. **Content Generation**: AI-generated content transfer

## Testing Strategy

1. Unit tests for client library
2. Integration tests with local ShrimpSend instance
3. End-to-end tests with Docker setup
4. Manual testing with real devices

## Dependencies

- Python 3.8+
- requests (HTTP client)
- websockets (for Centrifugo)
- hashlib (for file integrity)
- pathlib (for file handling)

## Configuration

Configuration stored in:
- `~/.shrimpsend-ai/config.json` (user config)
- `/workspace/.omnibot/config/shrimpsend.json` (Omnibot config)

## Error Handling

1. Network errors: Retry with exponential backoff
2. Authentication errors: Re-login or refresh token
3. Transfer errors: Resume from last position
4. Device errors: Re-register if device not found