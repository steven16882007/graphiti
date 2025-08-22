# -*- coding: utf-8 -*-
"""
MCP tool registrations that bridge to the VSCode UI Bridge.
Usage (in your server bootstrap):
    from tools.vscode_tools import register_vscode_tools
    register_vscode_tools(mcp)  # where mcp is your FastMCP instance

Requires:
  - pip install websockets
  - env VSCODE_UI_BRIDGE_WS=ws://127.0.0.1:5310?token=YOUR_TOKEN
"""
from __future__ import annotations

from typing import Any, Dict
from mcp.server.fastmcp import FastMCP
from .vscode_bridge_client import (
    get_vscode_context as _get_ctx,
    open_file as _open_file,
    reveal as _reveal,
    apply_edit as _apply_edit,
)


def register_vscode_tools(mcp: FastMCP) -> None:
    """Attach VSCode UI Bridge tools to a FastMCP instance."""

    @mcp.tool()
    async def vscode_get_context() -> Dict[str, Any]:
        """
        Return the current VS Code context snapshot:
        { workspace, tabs[], editors[], diagnostics[], git, active, ... }
        
        This provides a complete view of the current VS Code state including:
        - Open workspace and folders
        - All open tabs and their states
        - Currently visible editors and their content
        - Cursor positions and selections
        - Diagnostics (errors, warnings)
        - Git status information
        - Active file and editor focus
        """
        return await _get_ctx()

    @mcp.tool()
    async def vscode_open_file(path: str) -> Dict[str, Any]:
        """
        Open a file in VS Code by absolute path.
        
        Args:
            path: Absolute file path to open in VS Code
            
        Returns:
            Response from VS Code indicating success/failure
        """
        return await _open_file(path)

    @mcp.tool()
    async def vscode_reveal(path: str, line: int, character: int = 0) -> Dict[str, Any]:
        """
        Center the editor on a specific position in a file.
        
        Args:
            path: Absolute file path
            line: Line number (1-based)
            character: Character position in the line (0-based, default: 0)
            
        Returns:
            Response from VS Code indicating success/failure
        """
        return await _reveal(path, line, character)

    @mcp.tool()
    async def vscode_apply_edit(
        path: str,
        start_line: int,
        start_char: int,
        end_line: int,
        end_char: int,
        text: str,
    ) -> Dict[str, Any]:
        """
        Replace a range of text in a VS Code file.
        
        Args:
            path: Absolute file path
            start_line: Starting line number (0-based)
            start_char: Starting character position (0-based)
            end_line: Ending line number (0-based)
            end_char: Ending character position (0-based)
            text: New text to replace the range with
            
        Returns:
            Response from VS Code indicating success/failure
        """
        return await _apply_edit(path, start_line, start_char, end_line, end_char, text)
