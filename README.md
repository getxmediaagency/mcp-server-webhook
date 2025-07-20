# Modular MCP Server

A scalable, plugin-ready MCP (Model Context Protocol) server with human-in-the-loop collaboration capabilities.

## Features

- **Modular Architecture**: Plugin-ready action registry for easy extension
- **Human-in-the-Loop**: Built-in approval workflow for sensitive operations
- **Async Support**: Full async/await support with aiohttp
- **Comprehensive Logging**: Detailed logging with unique request tracking
- **Debugging Support**: Every operation has unique IDs for traceability
- **Production Ready**: Scalable design with error handling and monitoring

## Architecture

```
mcp_server/
├── core/                 # Core server components
│   ├── server.py        # Main MCPServer class
│   ├── action_registry.py # Action management system
│   └── human_loop.py    # Human approval workflow
├── actions/             # Action implementations
│   ├── client_data.py   # Client data actions
│   └── ...             # Additional action modules
├── utils/               # Utility functions
├── config/              # Configuration management
└── __init__.py         # Package initialization
```

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Server**:
   ```bash
   python main.py
   ```

3. **Test the Server**:
   ```bash
   # Health check
   curl http://localhost:8000/health
   
   # Get client data
   curl -X POST http://localhost:8000/api/action/get_client_data \
     -H "Content-Type: application/json" \
     -d '{"params": {"client_id": "test-client"}}'
   ```

## API Endpoints

### Core Endpoints

- `GET /health` - Health check
- `GET /api/status` - Server status and debugging info
- `GET /api/actions` - List available actions

### Action Execution

- `POST /api/action/{action_name}` - Execute an action
- `POST /api/approval/{request_id}` - Handle human approvals

## Human-in-the-Loop Workflow

Actions can be configured to require human approval:

1. **Action Registration**: Set `requires_approval=True` when registering actions
2. **Approval Request**: Server creates approval request when action is called
3. **Human Review**: Human reviews and approves/rejects the action
4. **Execution**: Approved actions are executed automatically

## Development

### Adding New Actions

1. Create action in `mcp_server/actions/`
2. Use `@action_handler` decorator for metadata
3. Register action in `main.py`

### Example Action

```python
from mcp_server.core.action_registry import action_handler

@action_handler(
    description="My custom action",
    requires_approval=True
)
async def my_action(params: Dict[str, Any]) -> Dict[str, Any]:
    # Action implementation
    return {"result": "success"}
```

## Configuration

The server supports configuration through environment variables:

- `MCP_HOST`: Server host (default: localhost)
- `MCP_PORT`: Server port (default: 8000)
- `MCP_DEBUG`: Enable debug mode (default: false)

## Logging

The server provides comprehensive logging:

- **Request Tracking**: Every request has a unique ID
- **Performance Monitoring**: Execution time tracking
- **Error Handling**: Detailed error logging with context
- **Human Loop**: Approval workflow logging

## Production Deployment

For production deployment:

1. Use a process manager (systemd, supervisor)
2. Configure reverse proxy (nginx, Apache)
3. Set up monitoring and alerting
4. Configure SSL/TLS certificates
5. Set up backup and recovery procedures

## Contributing

1. Follow the modular architecture
2. Add comprehensive documentation
3. Include unique IDs for all operations
4. Test thoroughly with async operations
5. Follow the human-in-the-loop workflow for sensitive operations
