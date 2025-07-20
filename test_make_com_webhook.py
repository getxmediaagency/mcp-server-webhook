"""
Test Make.com Webhook with Real Client Data

This script sends a test request to your Make.com webhook
to trigger the scenario and see the real data structure.
"""

import asyncio
import aiohttp
import json
from datetime import datetime

async def test_make_com_webhook():
    """Test the Make.com webhook with real client data."""
    
    print("🧪 Testing Make.com Webhook")
    print("=" * 40)
    
    # Your Make.com webhook URL
    webhook_url = "YOUR_WEBHOOK_URL"
    
    # Test data with your client ID
    test_data = {
        "client_id": "86drqmpje"
    }
    
    print(f"📤 Sending test data to Make.com webhook...")
    print(f"   URL: {webhook_url}")
    print(f"   Client ID: 86drqmpje")
    print(f"   Data: {json.dumps(test_data, indent=2)}")
    print()
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                webhook_url,
                json=test_data,
                headers={'Content-Type': 'application/json'}
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
                    except:
                        print("📊 Response is not JSON format")
                        
                except Exception as e:
                    print(f"📊 Could not read response body: {e}")
                
                print()
                print("✅ Test completed!")
                print("   Check your Make.com scenario logs for processing details")
                print("   The response above shows what your scenario returned")
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("   Check the webhook URL and try again")

if __name__ == "__main__":
    asyncio.run(test_make_com_webhook())
