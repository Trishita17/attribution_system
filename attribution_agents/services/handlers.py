from typing import Dict, Any
from ..agents.search_agents import SearchAttributionAgent
from ..agents.display_agents import DisplayAttributionAgent
from ..agents.display_agents import DisplayAttributionAgent

class MCPMessageHandler:
    def __init__(self):
        self.search_agent = SearchAttributionAgent()
        self.display_agent = DisplayAttributionAgent()
    
    async def handle_search_analysis_request(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle requests for search attribution analysis"""
        customer_id = message.get('customer_id')
        conversion_id = message.get('conversion_id')
        
        if not customer_id or not conversion_id:
            return {"error": "Missing customer_id or conversion_id"}
        
        result = await self.search_agent.calculate_attribution_weights(customer_id, conversion_id)
        return {"status": "success", "data": result}
        
    async def handle_display_analysis_request(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle requests for display attribution analysis"""
        customer_id = message.get('customer_id')
        conversion_id = message.get('conversion_id')
        
        if not customer_id or not conversion_id:
            return {"error": "Missing customer_id or conversion_id"}
        
        result = await self.display_agent.calculate_display_attribution(customer_id, conversion_id)
        return {"status": "success", "data": result}
        
    async def handle_customer_journey_request(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle requests for customer journey insights"""
        customer_id = message.get('customer_id')
        
        if not customer_id:
            return {"error": "Missing customer_id"}
        
        search_insights = await self.search_agent.get_search_insights(customer_id)
        display_insights = await self.display_agent.get_display_insights(customer_id)
        
        return {
            "status": "success",
            "data": {
                "customer_id": customer_id,
                "search_insights": search_insights,
                "display_insights": display_insights
            }
        }
        
    async def handle_attribution_update_request(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle requests to update attribution weights"""
        attribution_results = message.get('attribution_results')
        agent_type = message.get('agent_type', 'search')
        
        if not attribution_results:
            return {"error": "Missing attribution_results"}
        
        if agent_type == 'search':
            result = await self.search_agent.update_touchpoint_attribution(attribution_results)
        elif agent_type == 'display':
            result = await self.display_agent.update_display_attribution(attribution_results)
        else:
            return {"error": "Invalid agent_type"}
        
        return {"status": "success", "data": result}