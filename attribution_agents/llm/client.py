from typing import Dict, Any, Optional, List
import json
import logging

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self):
        self.model = "claude-3-haiku-20240307"
        logger.info("LLM Client initialized (mock mode)")
    
    async def classify_search_intent(self, query_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock search intent classification"""
        query_text = query_data.get('query_text', '').lower()
        
        # Simple rule-based classification for demo
        if any(word in query_text for word in ['buy', 'purchase', 'order', 'price']):
            intent_category = 'transactional'
            funnel_stage = 'decision'
            purchase_intent = 0.9
        elif any(word in query_text for word in ['compare', 'vs', 'versus', 'best']):
            intent_category = 'comparison'
            funnel_stage = 'consideration'
            purchase_intent = 0.7
        elif any(word in query_text for word in ['review', 'rating', 'opinion']):
            intent_category = 'validation'
            funnel_stage = 'consideration'
            purchase_intent = 0.6
        else:
            intent_category = 'product_research'
            funnel_stage = 'awareness'
            purchase_intent = 0.4
        
        return {
            'intent_category': intent_category,
            'funnel_stage': funnel_stage,
            'purchase_intent_score': purchase_intent,
            'urgency_score': 0.5,
            'confidence_score': 0.8
        }
    
    async def analyze_search_attribution(self, journey_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock search attribution analysis"""
        queries = journey_data.get('queries', [])
        
        if not queries:
            return {'query_contributions': {}, 'confidence_score': 0.0}
        
        # Simple position-based attribution
        contributions = {}
        total_queries = len(queries)
        
        for i, query in enumerate(queries):
            query_id = query.get('query_id', f'query_{i}')
            # Later queries get more weight
            weight = (i + 1) / sum(range(1, total_queries + 1))
            contributions[query_id] = weight
        
        return {
            'query_contributions': contributions,
            'confidence_score': 0.8,
            'attribution_method': 'position_based'
        }
    
    async def analyze_creative_performance(self, creative_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock creative performance analysis"""
        performance_metrics = creative_data.get("performance_metrics", {})
        
        ctr = performance_metrics.get("ctr", 0)
        cvr = performance_metrics.get("cvr", 0)
        
        if ctr >= 0.05 and cvr >= 0.03:
            tier = "top_performer"
            recommendations = ["Scale successful elements", "Test similar creatives"]
        elif ctr >= 0.03 or cvr >= 0.02:
            tier = "good_performer"
            recommendations = ["Optimize targeting", "Test new formats"]
        else:
            tier = "underperformer"
            recommendations = ["Review creative strategy", "Test new messaging"]
        
        return {
            "performance_tier": tier,
            "recommendations": recommendations,
            "confidence_score": 0.85
        }
    
    async def analyze_video_engagement(self, engagement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock video engagement analysis"""
        avg_completion = engagement_data.get("avg_completion_rate", 0)
        
        if avg_completion >= 0.75:
            tier = "high_engagement"
            recommendations = ["Continue strategy", "Increase frequency"]
        elif avg_completion >= 0.50:
            tier = "medium_engagement"
            recommendations = ["Optimize length", "Improve hooks"]
        else:
            tier = "low_engagement"
            recommendations = ["Shorten videos", "Test new themes"]
        
        return {
            "engagement_tier": tier,
            "recommendations": recommendations,
            "optimal_length": 30 if avg_completion < 0.5 else 60,
            "confidence_score": 0.7
        }
    
    async def analyze_display_attribution(self, journey_data: Dict[str, Any], conversion_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Mock display attribution analysis"""
        touchpoints = journey_data.get("display_touchpoints", [])
        
        if not touchpoints:
            return {"touchpoint_contributions": {}, "confidence_score": 0.0}
        
        # Viewability and recency weighted attribution
        contributions = {}
        total_weight = 0
        
        for i, tp in enumerate(touchpoints):
            viewability = tp.get("viewability_score", 0.5)
            recency_weight = (i + 1) / len(touchpoints)
            weight = viewability * recency_weight
            
            tp_id = tp.get("impression_id", f"display_{i}")
            contributions[tp_id] = weight
            total_weight += weight
        
        # Normalize
        if total_weight > 0:
            contributions = {tp_id: w / total_weight for tp_id, w in contributions.items()}
        
        return {
            "touchpoint_contributions": contributions,
            "confidence_score": 0.8
        }
    
    async def analyze_frequency_optimization(self, frequency_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock frequency optimization analysis"""
        return {
            "optimal_frequency": 3,
            "fatigue_point": 5,
            "recommendations": [
                "Set frequency cap to 3 per 24 hours",
                "Monitor performance metrics",
                "Consider audience segmentation"
            ],
            "confidence_score": 0.75
        }
    
    async def analyze_cross_channel_synergy(self, synergy_data: Dict[str, Any], search_insights: Optional[Dict] = None) -> Dict[str, Any]:
        """Mock cross-channel synergy analysis"""
        return {
            "synergy_score": 0.7,
            "optimization_opportunities": [
                "Coordinate messaging across channels",
                "Optimize timing between search and display",
                "Implement unified measurement"
            ],
            "recommended_strategy": "integrated_approach",
            "confidence_score": 0.8
        }