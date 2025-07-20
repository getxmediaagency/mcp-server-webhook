# Read the server.py file
with open('mcp_server/core/server.py', 'r') as f:
    content = f.read()

# Add webhook_handler initialization after human_loop
content = content.replace(
    '        self.human_loop = HumanLoopManager()\n        \n        # Setup logging with unique server ID',
    '        self.human_loop = HumanLoopManager()\n        self.webhook_handler = WebhookHandler(self.action_registry)\n        \n        # Setup logging with unique server ID'
)

# Write back to file
with open('mcp_server/core/server.py', 'w') as f:
    f.write(content)

print("Fixed webhook_handler initialization")
