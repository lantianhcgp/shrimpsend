#!/bin/bash

# ShrimpSend CLI Wrapper Script
# Usage: sh shrimpsend_cli.sh <command> [options]

set -e

# Configuration
SHRIMPSEND_DIR="/workspace/projects/shrimpsend/ai-client"
CONFIG_DIR="$HOME/.shrimpsend-ai"
SERVER="https://api.xiachuan.net"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python client is available
check_client() {
    if [ ! -d "$SHRIMPSEND_DIR" ]; then
        print_error "ShrimpSend client not found at $SHRIMPSEND_DIR"
        exit 1
    fi
}

# Login command
login() {
    local email=$1
    local password=$2
    local device_id=${3:-"ai-cli-001"}
    
    if [ -z "$email" ] || [ -z "$password" ]; then
        print_error "Usage: $0 login <email> <password> [device_id]"
        exit 1
    fi
    
    check_client
    cd "$SHRIMPSEND_DIR"
    python -m shrimpsend_ai.cli login --server "$SERVER" --email "$email" --password "$password" --device-id "$device_id"
}

# Register device
register() {
    local name=${1:-"Omnibot AI Agent"}
    local type=${2:-"AI_AGENT"}
    
    check_client
    cd "$SHRIMPSEND_DIR"
    python -m shrimpsend_ai.cli register --name "$name" --type "$type"
}

# List devices
list_devices() {
    check_client
    cd "$SHRIMPSEND_DIR"
    python -m shrimpsend_ai.cli list-devices
}

# Send text
send_text() {
    local device=$1
    local text=$2
    
    if [ -z "$device" ] || [ -z "$text" ]; then
        print_error "Usage: $0 send-text <device> <text>"
        exit 1
    fi
    
    check_client
    cd "$SHRIMPSEND_DIR"
    python -m shrimpsend_ai.cli send-text --device "$device" --text "$text"
}

# Send clipboard
send_clipboard() {
    local device=$1
    local content=$2
    local type=${3:-"text/plain"}
    
    if [ -z "$device" ] || [ -z "$content" ]; then
        print_error "Usage: $0 send-clipboard <device> <content> [type]"
        exit 1
    fi
    
    check_client
    cd "$SHRIMPSEND_DIR"
    python -m shrimpsend_ai.cli send-clipboard --device "$device" --content "$content" --type "$type"
}

# Logout
logout() {
    check_client
    cd "$SHRIMPSEND_DIR"
    python -m shrimpsend_ai.cli logout
}

# Show help
show_help() {
    echo "ShrimpSend CLI Wrapper"
    echo ""
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  login <email> <password> [device_id]  - Login to ShrimpSend"
    echo "  register [name] [type]                - Register AI device"
    echo "  list-devices                          - List all devices"
    echo "  send-text <device> <text>             - Send text message"
    echo "  send-clipboard <device> <content> [type] - Send clipboard content"
    echo "  logout                                - Logout"
    echo "  help                                  - Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 login user@example.com password123"
    echo "  $0 send-text \"Xiaomi Mi 10 Pro\" \"Hello from AI!\""
    echo "  $0 send-clipboard \"Xiaomi Mi 10 Pro\" \"Clipboard content\""
}

# Main command handler
case "$1" in
    login)
        login "$2" "$3" "$4"
        ;;
    register)
        register "$2" "$3"
        ;;
    list-devices)
        list_devices
        ;;
    send-text)
        send_text "$2" "$3"
        ;;
    send-clipboard)
        send_clipboard "$2" "$3" "$4"
        ;;
    logout)
        logout
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac