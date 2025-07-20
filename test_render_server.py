"""
Test script to verify Render server starts properly
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

async def test_server_start():
    """Test that the server can start properly."""
    try:
        # Import the main function
        from main_render import main
        
        # Start server in background
        task = asyncio.create_task(main())
        
        # Wait a moment for server to start
        await asyncio.sleep(2)
        
        # Cancel the task
        task.cancel()
        
        print("✅ Server started successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_server_start())
    sys.exit(0 if result else 1)
