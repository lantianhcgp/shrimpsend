"""
ShrimpSend AI Client - A Python client for AI agents to interact with ShrimpSend.
"""

from .client import ShrimpSendClient
from .auth import AuthManager
from .device import DeviceManager
from .transfer import TransferManager

__version__ = "0.1.0"
__author__ = "Omnibot AI Agent"

__all__ = [
    "ShrimpSendClient",
    "AuthManager", 
    "DeviceManager",
    "TransferManager",
]