#!/usr/bin/env python3
"""
ShrimpSend Integration Example
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, '/workspace/projects/shrimpsend/ai-client')

from shrimpsend_ai import ShrimpSendClient


def main():
    """Example usage of ShrimpSend Integration."""
    
    print("ShrimpSend Integration Example")
    print("=" * 40)
    
    # Configuration
    server = "https://api.xiachuan.net"
    email = "your@email.com"  # Replace with your email
    password = "yourpassword"  # Replace with your password
    device_name = "Xiaomi Mi 10 Pro"  # Replace with your device name
    
    # Create client
    client = ShrimpSendClient(
        server=server,
        config_dir=os.path.expanduser("~/.shrimpsend-ai")
    )
    
    # Login
    print("\n1. Login to ShrimpSend")
    if client.login(email, password, device_id="ai-example-001"):
        print("✓ Login successful!")
    else:
        print("✗ Login failed!")
        return
    
    # Register device
    print("\n2. Register AI device")
    try:
        device = client.register_device(
            name="Omnibot AI Agent",
            device_type="AI_AGENT"
        )
        print(f"✓ Device registered: {device.get('deviceId')}")
    except Exception as e:
        print(f"✗ Device registration failed: {e}")
    
    # List devices
    print("\n3. List devices")
    try:
        devices = client.list_devices()
        print("Available devices:")
        for dev in devices:
            print(f"  - {dev.get('name')} ({dev.get('deviceId')})")
    except Exception as e:
        print(f"✗ Failed to list devices: {e}")
    
    # Send text
    print("\n4. Send text message")
    try:
        result = client.send_text(
            target_device=device_name,
            text="Hello from ShrimpSend Integration Example!"
        )
        print("✓ Text sent successfully!")
    except Exception as e:
        print(f"✗ Failed to send text: {e}")
    
    # Send clipboard
    print("\n5. Send clipboard content")
    try:
        result = client.send_clipboard(
            target_device=device_name,
            content="Clipboard content from example",
            content_type="text/plain"
        )
        print("✓ Clipboard sent successfully!")
    except Exception as e:
        print(f"✗ Failed to send clipboard: {e}")
    
    print("\n" + "=" * 40)
    print("Example completed!")


if __name__ == "__main__":
    main()