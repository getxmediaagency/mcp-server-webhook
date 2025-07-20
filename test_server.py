"""
Simple test script to verify the MCP server functionality.
"""

import asyncio
import aiohttp
import json
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from mcp_server.core.server import MCPServer
from mcp_server.actions.client_data import get_client_data


async def test_server():
    """Test the MCP server functionality."""
    print("🧪 Testing Modular MCP Server...")
    
    # Create server instance
    server = MCPServer(host="localhost", port=8001, debug=True)
    
    # Register test action
    server.register_action("get_client_data", get_client_data)
    
    # Start server in background
    server_task = asyncio.create_task(server.start())
    
    # Wait a moment for server to start
    await asyncio.sleep(1)
    
    try:
        # Test health endpoint
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8001/health") as response:
                health_data = await response.json()
                print(f"✅ Health check: {health_data}")
            
            # Test action execution
            test_params = {"client_id": "test-client-123", "include_metrics": True}
            async with session.post(
                "http://localhost:8001/api/action/get_client_data",
                json={"params": test_params}
            ) as response:
                action_data = await response.json()
                print(f"✅ Action execution: {json.dumps(action_data, indent=2)}")
            
            # Test actions list
            async with session.get("http://localhost:8001/api/actions") as response:
                actions_data = await response.json()
                print(f"✅ Actions list: {actions_data}")
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
    finally:
        # Cancel server task
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            pass
    
    print("🎉 Test completed!")


if __name__ == "__main__":
    asyncio.run(test_server())
