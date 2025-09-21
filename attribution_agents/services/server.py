import asyncio
from mcp.server import Server
from .handlers import MCPMessageHandler

class MultiAgentAttributionMCPServer:
    def __init__(self):
        self.server = Server("multi-agent-attribution")
        self.handler = MCPMessageHandler()
        self.setup_routes()
    
    def setup_routes(self):
        """Setup MCP message routing"""
        @self.server.list_tools()
        async def handle_list_tools():
            return [
                {
                    "name": "search_attribution",
                    "description": "Calculate search attribution weights",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "customer_id": {"type": "string"},
                            "conversion_id": {"type": "string"}
                        },
                        "required": ["customer_id", "conversion_id"]
                    }
                },
                {
                    "name": "display_attribution",
                    "description": "Calculate display attribution weights",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "customer_id": {"type": "string"},
                            "conversion_id": {"type": "string"}
                        },
                        "required": ["customer_id", "conversion_id"]
                    }
                },
                {
                    "name": "customer_journey",
                    "description": "Get comprehensive customer journey insights",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "customer_id": {"type": "string"}
                        },
                        "required": ["customer_id"]
                    }
                }
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict):
            if name == "search_attribution":
                return await self.handler.handle_search_analysis_request(arguments)
            elif name == "display_attribution":
                return await self.handler.handle_display_analysis_request(arguments)
            elif name == "customer_journey":
                return await self.handler.handle_customer_journey_request(arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")
        
    async def start(self):
        """Start the MCP server"""
        await self.server.run()
        
    async def stop(self):
        """Stop the MCP server"""
        # Server cleanup if needed
        pass