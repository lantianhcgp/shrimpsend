#!/usr/bin/env python3
"""
ShrimpSend AI Client - Command Line Interface
"""

import argparse
import sys
import json
from typing import List, Optional

from .client import ShrimpSendClient


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for CLI.
    
    Args:
        args: Command line arguments
        
    Returns:
        Exit code
    """
    parser = argparse.ArgumentParser(
        description="ShrimpSend AI Client - Send files and text from AI agents"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Login command
    login_parser = subparsers.add_parser('login', help='Login to ShrimpSend')
    login_parser.add_argument('--server', required=True, help='Server URL')
    login_parser.add_argument('--email', required=True, help='Email address')
    login_parser.add_argument('--password', required=True, help='Password')
    
    # Register device command
    register_parser = subparsers.add_parser('register', help='Register as device')
    register_parser.add_argument('--name', default='Omnibot AI Agent', help='Device name')
    register_parser.add_argument('--type', default='AI_AGENT', help='Device type')
    
    # List devices command
    subparsers.add_parser('list-devices', help='List all devices')
    
    # Send text command
    send_text_parser = subparsers.add_parser('send-text', help='Send text to device')
    send_text_parser.add_argument('--device', required=True, help='Target device name')
    send_text_parser.add_argument('--text', required=True, help='Text to send')
    send_text_parser.add_argument('--thread', help='Thread ID')
    
    # Send file command
    send_file_parser = subparsers.add_parser('send-file', help='Send file to device')
    send_file_parser.add_argument('--device', required=True, help='Target device name')
    send_file_parser.add_argument('--file', required=True, help='File path')
    send_file_parser.add_argument('--thread', help='Thread ID')
    
    # Send clipboard command
    send_clip_parser = subparsers.add_parser('send-clipboard', help='Send clipboard content')
    send_clip_parser.add_argument('--device', required=True, help='Target device name')
    send_clip_parser.add_argument('--content', required=True, help='Clipboard content')
    send_clip_parser.add_argument('--type', default='text/plain', help='Content type')
    
    # Logout command
    subparsers.add_parser('logout', help='Logout')
    
    args = parser.parse_args(args)
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        client = ShrimpSendClient.from_config()
    except FileNotFoundError:
        print("Error: Not logged in. Use 'login' command first.", file=sys.stderr)
        return 1
    
    if args.command == 'login':
        client = ShrimpSendClient(
            server=args.server,
            config_dir=str(client.config_dir)
        )
        
        if client.login(args.email, args.password):
            print("Login successful!")
            return 0
        else:
            print("Login failed!", file=sys.stderr)
            return 1
    
    elif args.command == 'register':
        device = client.register_device(
            name=args.name,
            device_type=args.type
        )
        print(f"Device registered: {device.get('deviceId')}")
        return 0
    
    elif args.command == 'list-devices':
        devices = client.list_devices()
        for device in devices:
            print(f"- {device.get('name')} ({device.get('deviceId')}): {device.get('type')}")
        return 0
    
    elif args.command == 'send-text':
        result = client.send_text(
            target_device=args.device,
            text=args.text,
            thread_id=args.thread
        )
        print(f"Text sent: {result.get('transferId')}")
        return 0
    
    elif args.command == 'send-file':
        result = client.send_file(
            target_device=args.device,
            file_path=args.file,
            thread_id=args.thread
        )
        print(f"File sent: {result.get('transferId')}")
        return 0
    
    elif args.command == 'send-clipboard':
        result = client.send_clipboard(
            target_device=args.device,
            content=args.content,
            content_type=args.type
        )
        print(f"Clipboard sent: {result.get('transferId')}")
        return 0
    
    elif args.command == 'logout':
        client.auth.logout()
        print("Logged out!")
        return 0
    
    return 0


if __name__ == '__main__':
    sys.exit(main())