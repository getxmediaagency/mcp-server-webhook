"""
Test Make.com Webhook with Authentication

This script sends a test request to your Make.com webhook
with proper authentication using the API key.
"""

import asyncio
import aiohttp
import json
from datetime import datetime

async def test_make_com_webhook_auth():
    """Test the Make.com webhook with authentication."""
    
    print("🧪 Testing Make.com Webhook with Authentication")
    print("=" * 55)
    
    # Your Make.com webhook URL and API key
    webhook_url = "YOUR_WEBHOOK_URL"
    api_key = "YOUR_MAKE_API_KEY"
    
    # Test data with your client ID
    test_data = {
        "client_id": "86drqmpje"
    }
    
    # Headers with authentication
    headers = {
        'Content-Type': 'application/json',
        'x-make-apikey': api_key
    }
    
    print(f"📤 Sending authenticated test data to Make.com webhook...")
    print(f"   URL: {webhook_url}")
    print(f"   Client ID: 86drqmpje")
    print(f"   API Key: {api_key[:8]}...")
    print(f"   Data: {json.dumps(test_data, indent=2)}")
    print()
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                webhook_url,
                json=test_data,
                headers=headers
            ) as response:
                
                print(f"📊 Response Status: {response.status}")
                print(f"📊 Response Headers: {dict(response.headers)}")
                
                # Try to get the response body
                try:
                    response_text = await response.text()
                    print(f"📊 Response Body: {response_text}")
                    
                    # Try to parse as JSON
                    try:
                        response_json = await response.json()
                        print(f"📊 Response JSON: {json.dumps(response_json, indent=2)}")
                        
                        # Analyze the response structure
                        print("\n🔍 Response Analysis:")
                        if isinstance(response_json, dict):
                            print(f"   - Type: Dictionary with {len(response_json)} keys")
                            print(f"   - Keys: {list(response_json.keys())}")
                            
                            # Look for custom_fields or task data
                            if 'custom_fields' in response_json:
                                print(f"   - Custom Fields Found: {response_json['custom_fields']}")
                            elif 'task' in response_json:
                                print(f"   - Task Data Found: {response_json['task']}")
                            else:
                                print(f"   - Raw Data: {response_json}")
                        elif isinstance(response_json, list):
                            print(f"   - Type: Array with {len(response_json)} items")
                            print(f"   - Items: {response_json}")
                        else:
                            print(f"   - Type: {type(response_json)}")
                            print(f"   - Value: {response_json}")
                            
                    except Exception as e:
                        print(f"📊 Response is not JSON format: {e}")
                        print(f"📊 Raw response: {response_text}")
                        
                except Exception as e:
                    print(f"📊 Could not read response body: {e}")
                
                print()
                if response.status == 200:
                    print("✅ Test completed successfully!")
                    print("   Your Make.com scenario processed the request")
                    print("   Check the response above for the real data structure")
                else:
                    print(f"⚠️  Test completed with status {response.status}")
                    print("   Check the response for any error messages")
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("   Check the webhook URL and API key")

if __name__ == "__main__":
    asyncio.run(test_make_com_webhook_auth())
