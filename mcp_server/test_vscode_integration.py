#!/usr/bin/env python3
"""
Simple test script to verify VS Code Bridge integration.
Run this to check if the VS Code tools are properly registered.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from tools.vscode_bridge_client import get_vscode_context


async def test_vscode_connection():
    """Test connection to VS Code Bridge."""
    print("Testing VS Code Bridge connection...")
    
    # Check if environment variable is set
    ws_url = os.getenv("VSCODE_UI_BRIDGE_WS")
    if not ws_url:
        print("❌ VSCODE_UI_BRIDGE_WS environment variable not set")
        print("   Set it to something like: ws://127.0.0.1:5310?token=YOUR_TOKEN")
        return False
    
    print(f"✅ Environment variable set: {ws_url}")
    
    try:
        # Try to get VS Code context
        result = await get_vscode_context()
        
        if result.get("ok") is False:
            print(f"❌ Connection failed: {result.get('error', 'Unknown error')}")
            return False
        
        print("✅ Successfully connected to VS Code Bridge!")
        print(f"   Workspace: {result.get('workspace', {}).get('name', 'Unknown')}")
        print(f"   Open tabs: {len(result.get('tabs', []))}")
        print(f"   Active editors: {len(result.get('editors', []))}")
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False


async def main():
    """Main test function."""
    print("VS Code Bridge Integration Test")
    print("=" * 40)
    
    success = await test_vscode_connection()
    
    if success:
        print("\n🎉 VS Code Bridge integration is working!")
        print("   You can now use the following MCP tools:")
        print("   - vscode_get_context")
        print("   - vscode_open_file")
        print("   - vscode_reveal")
        print("   - vscode_apply_edit")
    else:
        print("\n❌ VS Code Bridge integration test failed")
        print("   Make sure:")
        print("   1. VS Code UI Bridge extension is installed and running")
        print("   2. VSCODE_UI_BRIDGE_WS environment variable is set correctly")
        print("   3. The WebSocket server is accessible")


if __name__ == "__main__":
    asyncio.run(main())
