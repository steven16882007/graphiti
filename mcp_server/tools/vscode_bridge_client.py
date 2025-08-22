# -*- coding: utf-8 -*-
"""
Thin WebSocket client for the VSCode UI Bridge (ws://HOST:5310?token=...).

Set env VSCODE_UI_BRIDGE_WS to something like:
  - ws://127.0.0.1:5310?token=XXXX
  - ws://host.docker.internal:5310?token=XXXX   # when this runs inside Docker
"""
from __future__ import annotations

import asyncio
import json
import os
from typing import Any, Dict

import websockets  # pip install websockets


def _ws_url() -> str:
    url = os.getenv("VSCODE_UI_BRIDGE_WS")
    if not url:
        raise RuntimeError(
            "VSCODE_UI_BRIDGE_WS is not set. "
            "Example: ws://127.0.0.1:5310?token=YOUR_TOKEN"
        )
    return url


async def _rpc(msg: Dict[str, Any], timeout: float = 8.0) -> Dict[str, Any]:
    """Send one message and await a single JSON response."""
    url = _ws_url()
    try:
        async with websockets.connect(
            url,
            ping_interval=30,
            ping_timeout=20,
            close_timeout=1,
            max_size=8 * 1024 * 1024,
        ) as ws:
            await ws.send(json.dumps(msg))
            raw = await asyncio.wait_for(ws.recv(), timeout=timeout)
            try:
                data = json.loads(raw)
            except Exception:
                return {"ok": False, "error": "Non-JSON response", "raw": raw[:2000]}
            return data if isinstance(data, dict) else {"ok": False, "error": "Invalid response type"}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}


# ---------- Public async APIs (used by MCP tools) ----------

async def get_vscode_context() -> Dict[str, Any]:
    """Get a snapshot: workspace, tabs, visible editors, selections, diagnostics, git, etc."""
    return await _rpc({"type": "getSnapshot"})

async def open_file(path: str) -> Dict[str, Any]:
    """Open a file in VS Code by absolute path."""
    return await _rpc({"type": "openFile", "path": path})

async def reveal(path: str, line: int, character: int = 0) -> Dict[str, Any]:
    """Reveal a specific position in VS Code."""
    return await _rpc(
        {"type": "reveal", "path": path, "line": int(line), "character": int(character)}
    )

async def apply_edit(
    path: str,
    start_line: int,
    start_char: int,
    end_line: int,
    end_char: int,
    text: str,
) -> Dict[str, Any]:
    """Replace the given range [start, end) with text in VS Code."""
    return await _rpc(
        {
            "type": "applyEdit",
            "path": path,
            "start": {"line": int(start_line), "character": int(start_char)},
            "end": {"line": int(end_line), "character": int(end_char)},
            "text": text,
        }
    )
