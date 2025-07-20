"""
Modular MCP Server Package

This package provides a scalable, plugin-ready MCP (Model Context Protocol) server
with human-in-the-loop collaboration capabilities.

Architecture:
- Action registry for modular command execution
- Async/await support with aiohttp
- Comprehensive logging and debugging
- Human-in-the-loop approval workflow
"""

__version__ = "1.0.0"
__author__ = "MCP Server Team"

# Import core components for easy access
from .core.server import MCPServer
from .core.action_registry import ActionRegistry
from .core.human_loop import HumanLoopManager

__all__ = ["MCPServer", "ActionRegistry", "HumanLoopManager"]
