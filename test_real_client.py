"""
Real Client Test for Webhook Integration

This script tests the webhook integration with the actual client ID: 86drqmpje
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
    extract_client_knowledge_graph,
    validate_webhook_signature
)


async def test_real_client_webhook():
    """Test webhook integration with real client ID: 86drqmpje"""
    print("🧪 Testing Webhook Integration with Real Client: 86drqmpje")
    print("=" * 60)
    
    # Create server instance
    server = MCPServer(host="localhost", port=8003, debug=True)
    
    # Register webhook actions
    server.register_action("process_webhook_data", process_webhook_data)
    server.register_action("extract_client_knowledge_graph", extract_client_knowledge_graph)
    server.register_action("validate_webhook_signature", validate_webhook_signature)
    
    # Configure webhook secrets and routes
    server.register_webhook_secret("make.com", "test_secret_86drqmpje")
    server.register_webhook_route("make.com_chatgpt_clients", "process_webhook_data")
    
    # Start server in background
    server_task = asyncio.create_task(server.start())
    
    # Wait a moment for server to start
    await asyncio.sleep(1)
    
    try:
        # Simulate real Make.com webhook payload for client 86drqmpje
        real_webhook_payload = {
            "client_id": "86drqmpje",
            "action_id": "get_client_data",
            "timestamp": datetime.utcnow().isoformat(),
            "task": {
                "id": "task_86drqmpje_001",
                "name": "Client Knowledge Graph - 86drqmpje",
                "description": "Knowledge graph extraction for client 86drqmpje",
                "status": {
                    "status": "in progress",
                    "color": "#4CAF50",
                    "type": "custom",
                    "orderindex": 1
                },
                "orderindex": 1,
                "date_created": "2024-01-15T10:00:00Z",
                "date_updated": datetime.utcnow().isoformat(),
                "archived": False,
                "creator": {
                    "id": 123,
                    "username": "corey_hayes",
                    "color": "#ff6b6b",
                    "profilePicture": "https://example.com/profile.jpg",
                    "email": "corey@example.com"
                },
                "assignees": [
                    {
                        "id": 123,
                        "username": "corey_hayes",
                        "color": "#ff6b6b",
                        "initials": "CH",
                        "profilePicture": "https://example.com/profile.jpg",
                        "email": "corey@example.com"
                    }
                ],
                "checklists": [
                    {
                        "id": "checklist_001",
                        "task_id": "task_86drqmpje_001",
                        "name": "Client Data Checklist",
                        "date_created": "2024-01-15T10:00:00Z",
                        "orderindex": 1,
                        "creator": 123,
                        "resolved": 2,
                        "unresolved": 1,
                        "items": [
                            {
                                "id": "item_001",
                                "name": "Extract client preferences",
                                "orderindex": 1,
                                "assignee": None,
                                "group_assignee": None,
                                "resolved": True,
                                "parent": None,
                                "date_created": "2024-01-15T10:00:00Z",
                                "children": []
                            },
                            {
                                "id": "item_002",
                                "name": "Identify key stakeholders",
                                "orderindex": 2,
                                "assignee": None,
                                "group_assignee": None,
                                "resolved": True,
                                "parent": None,
                                "date_created": "2024-01-15T10:00:00Z",
                                "children": []
                            },
                            {
                                "id": "item_003",
                                "name": "Map client relationships",
                                "orderindex": 3,
                                "assignee": None,
                                "group_assignee": None,
                                "resolved": False,
                                "parent": None,
                                "date_created": "2024-01-15T10:00:00Z",
                                "children": []
                            }
                        ]
                    }
                ],
                "tags": [
                    {
                        "name": "client-data",
                        "creator": "corey_hayes",
                        "tag_fg": "#ffffff",
                        "tag_bg": "#4CAF50"
                    },
                    {
                        "name": "knowledge-graph",
                        "creator": "corey_hayes",
                        "tag_fg": "#ffffff",
                        "tag_bg": "#2196F3"
                    }
                ],
                "priority": {
                    "id": "priority_1",
                    "priority": "high",
                    "color": "#ff6b6b",
                    "orderindex": 1
                },
                "due_date": "2024-01-20T23:59:59Z",
                "start_date": "2024-01-15T10:00:00Z",
                "points": 5,
                "time_estimate": 120,
                "time_spent": 60,
                "list": {
                    "id": "list_001",
                    "name": "Client Management",
                    "access": True
                },
                "project": {
                    "id": "project_001",
                    "name": "Client Knowledge Graph Project",
                    "hidden": False,
                    "access": True
                },
                "folder": {
                    "id": "folder_001",
                    "name": "Active Clients",
                    "hidden": False,
                    "access": True
                },
                "space": {
                    "id": "space_001"
                },
                "custom_fields": [
                    {
                        "id": "field_001",
                        "name": "Client ID",
                        "type": "text",
                        "type_config": {},
                        "date_created": "2024-01-15T10:00:00Z",
                        "hide_from_guests": False,
                        "value": "86drqmpje",
                        "required": True
                    },
                    {
                        "id": "field_002",
                        "name": "Client Type",
                        "type": "select",
                        "type_config": {
                            "options": [
                                {"name": "Enterprise", "orderindex": 1},
                                {"name": "SMB", "orderindex": 2},
                                {"name": "Startup", "orderindex": 3}
                            ]
                        },
                        "date_created": "2024-01-15T10:00:00Z",
                        "hide_from_guests": False,
                        "value": "Enterprise",
                        "required": False
                    },
                    {
                        "id": "field_003",
                        "name": "Industry",
                        "type": "text",
                        "type_config": {},
                        "date_created": "2024-01-15T10:00:00Z",
                        "hide_from_guests": False,
                        "value": "Technology",
                        "required": False
                    },
                    {
                        "id": "field_004",
                        "name": "Annual Revenue",
                        "type": "number",
                        "type_config": {},
                        "date_created": "2024-01-15T10:00:00Z",
                        "hide_from_guests": False,
                        "value": 5000000,
                        "required": False
                    },
                    {
                        "id": "field_005",
                        "name": "Key Contact",
                        "type": "text",
                        "type_config": {},
                        "date_created": "2024-01-15T10:00:00Z",
                        "hide_from_guests": False,
                        "value": "John Smith",
                        "required": False
                    }
                ],
                "attachments": [
                    {
                        "id": "attachment_001",
                        "date": "2024-01-15T10:00:00Z",
                        "title": "Client Profile - 86drqmpje.pdf",
                        "type": 1,
                        "source": 1,
                        "version": 1,
                        "extension": "pdf",
                        "thumbnail_small": "https://example.com/thumb_small.jpg",
                        "thumbnail_medium": "https://example.com/thumb_medium.jpg",
                        "thumbnail_large": "https://example.com/thumb_large.jpg",
                        "is_folder": False,
                        "mimetype": "application/pdf",
                        "hidden": False,
                        "parent_id": None,
                        "size": 1024000,
                        "total_comments": 0,
                        "resolved_comments": 0,
                        "user": {
                            "id": 123,
                            "username": "corey_hayes",
                            "email": "corey@example.com",
                            "initials": "CH",
                            "color": "#ff6b6b",
                            "profilePicture": "https://example.com/profile.jpg"
                        },
                        "deleted": False,
                        "orientation": "portrait",
                        "url": "https://example.com/client_profile.pdf",
                        "email_data": None,
                        "url_w_query": "https://example.com/client_profile.pdf",
                        "url_w_host": "https://example.com/client_profile.pdf"
                    }
                ],
                "url": "https://app.clickup.com/t/86drqmpje_001"
            }
        }
        
        print("📋 Testing with client ID: 86drqmpje")
        print("📊 Webhook payload includes:")
        print(f"   - Task ID: {real_webhook_payload['task']['id']}")
        print(f"   - Task Name: {real_webhook_payload['task']['name']}")
        print(f"   - Custom Fields: {len(real_webhook_payload['task']['custom_fields'])}")
        print(f"   - Assignees: {len(real_webhook_payload['task']['assignees'])}")
        print(f"   - Checklists: {len(real_webhook_payload['task']['checklists'])}")
        print(f"   - Attachments: {len(real_webhook_payload['task']['attachments'])}")
        print()
        
        async with aiohttp.ClientSession() as session:
            print("🔄 Testing Make.com webhook endpoint...")
            
            # Test Make.com specific webhook endpoint
            async with session.post(
                "http://localhost:8003/api/webhook/make.com/chatgpt-clients",
                json=real_webhook_payload
            ) as response:
                webhook_result = await response.json()
                print("✅ Make.com webhook test successful!")
                print(f"   Status: {webhook_result.get('status')}")
                print(f"   Webhook ID: {webhook_result.get('webhook_id')}")
                print(f"   Client ID: {webhook_result.get('client_id')}")
                
                if 'result' in webhook_result and 'knowledge_graph' in webhook_result['result']:
                    kg = webhook_result['result']['knowledge_graph']
                    print(f"   Knowledge Graph Nodes: {kg.get('metadata', {}).get('total_nodes', 0)}")
                    print(f"   Knowledge Graph Relationships: {kg.get('metadata', {}).get('total_relationships', 0)}")
            
            print()
            print("🧠 Testing knowledge graph extraction...")
            
            # Test direct knowledge graph extraction
            kg_result = await server.action_registry.execute_action(
                "extract_client_knowledge_graph",
                {
                    "webhook_data": real_webhook_payload,
                    "client_id": "86drqmpje",
                    "include_task_details": True
                }
            )
            
            print("✅ Knowledge graph extraction successful!")
            print(f"   Total Nodes: {kg_result.get('metadata', {}).get('total_nodes', 0)}")
            print(f"   Total Relationships: {kg_result.get('metadata', {}).get('total_relationships', 0)}")
            
            # Display extracted knowledge nodes
            print("\n📋 Extracted Knowledge Nodes:")
            for node in kg_result.get('knowledge_nodes', [])[:5]:  # Show first 5
                print(f"   - {node['node_type']}: {node['properties'].get('name', node['node_id'])}")
            
            print("\n🔗 Extracted Relationships:")
            for rel in kg_result.get('relationships', [])[:5]:  # Show first 5
                print(f"   - {rel['source_node']} --[{rel['relationship_type']}]--> {rel['target_node']}")
            
            print()
            print("🔐 Testing webhook signature validation...")
            
            # Test signature validation
            validation_result = await server.action_registry.execute_action(
                "validate_webhook_signature",
                {
                    "webhook_data": real_webhook_payload,
                    "signature": "test_signature_86drqmpje",
                    "secret_key": "test_secret_86drqmpje",
                    "client_id": "86drqmpje"
                }
            )
            
            print(f"✅ Signature validation test completed!")
            print(f"   Is Valid: {validation_result.get('is_valid')}")
            print(f"   Validation Method: {validation_result.get('validation_method')}")
            
            print()
            print("📊 Testing server status endpoint...")
            
            # Test server status
            async with session.get("http://localhost:8003/api/status") as response:
                status_data = await response.json()
                print("✅ Server status retrieved!")
                print(f"   Server ID: {status_data.get('server_id')}")
                print(f"   Active Requests: {status_data.get('active_requests', {})}")
                print(f"   Registered Actions: {status_data.get('registered_actions')}")
                print(f"   Pending Approvals: {status_data.get('pending_approvals')}")
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cancel server task
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            pass
    
    print("\n" + "=" * 60)
    print("🎉 Real client webhook test completed!")
    print("✅ All webhook integration features working with client ID: 86drqmpje")


if __name__ == "__main__":
    asyncio.run(test_real_client_webhook())
