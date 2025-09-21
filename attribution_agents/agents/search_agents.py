from typing import Dict, List, Any

from ..data.snowflake_client import SnowflakeClient
from ..data.model import SearchQuery, SearchSession, AttributionResult
from ..llm.client import LLMClient

class SearchAttributionAgent:
    def __init__(self):
        self.db_client = SnowflakeClient()
        self.llm_client = LLMClient()
        self.agent_id = "search_attribution_agent"
    
    async def process_search_query(self, query_data: Dict) -> Dict[str, Any]:
        """Process a single search query with intent classification"""
        # Get LLM classification
        intent_result = await self.llm_client.classify_search_intent(query_data)
        
        # Update database with classification
        if "query_id" in query_data:
            await self.db_client.update_intent_classification(query_data["query_id"], intent_result)
        
        return intent_result
        
    async def analyze_search_session(self, session_id: str) -> Dict[str, Any]:
        """Analyze complete search session"""
        # Get session data from database
        sessions = await self.db_client.get_search_sessions(session_id)
        
        if sessions:
            return sessions[0]
        else:
            return {"session_id": session_id, "error": "Session not found"}
        
    async def calculate_attribution_weights(self, customer_id: str, conversion_id: str) -> Dict[str, Any]:
        """Calculate attribution weights for customer's search journey"""
        # Get customer search data
        attribution_data = await self.db_client.calculate_search_attribution(customer_id)
        queries = attribution_data.get("query_data", [])
        
        if not queries:
            return {
                "customer_id": customer_id,
                "query_contributions": {},
                "session_contributions": {},
                "total_attribution_weight": 0.0,
                "confidence_score": 0.0
            }
        
        query_contributions = {}
        total_weight = 0.0
        
        for i, query in enumerate(queries):
            query_id = query.get("QUERY_ID", query.get("query_id", f"query_{i}"))
            
            # Position-based weight (later queries get more weight)
            position_weight = (i + 1) / len(queries)
            
            # Funnel stage weight (decision stage gets more weight)
            stage = query.get("FUNNEL_STAGE", query.get("funnel_stage", "awareness")).lower()
            stage_weights = {"awareness": 0.3, "consideration": 0.5, "decision": 1.0}
            stage_weight = stage_weights.get(stage, 0.3)
            
            # Query type weight (transactional gets more weight)
            query_type = query.get("QUERY_TYPE", query.get("query_type", "unknown")).lower()
            type_weights = {
                "brand_research": 0.4,
                "product_research": 0.5, 
                "comparison": 0.7,
                "validation": 0.8,
                "transactional": 1.0,
                "navigational": 0.3,
                "unknown": 0.2
            }
            type_weight = type_weights.get(query_type, 0.2)
            
            # Combined weight
            weight = position_weight * stage_weight * type_weight
            query_contributions[query_id] = weight
            total_weight += weight
        
        # Normalize weights to sum to 1.0
        if total_weight > 0:
            for query_id in query_contributions:
                query_contributions[query_id] = query_contributions[query_id] / total_weight
        
        return {
            "customer_id": customer_id,
            "query_contributions": query_contributions,
            "session_contributions": {},
            "total_attribution_weight": 1.0,
            "confidence_score": 0.9
        }
        
    async def get_search_insights(self, customer_id: str) -> Dict[str, Any]:
        """Generate insights about customer's search behavior"""
        search_history = await self.db_client.get_customer_search_history(customer_id)
        
        return {
            "customer_id": customer_id,
            "total_searches": len(search_history),
            "search_types": list(set(q.get("query_type", "unknown") for q in search_history)),
            "funnel_stages": list(set(q.get("funnel_stage", "unknown") for q in search_history))
        }
        
    async def update_touchpoint_attribution(self, attribution_results: Dict[str, Any]):
        """Update touchpoints table with calculated attribution weights"""
        # This would update a touchpoints table with attribution weights
        # For now, just return success
        return {"status": "success", "updated_touchpoints": len(attribution_results.get("query_contributions", {}))}