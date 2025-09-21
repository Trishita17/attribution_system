"""
Multi-Agent Attribution Manager
Coordinates between Search and Display Attribution Agents
"""
from typing import Dict, List, Any, Optional
from .agents.search_agents import SearchAttributionAgent
from .agents.display_agents import DisplayAttributionAgent
from .data.model import AttributionResult
import logging
import asyncio

logger = logging.getLogger(__name__)

class MultiAgentAttributionManager:
    """
    Manages coordination between Search and Display Attribution Agents
    Provides unified interface for multi-channel attribution analysis
    """
    
    def __init__(self):
        self.search_agent = SearchAttributionAgent()
        self.display_agent = DisplayAttributionAgent()
        self.manager_id = "multi_agent_attribution_manager"
        logger.info("Multi-Agent Attribution Manager initialized")
    
    async def calculate_unified_attribution(
        self, 
        customer_id: str, 
        conversion_id: str
    ) -> Dict[str, Any]:
        """
        Calculate attribution across both search and display channels
        
        Args:
            customer_id: Customer identifier
            conversion_id: Conversion event identifier
            
        Returns:
            Dict with unified attribution results
        """
        try:
            logger.info(f"Calculating unified attribution for customer {customer_id}")
            
            # Run both agents in parallel
            search_task = self.search_agent.calculate_attribution_weights(customer_id, conversion_id)
            display_task = self.display_agent.calculate_display_attribution(customer_id, conversion_id)
            
            search_result, display_result = await asyncio.gather(
                search_task, display_task, return_exceptions=True
            )
            
            # Handle exceptions
            if isinstance(search_result, Exception):
                logger.error(f"Search attribution failed: {str(search_result)}")
                search_result = {"error": str(search_result)}
            
            if isinstance(display_result, Exception):
                logger.error(f"Display attribution failed: {str(display_result)}")
                display_result = AttributionResult(
                    customer_id=customer_id,
                    query_contributions={},
                    session_contributions={},
                    total_attribution_weight=0.0,
                    confidence_score=0.0,
                    error=str(display_result)
                )
            
            # Combine results
            unified_result = self._combine_attribution_results(
                customer_id, conversion_id, search_result, display_result
            )
            
            logger.info(f"Unified attribution completed for customer {customer_id}")
            return unified_result
            
        except Exception as e:
            logger.error(f"Error in unified attribution calculation: {str(e)}")
            return {
                "customer_id": customer_id,
                "conversion_id": conversion_id,
                "error": str(e),
                "search_attribution": {},
                "display_attribution": {},
                "unified_attribution": {}
            }
    
    async def get_comprehensive_insights(self, customer_id: str) -> Dict[str, Any]:
        """
        Get comprehensive insights from both agents
        
        Args:
            customer_id: Customer identifier
            
        Returns:
            Dict with insights from both channels
        """
        try:
            logger.info(f"Getting comprehensive insights for customer {customer_id}")
            
            # Get insights from both agents
            search_insights_task = self.search_agent.get_search_insights(customer_id)
            display_insights_task = self.display_agent.get_display_insights(customer_id)
            
            search_insights, display_insights = await asyncio.gather(
                search_insights_task, display_insights_task, return_exceptions=True
            )
            
            # Handle exceptions
            if isinstance(search_insights, Exception):
                search_insights = {"error": str(search_insights)}
            
            if isinstance(display_insights, Exception):
                display_insights = {"error": str(display_insights)}
            
            # Analyze cross-channel synergy
            cross_channel_analysis = await self.display_agent.analyze_cross_channel_synergy(
                customer_id, search_insights if not isinstance(search_insights, dict) or "error" not in search_insights else None
            )
            
            return {
                "customer_id": customer_id,
                "search_insights": search_insights,
                "display_insights": display_insights,
                "cross_channel_analysis": cross_channel_analysis,
                "unified_recommendations": self._generate_unified_recommendations(
                    search_insights, display_insights, cross_channel_analysis
                )
            }
            
        except Exception as e:
            logger.error(f"Error getting comprehensive insights: {str(e)}")
            return {
                "customer_id": customer_id,
                "error": str(e)
            }
    
    async def optimize_cross_channel_strategy(
        self, 
        customer_id: str,
        optimization_goals: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate cross-channel optimization recommendations
        
        Args:
            customer_id: Customer identifier
            optimization_goals: List of optimization objectives
            
        Returns:
            Dict with optimization strategy
        """
        try:
            # Get comprehensive insights first
            insights = await self.get_comprehensive_insights(customer_id)
            
            if "error" in insights:
                return insights
            
            # Generate optimization strategy
            strategy = self._create_optimization_strategy(insights, optimization_goals or [])
            
            return {
                "customer_id": customer_id,
                "optimization_strategy": strategy,
                "implementation_priority": self._prioritize_optimizations(strategy),
                "expected_impact": self._estimate_optimization_impact(strategy, insights)
            }
            
        except Exception as e:
            logger.error(f"Error optimizing cross-channel strategy: {str(e)}")
            return {
                "customer_id": customer_id,
                "error": str(e)
            }
    
    def _combine_attribution_results(
        self,
        customer_id: str,
        conversion_id: str,
        search_result: Dict[str, Any],
        display_result: AttributionResult
    ) -> Dict[str, Any]:
        """Combine search and display attribution results"""
        
        # Extract search contributions
        search_contributions = {}
        if isinstance(search_result, dict) and "query_contributions" in search_result:
            search_contributions = search_result["query_contributions"]
        
        # Extract display contributions
        display_contributions = {}
        if hasattr(display_result, 'query_contributions'):
            display_contributions = display_result.query_contributions
        
        # Calculate channel weights (simple approach - can be enhanced with ML)
        total_search_touchpoints = len(search_contributions)
        total_display_touchpoints = len(display_contributions)
        total_touchpoints = total_search_touchpoints + total_display_touchpoints
        
        if total_touchpoints == 0:
            search_weight = 0.5
            display_weight = 0.5
        else:
            search_weight = total_search_touchpoints / total_touchpoints
            display_weight = total_display_touchpoints / total_touchpoints
        
        # Normalize contributions within each channel
        normalized_search = {
            f"search_{k}": v * search_weight 
            for k, v in search_contributions.items()
        }
        normalized_display = {
            f"display_{k}": v * display_weight 
            for k, v in display_contributions.items()
        }
        
        # Combine all contributions
        unified_contributions = {**normalized_search, **normalized_display}
        
        return {
            "customer_id": customer_id,
            "conversion_id": conversion_id,
            "search_attribution": {
                "contributions": search_contributions,
                "total_weight": search_weight,
                "confidence": search_result.get("confidence_score", 0.0) if isinstance(search_result, dict) else 0.0
            },
            "display_attribution": {
                "contributions": display_contributions,
                "total_weight": display_weight,
                "confidence": display_result.confidence_score if hasattr(display_result, 'confidence_score') else 0.0
            },
            "unified_attribution": {
                "contributions": unified_contributions,
                "total_weight": sum(unified_contributions.values()),
                "channel_weights": {
                    "search": search_weight,
                    "display": display_weight
                }
            }
        }
    
    def _generate_unified_recommendations(
        self,
        search_insights: Dict[str, Any],
        display_insights: Any,
        cross_channel_analysis: Dict[str, Any]
    ) -> List[str]:
        """Generate unified optimization recommendations"""
        recommendations = []
        
        # Search-based recommendations
        if isinstance(search_insights, dict) and "total_searches" in search_insights:
            if search_insights["total_searches"] < 5:
                recommendations.append("Increase search marketing investment to capture more customer touchpoints")
        
        # Display-based recommendations
        if hasattr(display_insights, 'total_impressions'):
            if display_insights.total_impressions < 10:
                recommendations.append("Expand display advertising reach to increase brand awareness")
            
            if hasattr(display_insights, 'avg_viewability') and display_insights.avg_viewability < 0.7:
                recommendations.append("Optimize display placements for better viewability")
        
        # Cross-channel recommendations
        if isinstance(cross_channel_analysis, dict):
            if cross_channel_analysis.get("sequence_pattern") == "display_to_search":
                recommendations.append("Display ads are driving search behavior - increase display investment")
            elif cross_channel_analysis.get("sequence_pattern") == "search_to_display":
                recommendations.append("Search is driving display engagement - optimize display retargeting")
        
        return recommendations
    
    def _create_optimization_strategy(
        self,
        insights: Dict[str, Any],
        goals: List[str]
    ) -> Dict[str, Any]:
        """Create comprehensive optimization strategy"""
        return {
            "search_optimizations": self._get_search_optimizations(insights.get("search_insights", {})),
            "display_optimizations": self._get_display_optimizations(insights.get("display_insights", {})),
            "cross_channel_optimizations": self._get_cross_channel_optimizations(
                insights.get("cross_channel_analysis", {})
            ),
            "budget_allocation": self._recommend_budget_allocation(insights),
            "timing_strategy": self._recommend_timing_strategy(insights)
        }
    
    def _get_search_optimizations(self, search_insights: Dict[str, Any]) -> List[str]:
        """Get search-specific optimizations"""
        optimizations = []
        
        if search_insights.get("total_searches", 0) > 0:
            search_types = search_insights.get("search_types", [])
            if "transactional" not in search_types:
                optimizations.append("Target more transactional keywords")
            
            funnel_stages = search_insights.get("funnel_stages", [])
            if "decision" not in funnel_stages:
                optimizations.append("Add decision-stage keyword targeting")
        
        return optimizations
    
    def _get_display_optimizations(self, display_insights: Any) -> List[str]:
        """Get display-specific optimizations"""
        optimizations = []
        
        if hasattr(display_insights, 'avg_viewability'):
            if display_insights.avg_viewability < 0.7:
                optimizations.append("Improve ad placement for better viewability")
        
        if hasattr(display_insights, 'optimal_frequency'):
            optimizations.append(f"Optimize frequency capping to {display_insights.optimal_frequency}")
        
        return optimizations
    
    def _get_cross_channel_optimizations(self, cross_channel_analysis: Dict[str, Any]) -> List[str]:
        """Get cross-channel optimizations"""
        optimizations = []
        
        sequence_pattern = cross_channel_analysis.get("sequence_pattern", "unknown")
        if sequence_pattern == "display_to_search":
            optimizations.append("Increase display investment to drive more search activity")
        elif sequence_pattern == "search_to_display":
            optimizations.append("Enhance display retargeting for search users")
        
        return optimizations
    
    def _recommend_budget_allocation(self, insights: Dict[str, Any]) -> Dict[str, float]:
        """Recommend budget allocation between channels"""
        # Simple allocation based on performance indicators
        search_score = self._calculate_channel_score(insights.get("search_insights", {}), "search")
        display_score = self._calculate_channel_score(insights.get("display_insights", {}), "display")
        
        total_score = search_score + display_score
        if total_score == 0:
            return {"search": 0.5, "display": 0.5}
        
        return {
            "search": search_score / total_score,
            "display": display_score / total_score
        }
    
    def _calculate_channel_score(self, insights: Any, channel_type: str) -> float:
        """Calculate performance score for a channel"""
        if channel_type == "search":
            if isinstance(insights, dict):
                return min(insights.get("total_searches", 0) / 10.0, 1.0)
        elif channel_type == "display":
            if hasattr(insights, 'total_impressions'):
                return min(insights.total_impressions / 50.0, 1.0)
        
        return 0.5  # Default score
    
    def _recommend_timing_strategy(self, insights: Dict[str, Any]) -> Dict[str, str]:
        """Recommend timing strategy for cross-channel coordination"""
        return {
            "search_timing": "Continuous with peak during decision stage",
            "display_timing": "Front-load for awareness, retarget for conversion",
            "coordination": "Use display to drive search, then retarget searchers"
        }
    
    def _prioritize_optimizations(self, strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prioritize optimization recommendations"""
        priorities = []
        
        # High priority: Cross-channel optimizations
        for opt in strategy.get("cross_channel_optimizations", []):
            priorities.append({"optimization": opt, "priority": "high", "channel": "cross_channel"})
        
        # Medium priority: Channel-specific optimizations
        for opt in strategy.get("search_optimizations", []):
            priorities.append({"optimization": opt, "priority": "medium", "channel": "search"})
        
        for opt in strategy.get("display_optimizations", []):
            priorities.append({"optimization": opt, "priority": "medium", "channel": "display"})
        
        return priorities
    
    def _estimate_optimization_impact(
        self, 
        strategy: Dict[str, Any], 
        insights: Dict[str, Any]
    ) -> Dict[str, str]:
        """Estimate impact of optimization strategy"""
        return {
            "attribution_accuracy": "15-25% improvement expected",
            "cross_channel_synergy": "20-30% lift in combined performance",
            "budget_efficiency": "10-20% improvement in ROAS",
            "customer_journey_optimization": "Enhanced touchpoint effectiveness"
        }