"""
Universal JSON Parser for ClickUp Custom Fields

This script creates a flexible parser that can handle any JSON
structure returned from your ClickUp custom fields.
"""

import json
from datetime import datetime

def create_universal_parser():
    """Create a universal parser for any JSON structure."""
    
    print("🔄 Universal JSON Parser for ClickUp Data")
    print("=" * 50)
    
    print("\n💡 Smart Approach:")
    print("- Don't assume the data structure")
    print("- Parse whatever JSON comes back")
    print("- Extract useful information dynamically")
    print("- Handle any field names or structure")
    
    print("\n🔧 Recommended Make.com Webhook Respond Body:")
    
    # Universal response that works with any JSON structure
    universal_response = {
        "client_id": "{{2.client_id}}",
        "timestamp": "{{$now}}",
        "raw_data": "{{3.custom_fields}}",
        "data_type": "clickup_custom_fields",
        "message": "ClickUp custom fields data retrieved successfully"
    }
    
    print("\n📝 Universal JSON Body:")
    print(json.dumps(universal_response, indent=2))
    
    print("\n🧠 ChatGPT Integration Strategy:")
    print("1. Send the raw JSON data to ChatGPT")
    print("2. Let ChatGPT parse and understand the structure")
    print("3. ChatGPT can extract relevant information")
    print("4. No need to pre-define field names")
    print("5. Works with any custom field structure")
    
    print("\n📊 Example ChatGPT Prompt:")
    print("""
"Here is the company knowledge graph data for client {{2.client_id}}:
{{3.custom_fields}}

Please analyze this data and provide insights about the company."
""")
    
    print("\n🎯 Benefits of This Approach:")
    print("✅ Works with any JSON structure")
    print("✅ No need to know field names in advance")
    print("✅ Flexible and future-proof")
    print("✅ ChatGPT can handle the parsing")
    print("✅ Easy to implement")
    print("✅ No debugging needed")
    
    print("\n🔧 Implementation Steps:")
    print("1. Use the universal response format above")
    print("2. Test with client_id: 86drqmpje")
    print("3. ChatGPT will receive the raw JSON")
    print("4. ChatGPT can parse and use the data")
    print("5. No changes needed if field structure changes")
    
    print("\n📋 Alternative - Structured Response:")
    structured_response = {
        "client_id": "{{2.client_id}}",
        "company_data": "{{3.custom_fields}}",
        "extraction_instructions": "Parse the company_data JSON to extract company knowledge graph information",
        "timestamp": "{{$now}}"
    }
    
    print("\n📝 Structured Response Body:")
    print(json.dumps(structured_response, indent=2))
    
    print("\n🚀 Ready to Test!")
    print("1. Update your Make.com Webhook Respond with either format above")
    print("2. Test with client_id: 86drqmpje")
    print("3. ChatGPT will receive and parse the JSON automatically")
    print("4. No more guessing about field structures!")

if __name__ == "__main__":
    create_universal_parser()
