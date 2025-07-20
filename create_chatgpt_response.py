"""
Create ChatGPT-Compatible Response Format

This script shows how to structure the Make.com response so ChatGPT
can understand and use the client data effectively.
"""

import json
from datetime import datetime

def create_chatgpt_response_format():
    """Create a ChatGPT-compatible response format for client data."""
    
    print("🤖 Creating ChatGPT-Compatible Response Format")
    print("=" * 60)
    
    print("\n📋 Current Make.com Setup:")
    print("- Webhook Trigger: Receives client_id")
    print("- ClickUp Get Task: Gets full task data")
    print("- Webhook Respond: Returns to ChatGPT")
    print("- Custom Fields: Contains full task data")
    
    print("\n🔧 Recommended Response Format:")
    print("\nIn your Make.com Webhook Respond module, use this body:")
    
    chatgpt_response = {
        "client_data": {
            "client_id": "{{2.client_id}}",
            "timestamp": "{{$now}}",
            "task_info": {
                "task_id": "{{3.id}}",
                "task_name": "{{3.name}}",
                "description": "{{3.description}}",
                "status": "{{3.status.status}}",
                "priority": "{{3.priority.priority}}",
                "due_date": "{{3.due_date}}",
                "created_date": "{{3.date_created}}",
                "updated_date": "{{3.date_updated}}"
            },
            "custom_fields": "{{3.custom_fields}}",
            "assignees": "{{3.assignees}}",
            "tags": "{{3.tags}}",
            "attachments": "{{3.attachments}}",
            "checklists": "{{3.checklists}}"
        },
        "knowledge_graph": {
            "nodes": [
                {
                    "type": "client",
                    "id": "{{2.client_id}}",
                    "properties": {
                        "name": "{{3.name}}",
                        "status": "{{3.status.status}}",
                        "priority": "{{3.priority.priority}}"
                    }
                }
            ],
            "relationships": []
        },
        "summary": "Client data retrieved successfully from ClickUp task {{3.id}}"
    }
    
    print("\n📝 JSON Body for Webhook Respond:")
    print(json.dumps(chatgpt_response, indent=2))
    
    print("\n🎯 Alternative - Simple Format:")
    simple_response = {
        "client_id": "{{2.client_id}}",
        "task_id": "{{3.id}}",
        "task_name": "{{3.name}}",
        "status": "{{3.status.status}}",
        "custom_fields": "{{3.custom_fields}}",
        "assignees": "{{3.assignees}}",
        "message": "Client data retrieved from ClickUp"
    }
    
    print("\n📝 Simple JSON Body:")
    print(json.dumps(simple_response, indent=2))
    
    print("\n🔍 Understanding Custom Fields:")
    print("The custom_fields contains:")
    print("- Client ID")
    print("- Client Type")
    print("- Industry")
    print("- Annual Revenue")
    print("- Key Contact")
    print("- Any other custom fields you've set up")
    
    print("\n💡 ChatGPT Integration Tips:")
    print("1. Structure the response clearly")
    print("2. Include all relevant client information")
    print("3. Make it easy for ChatGPT to parse")
    print("4. Include a summary or message")
    print("5. Use consistent field names")
    
    print("\n🧪 Testing Your Setup:")
    print("1. Update your Make.com Webhook Respond body")
    print("2. Test with client_id: 86drqmpje")
    print("3. Check what ChatGPT receives")
    print("4. Verify all client data is included")
    
    print("\n📊 Expected Data Flow:")
    print("""
ChatGPT Request
    ↓
Make.com Webhook Trigger
    ↓
ClickUp Get Task (86drqmpje)
    ↓
Webhook Respond (Structured Data)
    ↓
ChatGPT Receives Client Data
    ↓
ChatGPT Uses Data for Responses
""")

if __name__ == "__main__":
    create_chatgpt_response_format()
