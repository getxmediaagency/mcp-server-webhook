"""
Test Webhook Client

This script simulates what your Make.com scenario would send
to test the webhook endpoint.
"""

import asyncio
import aiohttp
import json
from datetime import datetime

async def test_webhook_client():
    """Test the webhook endpoint with simulated Make.com data."""
    
    print("🧪 Testing Webhook Client")
    print("=" * 40)
    
    # Simulate the data your Make.com scenario would send
    test_data = {
        "client_id": "86drqmpje",
        "timestamp": datetime.now().isoformat(),
        "raw_data": "{{3.custom_fields}}",  # This would be the actual custom fields
        "data_type": "clickup_custom_fields",
        "message": "ClickUp custom fields data retrieved successfully"
    }
    
    print("📤 Sending test data to webhook...")
    print(f"   Data: {json.dumps(test_data, indent=2)}")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:8005/test-webhook",
                json=test_data
            ) as response:
                result = await response.json()
                print("✅ Test webhook call successful!")
                print(f"   Status: {result.get('status')}")
                print(f"   Message: {result.get('message')}")
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("   Make sure the webhook server is running first!")

if __name__ == "__main__":
    asyncio.run(test_webhook_client())
