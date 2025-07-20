"""
Real Webhook Endpoint Test

This script creates a test endpoint that will show exactly what data
your Make.com scenario should send to get real client data.
"""

import asyncio
import aiohttp
import json
import sys
from pathlib import Path
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from mcp_server.core.server import MCPServer
from mcp_server.actions.webhook_integration import (
    process_webhook_data,
    extract_client_knowledge_graph
)


async def test_real_webhook_endpoint():
    """Test the real webhook endpoint with detailed logging."""
    print("🔗 Testing Real Webhook Endpoint for Make.com Integration")
    print("=" * 70)
    
    # Create server instance
    server = MCPServer(host="localhost", port=8004, debug=True)
    
    # Register webhook actions
    server.register_action("process_webhook_data", process_webhook_data)
    server.register_action("extract_client_knowledge_graph", extract_client_knowledge_graph)
    
    # Configure webhook secrets and routes
    server.register_webhook_secret("make.com", "test_secret_86drqmpje")
    server.register_webhook_route("make.com_chatgpt_clients", "process_webhook_data")
    
    # Start server in background
    server_task = asyncio.create_task(server.start())
    
    # Wait a moment for server to start
    await asyncio.sleep(1)
    
    print("🌐 Webhook Endpoint Ready!")
    print(f"   URL: http://localhost:8004/api/webhook/make.com/chatgpt-clients")
    print(f"   Method: POST")
    print(f"   Content-Type: application/json")
    print()
    
    print("📋 Expected Make.com Webhook Payload Structure:")
    print("""
{
  "client_id": "86drqmpje",
  "action_id": "get_client_data",
  "task": {
    "id": "your_clickup_task_id",
    "name": "Task Name from ClickUp",
    "description": "Task Description from ClickUp",
    "custom_fields": [
      {
        "id": "field_id",
        "name": "Field Name",
        "type": "text",
        "value": "Field Value"
      }
    ],
    "assignees": [
      {
        "id": 123,
        "username": "username",
        "email": "email@example.com"
      }
    ]
  }
}
""")
    
    print("�� Make.com Scenario Configuration:")
    print("""
1. In your Make.com scenario "GPT - Get Client Knowledge Graph":
   - Webhook URL: http://localhost:8004/api/webhook/make.com/chatgpt-clients
   - Method: POST
   - Content-Type: application/json
   
2. The webhook should send the ClickUp task data in the format above
   
3. The server will automatically:
   - Extract client_id from custom fields or payload
   - Process the task data
   - Create a knowledge graph
   - Return structured data
""")
    
    print("🧪 Testing with minimal payload...")
    
    # Test with minimal payload to see what happens
    minimal_payload = {
        "client_id": "86drqmpje",
        "action_id": "get_client_data"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:8004/api/webhook/make.com/chatgpt-clients",
                json=minimal_payload
            ) as response:
                result = await response.json()
                print("✅ Minimal payload test successful!")
                print(f"   Status: {result.get('status')}")
                print(f"   Client ID: {result.get('client_id')}")
                print(f"   Webhook ID: {result.get('webhook_id')}")
                
                if 'result' in result:
                    print(f"   Processed Data: {json.dumps(result['result'], indent=2)}")
    
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    print()
    print("📊 Server Status:")
    print("   - Webhook endpoint is ready to receive data")
    print("   - Server will log all incoming webhooks")
    print("   - Check server logs for detailed information")
    print()
    print("🎯 Next Steps:")
    print("   1. Update your Make.com scenario with the webhook URL above")
    print("   2. Configure the webhook to send ClickUp task data")
    print("   3. Test the scenario to see real client data")
    print("   4. Check server logs for detailed processing information")
    
    # Keep server running for manual testing
    print()
    print("⏳ Server is running... Press Ctrl+C to stop")
    print("   You can now test your Make.com scenario!")
    
    try:
        await asyncio.Future()  # Keep running
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
    finally:
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            pass


if __name__ == "__main__":
    asyncio.run(test_real_webhook_endpoint())
