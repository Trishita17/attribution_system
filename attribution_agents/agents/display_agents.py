from typing import Dict, List, Any, Optional
from ..data.snowflake_client import SnowflakeClient
from ..data.model import DisplayInsights, AttributionResult, CreativePerformance, AdImpression, VideoInteraction
from ..llm.client import LLMClient
import logging
from datetime import datetime
from pydantic import Field
from . import display_helpers

logger = logging.getLogger(__name__)

class DisplayAttributionAgent:
    """
    Display Attribution Agent - Analyzes display and video advertising performance
    Focuses on creative optimization, frequency analysis, and cross-channel attribution
    """
    
    def __init__(self):
        self.db_client = SnowflakeClient()
        self.llm_client = LLMClient()
        self.agent_id = "display_attribution_agent"
        logger.info("Display Attribution Agent initialized")
    
    async def analyze_creative_performance(self, creative_id: str) -> Dict[str, Any]:
        """
        Analyze individual creative performance with LLM insights
        
        Args:
            creative_id: Unique creative identifier
            
        Returns:
            Dict with creative analysis and optimization recommendations
        """
        try:
            # Get creative performance data
            creative_data = await self.db_client.get_creative_performance(creative_id)
            
            if not creative_data:
                return {"error": "Creative not found", "creative_id": creative_id}
            
            # Get impression data for this creative
            impressions = await self.db_client.get_creative_impressions(creative_id)
            
            # Prepare data for LLM analysis
            analysis_data = {
                "creative_id": creative_id,
                "creative_data": creative_data,
                "impression_data": impressions,
                "performance_metrics": {
                    "ctr": creative_data.get("click_through_rate", 0),
                    "cvr": creative_data.get("conversion_rate", 0),
                    "viewability": creative_data.get("avg_viewability", 0),
                    "brand_lift": creative_data.get("brand_lift_score", 0)
                }
            }
            
            # Get LLM analysis
            llm_insights = await self.llm_client.analyze_creative_performance(analysis_data)
            
            # Process and enhance insights
            result = {
                "creative_id": creative_id,
                "performance_summary": self._summarize_creative_performance(creative_data),
                "llm_insights": llm_insights,
                "optimization_recommendations": self._generate_creative_recommendations(
                    creative_data, llm_insights
                ),
                "frequency_analysis": self._analyze_frequency_performance(creative_data),
                "competitive_position": self._assess_creative_competitiveness(creative_data)
            }
            
            logger.info(f"Creative analysis completed for {creative_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing creative performance: {str(e)}")
            return {"error": str(e), "creative_id": creative_id}
    
    async def analyze_video_engagement(self, customer_id: str) -> Dict[str, Any]:
        """
        Analyze customer's video interaction patterns
        
        Args:
            customer_id: Customer identifier
            
        Returns:
            Dict with video engagement analysis
        """
        try:
            # Get customer's video interactions
            video_data = await self.db_client.get_customer_video_interactions(customer_id)
            
            if not video_data:
                return {"customer_id": customer_id, "video_interactions": 0}
            
            # Analyze engagement patterns
            engagement_analysis = {
                "customer_id": customer_id,
                "total_videos": len(video_data),
                "avg_completion_rate": self._calculate_avg_completion_rate(video_data),
                "engagement_depth": self._analyze_engagement_depth(video_data),
                "content_preferences": self._identify_content_preferences(video_data),
                "optimal_video_length": self._determine_optimal_length(video_data),
                "drop_off_patterns": self._analyze_drop_off_patterns(video_data)
            }
            
            # Get LLM insights on engagement patterns
            llm_analysis = await self.llm_client.analyze_video_engagement(engagement_analysis)
            
            result = {
                **engagement_analysis,
                "llm_insights": llm_analysis,
                "personalization_recommendations": self._generate_video_recommendations(
                    engagement_analysis, llm_analysis
                )
            }
            
            logger.info(f"Video engagement analysis completed for {customer_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing video engagement: {str(e)}")
            return {"error": str(e), "customer_id": customer_id}
    
    async def calculate_display_attribution(self, customer_id: str, conversion_id: str) -> AttributionResult:
        """
        Calculate attribution weights for customer's display journey
        
        Args:
            customer_id: Customer identifier
            conversion_id: Conversion event identifier
            
        Returns:
            AttributionResult with display attribution weights
        """
        try:
            logger.info(f"Calculating display attribution for customer {customer_id}")
            
            # Get customer's display journey
            display_history = await self.db_client.get_customer_display_history(customer_id)
            
            if not display_history:
                return AttributionResult(
                    customer_id=customer_id,
                    query_contributions={},
                    session_contributions={},
                    total_attribution_weight=0.0,
                    confidence_score=0.0,
                    error="No display history found"
                )
            
            # Get conversion details
            conversion_data = await self.db_client.get_conversion_details(conversion_id)
            
            # Prepare journey data for LLM analysis
            journey_data = {
                "customer_id": customer_id,
                "display_touchpoints": display_history,
                "conversion": conversion_data,
                "total_touchpoints": len(display_history)
            }
            
            # Get LLM attribution analysis
            llm_attribution = await self.llm_client.analyze_display_attribution(
                journey_data, conversion_data
            )
            
            # Process attribution results
            attribution_result = self._process_display_attribution_results(
                customer_id,
                conversion_id, 
                display_history,
                llm_attribution
            )
            
            # Update touchpoints with attribution weights
            await self.update_display_attribution(attribution_result)
            
            logger.info(f"Display attribution calculation completed for {customer_id}")
            return attribution_result
            
        except Exception as e:
            logger.error(f"Error calculating display attribution: {str(e)}")
            return AttributionResult(
                customer_id=customer_id,
                query_contributions={},
                session_contributions={},
                total_attribution_weight=0.0,
                confidence_score=0.0,
                error=str(e)
            )
    
    async def optimize_frequency_capping(self, campaign_id: str) -> Dict[str, Any]:
        """
        Analyze campaign performance across frequency levels and recommend optimal capping
        
        Args:
            campaign_id: Campaign identifier
            
        Returns:
            Dict with frequency optimization recommendations
        """
        try:
            # Get campaign impression data grouped by frequency
            frequency_data = await self.db_client.get_campaign_frequency_data(campaign_id)
            
            if not frequency_data:
                return {"error": "No frequency data found", "campaign_id": campaign_id}
            
            # Analyze performance by frequency level
            frequency_analysis = {
                "campaign_id": campaign_id,
                "frequency_performance": self._analyze_frequency_performance_curve(frequency_data),
                "optimal_frequency": self._determine_optimal_frequency(frequency_data),
                "fatigue_point": self._identify_ad_fatigue_point(frequency_data),
                "current_settings": await self.db_client.get_campaign_frequency_settings(campaign_id)
            }
            
            # Get LLM recommendations
            llm_recommendations = await self.llm_client.analyze_frequency_optimization(
                frequency_analysis
            )
            
            result = {
                **frequency_analysis,
                "llm_recommendations": llm_recommendations,
                "implementation_plan": self._create_frequency_optimization_plan(
                    frequency_analysis, llm_recommendations
                )
            }
            
            logger.info(f"Frequency optimization analysis completed for campaign {campaign_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error optimizing frequency capping: {str(e)}")
            return {"error": str(e), "campaign_id": campaign_id}
    
    async def analyze_cross_channel_synergy(
        self, 
        customer_id: str, 
        search_insights: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Analyze how display advertising works with search behavior
        
        Args:
            customer_id: Customer identifier
            search_insights: Optional search agent insights
            
        Returns:
            Dict with cross-channel analysis
        """
        try:
            # Get display and search touchpoints
            display_touchpoints = await self.db_client.get_customer_display_history(customer_id)
            search_touchpoints = await self.db_client.get_customer_search_history(customer_id)
            
            if not display_touchpoints or not search_touchpoints:
                return {
                    "customer_id": customer_id,
                    "analysis": "insufficient_data",
                    "display_count": len(display_touchpoints or []),
                    "search_count": len(search_touchpoints or [])
                }
            
            # Analyze interaction patterns
            synergy_analysis = {
                "customer_id": customer_id,
                "channel_sequence": self._analyze_channel_sequence(
                    display_touchpoints, search_touchpoints
                ),
                "interaction_effects": self._measure_interaction_effects(
                    display_touchpoints, search_touchpoints
                ),
                "attribution_overlap": self._calculate_attribution_overlap(
                    display_touchpoints, search_touchpoints
                ),
                "optimal_timing": self._determine_optimal_channel_timing(
                    display_touchpoints, search_touchpoints
                )
            }
            
            # Get LLM insights on cross-channel behavior
            llm_analysis = await self.llm_client.analyze_cross_channel_synergy(
                synergy_analysis, search_insights
            )
            
            result = {
                **synergy_analysis,
                "llm_insights": llm_analysis,
                "optimization_opportunities": self._identify_cross_channel_opportunities(
                    synergy_analysis, llm_analysis
                )
            }
            
            logger.info(f"Cross-channel analysis completed for {customer_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing cross-channel synergy: {str(e)}")
            return {"error": str(e), "customer_id": customer_id}
    
    async def get_display_insights(self, customer_id: str) -> DisplayInsights:
        """
        Generate comprehensive display advertising insights for a customer
        
        Args:
            customer_id: Customer identifier
            
        Returns:
            DisplayInsights object with comprehensive analysis
        """
        try:
            # Get all display data
            display_history = await self.db_client.get_customer_display_history(customer_id)
            video_interactions = await self.db_client.get_customer_video_interactions(customer_id)
            
            # Calculate insights
            insights = DisplayInsights(
                customer_id=customer_id,
                total_impressions=len(display_history),
                total_video_interactions=len(video_interactions),
                avg_viewability=self._calculate_avg_viewability(display_history),
                preferred_ad_formats=self._identify_preferred_formats(display_history),
                optimal_frequency=self._calculate_customer_optimal_frequency(display_history),
                brand_affinity_score=self._calculate_brand_affinity(display_history),
                creative_engagement_patterns=self._analyze_creative_engagement(display_history),
                cross_device_behavior=self._analyze_cross_device_patterns(display_history)
            )
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating display insights: {str(e)}")
            return DisplayInsights(
                customer_id=customer_id,
                error=str(e)
            )
    
    async def update_display_attribution(self, attribution_results: AttributionResult):
        """Update display touchpoints with calculated attribution weights"""
        try:
            for touchpoint_id, weight in attribution_results.query_contributions.items():
                await self.db_client.update_touchpoint_attribution_weight(touchpoint_id, weight)
                
            logger.info(f"Updated attribution weights for {len(attribution_results.query_contributions)} display touchpoints")
            
        except Exception as e:
            logger.error(f"Error updating display attribution: {str(e)}")
    
    # =============================================================================
    # HELPER METHODS - Internal Processing Logic
    # =============================================================================
    
    def _summarize_creative_performance(self, creative_data: Dict) -> Dict[str, Any]:
        """Summarize key creative performance metrics"""
        return {
            "performance_tier": self._classify_performance_tier(creative_data),
            "key_strengths": self._identify_creative_strengths(creative_data),
            "improvement_areas": self._identify_improvement_areas(creative_data),
            "benchmark_comparison": self._compare_to_benchmarks(creative_data)
        }
    
    def _classify_performance_tier(self, creative_data: Dict) -> str:
        """Classify creative into performance tiers"""
        ctr = creative_data.get("click_through_rate", 0)
        cvr = creative_data.get("conversion_rate", 0)
        
        if ctr >= 0.05 and cvr >= 0.03:
            return "top_performer"
        elif ctr >= 0.03 or cvr >= 0.02:
            return "good_performer" 
        elif ctr >= 0.02 or cvr >= 0.01:
            return "average_performer"
        else:
            return "underperformer"
    
    def _generate_creative_recommendations(
        self, 
        creative_data: Dict, 
        llm_insights: Dict
    ) -> List[str]:
        """Generate actionable creative optimization recommendations"""
        recommendations = []
        
        ctr = creative_data.get("click_through_rate", 0)
        cvr = creative_data.get("conversion_rate", 0)
        viewability = creative_data.get("avg_viewability", 0)
        
        if ctr < 0.025:
            recommendations.append("Improve creative engagement - test different hooks or CTAs")
        
        if cvr < 0.015:
            recommendations.append("Optimize landing page alignment with creative messaging")
            
        if viewability < 0.70:
            recommendations.append("Review placement strategy - focus on above-fold positions")
        
        # Add LLM-specific recommendations
        if llm_insights.get("recommendations"):
            recommendations.extend(llm_insights["recommendations"])
        
        return recommendations
    
    def _analyze_frequency_performance(self, creative_data: Dict) -> Dict[str, Any]:
        """Analyze performance across different frequency levels"""
        frequency_data = creative_data.get("performance_by_frequency", {})
        
        if not frequency_data:
            return {"analysis": "no_frequency_data"}
        
        return {
            "optimal_frequency": self._find_optimal_frequency(frequency_data),
            "fatigue_point": self._find_fatigue_point(frequency_data),
            "frequency_curve": frequency_data
        }
    
    def _find_optimal_frequency(self, frequency_data: Dict) -> int:
        """Find the frequency level with best performance"""
        if not frequency_data:
            return 2  # Default
        
        best_freq = 1
        best_performance = 0
        
        for freq, metrics in frequency_data.items():
            if isinstance(metrics, dict):
                # Combine CTR and CVR for overall performance score
                performance = (metrics.get("ctr", 0) * 0.4 + 
                              metrics.get("cvr", 0) * 0.6)
                if performance > best_performance:
                    best_performance = performance
                    best_freq = int(freq.replace("freq_", "").replace("+", ""))
        
        return best_freq
    
    def _calculate_avg_completion_rate(self, video_data: List[Dict]) -> float:
        """Calculate average video completion rate"""
        if not video_data:
            return 0.0
        
        completion_rates = [v.get("completion_rate", 0) for v in video_data]
        return sum(completion_rates) / len(completion_rates)
    
    def _analyze_engagement_depth(self, video_data: List[Dict]) -> Dict[str, Any]:
        """Analyze depth of video engagement"""
        if not video_data:
            return {"depth": "no_data"}
        
        high_engagement = sum(1 for v in video_data if v.get("completion_rate", 0) >= 0.75)
        total_videos = len(video_data)
        
        return {
            "high_engagement_rate": high_engagement / total_videos if total_videos > 0 else 0,
            "avg_interactions_per_video": self._calculate_avg_interactions(video_data),
            "engagement_tier": "high" if high_engagement / total_videos > 0.6 else "medium" if high_engagement / total_videos > 0.3 else "low"
        }
    
    def _calculate_avg_interactions(self, video_data: List[Dict]) -> float:
        """Calculate average interactions per video"""
        if not video_data:
            return 0.0
        
        total_interactions = 0
        for video in video_data:
            engagement_points = video.get("engagement_points", [])
            if isinstance(engagement_points, list):
                total_interactions += len(engagement_points)
        
        return total_interactions / len(video_data)
    
    def _process_display_attribution_results(
        self,
        customer_id: str,
        conversion_id: str,
        display_history: List[Dict],
        llm_attribution: Dict[str, Any]
    ) -> AttributionResult:
        """Process and validate display attribution results"""
        
        # Extract touchpoint contributions from LLM response
        touchpoint_contributions = llm_attribution.get("touchpoint_contributions", {})
        
        # If LLM failed, use fallback attribution
        if not touchpoint_contributions or "error" in llm_attribution:
            touchpoint_contributions = self._calculate_fallback_display_attribution(display_history)
        
        # Normalize weights
        touchpoint_contributions = self._normalize_attribution_weights(touchpoint_contributions)
        
        # Calculate confidence score
        confidence_score = self._calculate_display_attribution_confidence(llm_attribution, display_history)
        
        return AttributionResult(
            customer_id=customer_id,
            conversion_id=conversion_id,
            query_contributions=touchpoint_contributions,  # Reusing field name for consistency
            session_contributions={},
            total_attribution_weight=sum(touchpoint_contributions.values()),
            confidence_score=confidence_score,
            model_version="display_agent_v1.0",
            attribution_method="llm_enhanced" if not llm_attribution.get("error") else "fallback"
        )
    
    def _calculate_fallback_display_attribution(self, display_history: List[Dict]) -> Dict[str, float]:
        """Simple viewability-weighted attribution as fallback"""
        if not display_history:
            return {}
        
        # Weight by viewability and recency
        attributions = {}
        total_weight = 0
        
        for i, touchpoint in enumerate(display_history):
            viewability = touchpoint.get("viewability_score", 0.5)
            recency_weight = (i + 1) / len(display_history)  # More recent = higher weight
            weight = viewability * recency_weight
            
            touchpoint_id = touchpoint.get("impression_id", f'display_{i}')
            attributions[touchpoint_id] = weight
            total_weight += weight
        
        # Normalize
        if total_weight > 0:
            return {tid: weight / total_weight for tid, weight in attributions.items()}
        
        return attributions
    
    def _normalize_attribution_weights(self, weights: Dict[str, float]) -> Dict[str, float]:
        """Ensure attribution weights sum to 1.0"""
        if not weights:
            return {}
        
        total_weight = sum(weights.values())
        
        if total_weight == 0:
            equal_weight = 1.0 / len(weights)
            return {touchpoint_id: equal_weight for touchpoint_id in weights.keys()}
        
        if abs(total_weight - 1.0) > 0.01:
            return {touchpoint_id: weight / total_weight for touchpoint_id, weight in weights.items()}
        
        return weights
    
    def _calculate_display_attribution_confidence(
        self, 
        llm_attribution: Dict[str, Any], 
        display_history: List[Dict]
    ) -> float:
        """Calculate confidence score for display attribution"""
        base_confidence = 0.5
        
        # Boost if LLM succeeded
        if "error" not in llm_attribution:
            base_confidence += 0.25
        
        # Boost based on data quality
        if len(display_history) >= 2:
            base_confidence += 0.15
        
        # Boost if we have viewability data
        viewability_data = sum(1 for t in display_history if t.get("viewability_score", 0) > 0)
        if viewability_data / len(display_history) > 0.8:
            base_confidence += 0.1
        
        return min(base_confidence, 1.0)
    
    def _analyze_channel_sequence(
        self, 
        display_touchpoints: List[Dict], 
        search_touchpoints: List[Dict]
    ) -> Dict[str, Any]:
        """Analyze the sequence of search and display interactions"""
        # Combine and sort by timestamp
        all_touchpoints = []
        
        for tp in display_touchpoints:
            all_touchpoints.append({
                "type": "display",
                "timestamp": tp.get("timestamp"),
                "data": tp
            })
        
        for tp in search_touchpoints:
            all_touchpoints.append({
                "type": "search", 
                "timestamp": tp.get("timestamp"),
                "data": tp
            })
        
        # Sort by timestamp
        all_touchpoints.sort(key=lambda x: x.get("timestamp", ""))
        
        # Analyze sequence patterns
        sequence = [tp["type"] for tp in all_touchpoints]
        
        return {
            "full_sequence": sequence,
            "sequence_pattern": self._classify_sequence_pattern(sequence),
            "channel_transitions": self._count_channel_transitions(sequence),
            "dominant_channel": self._identify_dominant_channel(sequence)
        }
    
    def _classify_sequence_pattern(self, sequence: List[str]) -> str:
        """Classify the customer's channel interaction pattern"""
        if not sequence:
            return "no_pattern"
        
        search_count = sequence.count("search")
        display_count = sequence.count("display")
        
        if sequence[0] == "display" and sequence[-1] == "search":
            return "display_to_search"
        elif sequence[0] == "search" and sequence[-1] == "display":
            return "search_to_display" 
        elif search_count > display_count * 2:
            return "search_dominant"
        elif display_count > search_count * 2:
            return "display_dominant"
        else:
            return "balanced_interaction"
    
    def _calculate_avg_viewability(self, display_history: List[Dict]) -> float:
        """Calculate average viewability score"""
        if not display_history:
            return 0.0
        
        viewability_scores = [
            d.get("viewability_score", 0) for d in display_history 
            if d.get("viewability_score") is not None
        ]
        
        if not viewability_scores:
            return 0.0
        
        return sum(viewability_scores) / len(viewability_scores)
    
    # Delegate to helper methods
    def _identify_creative_strengths(self, creative_data: Dict) -> List[str]:
        return display_helpers._identify_creative_strengths(creative_data)
    
    def _identify_improvement_areas(self, creative_data: Dict) -> List[str]:
        return display_helpers._identify_improvement_areas(creative_data)
    
    def _compare_to_benchmarks(self, creative_data: Dict) -> Dict[str, str]:
        return display_helpers._compare_to_benchmarks(creative_data)
    
    def _assess_creative_competitiveness(self, creative_data: Dict) -> Dict[str, Any]:
        return display_helpers._assess_creative_competitiveness(creative_data)
    
    def _find_fatigue_point(self, frequency_data: Dict) -> int:
        return display_helpers._find_fatigue_point(frequency_data)
    
    def _identify_content_preferences(self, video_data: List[Dict]) -> Dict[str, Any]:
        return display_helpers._identify_content_preferences(video_data)
    
    def _determine_optimal_length(self, video_data: List[Dict]) -> int:
        return display_helpers._determine_optimal_length(video_data)
    
    def _analyze_drop_off_patterns(self, video_data: List[Dict]) -> Dict[str, Any]:
        return display_helpers._analyze_drop_off_patterns(video_data)
    
    def _generate_video_recommendations(self, engagement_analysis: Dict, llm_analysis: Dict) -> List[str]:
        return display_helpers._generate_video_recommendations(engagement_analysis, llm_analysis)
    
    def _identify_preferred_formats(self, display_history: List[Dict]) -> List[str]:
        return display_helpers._identify_preferred_formats(display_history)
    
    def _calculate_customer_optimal_frequency(self, display_history: List[Dict]) -> int:
        return display_helpers._calculate_customer_optimal_frequency(display_history)
    
    def _calculate_brand_affinity(self, display_history: List[Dict]) -> float:
        return display_helpers._calculate_brand_affinity(display_history)
    
    def _analyze_creative_engagement(self, display_history: List[Dict]) -> Dict[str, Any]:
        return display_helpers._analyze_creative_engagement(display_history)
    
    def _analyze_cross_device_patterns(self, display_history: List[Dict]) -> Dict[str, Any]:
        return display_helpers._analyze_cross_device_patterns(display_history)
    
    def _count_channel_transitions(self, sequence: List[str]) -> Dict[str, int]:
        return display_helpers._count_channel_transitions(sequence)
    
    def _identify_dominant_channel(self, sequence: List[str]) -> str:
        return display_helpers._identify_dominant_channel(sequence)
    
    def _measure_interaction_effects(self, display_touchpoints: List[Dict], search_touchpoints: List[Dict]) -> Dict[str, Any]:
        return display_helpers._measure_interaction_effects(display_touchpoints, search_touchpoints)
    
    def _calculate_attribution_overlap(self, display_touchpoints: List[Dict], search_touchpoints: List[Dict]) -> float:
        return display_helpers._calculate_attribution_overlap(display_touchpoints, search_touchpoints)
    
    def _determine_optimal_channel_timing(self, display_touchpoints: List[Dict], search_touchpoints: List[Dict]) -> Dict[str, str]:
        return display_helpers._determine_optimal_channel_timing(display_touchpoints, search_touchpoints)
    
    def _identify_cross_channel_opportunities(self, synergy_analysis: Dict, llm_analysis: Dict) -> List[str]:
        return display_helpers._identify_cross_channel_opportunities(synergy_analysis, llm_analysis)