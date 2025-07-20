"""
Test script for webhook integration functionality.
"""

import asyncio
import aiohttp
import json
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from mcp_server.core.server import MCPServer
from mcp_server.actions.webhook_integration import process_webhook_data


async def test_webhook_integration():
    """Test the webhook integration functionality."""
    print("🧪 Testing Webhook Integration...")
    
    # Create server instance
    server = MCPServer(host="localhost", port=8002, debug=True)
    
    # Register webhook actions
    server.register_action("process_webhook_data", process_webhook_data)
    
    # Configure webhook secrets and routes
    server.register_webhook_secret("make.com", "test_secret_123")
    server.register_webhook_route("make.com_chatgpt_clients", "process_webhook_data")
    
    # Start server in background
    server_task = asyncio.create_task(server.start())
    
    # Wait a moment for server to start
    await asyncio.sleep(1)
    
    try:
        # Test Make.com webhook endpoint
        async with aiohttp.ClientSession() as session:
            # Simulate Make.com webhook payload based on the blueprint
            webhook_payload = {
                "client_id": "test-client-123",
                "action_id": "get_client_data",
                "task": {
                    "id": "task_123",
                    "name": "Test Client Task",
                    "description": "This is a test task for client data",
                    "status": {
                        "status": "in progress",
                        "color": "#ff6b6b"
                    },
                    "custom_fields": [
                        {
                            "id": "field_1",
                            "name": "Client ID",
                            "type": "text",
                            "value": "test-client-123"
                        },
                        {
                            "id": "field_2", 
                            "name": "Priority",
                            "type": "select",
                            "value": "High"
                        }
                    ],
                    "assignees": [
                        {
                            "id": 1,
                            "username": "testuser",
                            "email": "test@example.com",
                            "initials": "TU"
                        }
                    ]
                }
            }
            
            # Test Make.com specific webhook endpoint
            async with session.post(
                "http://localhost:8002/api/webhook/make.com/chatgpt-clients",
                json=webhook_payload
            ) as response:
                webhook_result = await response.json()
                print(f"✅ Make.com webhook test: {json.dumps(webhook_result, indent=2)}")
            
            # Test generic webhook endpoint
            async with session.post(
                "http://localhost:8002/api/webhook/make.com_chatgpt_clients",
                json=webhook_payload
            ) as response:
                generic_result = await response.json()
                print(f"✅ Generic webhook test: {json.dumps(generic_result, indent=2)}")
            
            # Test webhook data processing action directly
            action_result = await server.action_registry.execute_action(
                "process_webhook_data",
                {
                    "webhook_data": webhook_payload,
                    "client_id": "test-client-123"
                }
            )
            print(f"✅ Direct action test: {json.dumps(action_result, indent=2)}")
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
    finally:
        # Cancel server task
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            pass
    
    print("🎉 Webhook integration test completed!")


if __name__ == "__main__":
    asyncio.run(test_webhook_integration())
