#!/usr/bin/env python3
"""
Basic usage example for ShrimpSend AI Client
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shrimpsend_ai import ShrimpSendClient


def main():
    """Example usage of ShrimpSend AI Client."""
    
    # Example 1: Login and register device
    print("Example 1: Login and register device")
    print("-" * 40)
    
    client = ShrimpSendClient(
        server="https://xiachuan.net",
        config_dir="/tmp/shrimpsend_example"
    )
    
    # Login (replace with your credentials)
    # client.login("your@email.com", "yourpassword")
    
    # Register as device
    # device = client.register_device(
    #     name="Example AI Agent",
    #     device_type="AI_AGENT"
    # )
    # print(f"Device registered: {device.get('deviceId')}")
    
    print()
    
    # Example 2: List devices
    print("Example 2: List devices")
    print("-" * 40)
    
    # devices = client.list_devices()
    # for device in devices:
    #     print(f"- {device.get('name')} ({device.get('deviceId')})")
    
    print()
    
    # Example 3: Send text
    print("Example 3: Send text")
    print("-" * 40)
    
    # result = client.send_text(
    #     target_device="My Phone",
    #     text="Hello from AI agent!"
    # )
    # print(f"Text sent: {result.get('transferId')}")
    
    print()
    
    # Example 4: Send file
    print("Example 4: Send file")
    print("-" * 40)
    
    # Create a sample file
    sample_file = "/tmp/sample.txt"
    with open(sample_file, "w") as f:
        f.write("This is a sample file from AI agent.\n")
        f.write("Created at: 2026-07-07\n")
    
    # result = client.send_file(
    #     target_device="My Laptop",
    #     file_path=sample_file
    # )
    # print(f"File sent: {result.get('transferId')}")
    
    print()
    
    # Example 5: Send clipboard
    print("Example 5: Send clipboard")
    print("-" * 40)
    
    # result = client.send_clipboard(
    #     target_device="My Phone",
    #     content="Text copied from AI workspace",
    #     content_type="text/plain"
    # )
    # print(f"Clipboard sent: {result.get('transferId')}")
    
    print()
    print("Examples completed!")
    print("Note: Uncomment the code above and provide credentials to test.")


if __name__ == "__main__":
    main()