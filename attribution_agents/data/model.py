from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class SearchQuery(BaseModel):
    query_id: str
    customer_id: str
    session_id: Optional[str]
    query_text: str
    query_type: Optional[str]
    intent_classification: Optional[Dict[str, Any]]
    intent_confidence: Optional[float]
    timestamp: datetime
    query_sequence_position: Optional[int]
    funnel_stage: Optional[str]

class SearchSession(BaseModel):
    session_id: str
    customer_id: str
    start_time: datetime
    end_time: Optional[datetime]
    total_queries: int
    unique_intent_types: Optional[List[str]]
    session_progression: Optional[Dict[str, Any]]
    exit_point: Optional[str]
    session_outcome: Optional[str]
    session_value: Optional[float]

class AttributionResult(BaseModel):
    customer_id: str
    conversion_id: Optional[str] = None
    query_contributions: Dict[str, float]
    session_contributions: Dict[str, float]
    total_attribution_weight: float
    confidence_score: float
    model_version: Optional[str] = None
    attribution_method: Optional[str] = None
    error: Optional[str] = None

class AdImpression(BaseModel):
    impression_id: str
    customer_id: str
    creative_id: str
    campaign_id: Optional[str] = None
    placement_id: Optional[str] = None
    ad_format: str  # banner, video, native, rich_media
    viewability_score: float = 0.0
    view_duration_seconds: Optional[int] = None
    interaction_data: Optional[Dict[str, Any]] = None
    timestamp: datetime
    frequency_cap_count: int = 1
    cost: float = 0.0

class VideoInteraction(BaseModel):
    interaction_id: str
    customer_id: str
    video_id: str
    campaign_id: Optional[str] = None
    video_duration_seconds: int
    completion_rate: float = 0.0
    quartile_completions: List[int] = Field(default_factory=list)  # [25, 50, 75, 100]
    engagement_points: List[Dict[str, Any]] = Field(default_factory=list)
    drop_off_time: Optional[int] = None
    interaction_type: str  # ad_view, organic_view, social_view
    timestamp: datetime
    video_metadata: Optional[Dict[str, Any]] = None

class CreativePerformance(BaseModel):
    creative_id: str
    creative_name: str
    creative_type: str  # image, video, carousel, dynamic
    campaign_id: Optional[str] = None
    total_impressions: int = 0
    unique_viewers: int = 0
    avg_viewability: float = 0.0
    click_through_rate: float = 0.0
    conversion_rate: float = 0.0
    brand_lift_score: float = 0.0
    creative_metadata: Optional[Dict[str, Any]] = None
    performance_by_frequency: Optional[Dict[str, Any]] = None
    last_updated: Optional[datetime] = None

class DisplayInsights(BaseModel):
    """
    Generated insights about customer display advertising behavior
    """
    customer_id: str
    total_impressions: int = 0
    total_video_interactions: int = 0
    avg_viewability: float = 0.0
    preferred_ad_formats: List[str] = Field(default_factory=list)
    optimal_frequency: int = 2
    brand_affinity_score: float = 0.0
    creative_engagement_patterns: Dict[str, Any] = Field(default_factory=dict)
    cross_device_behavior: Dict[str, Any] = Field(default_factory=dict)
    video_engagement_tier: str = "unknown"  # high, medium, low
    frequency_tolerance: int = 3
    preferred_placements: List[str] = Field(default_factory=list)
    error: Optional[str] = None

class FrequencyAnalysis(BaseModel):
    """
    Analysis of ad frequency performance and optimization
    """
    campaign_id: str
    current_frequency_cap: int = 3
    optimal_frequency: int = 2
    fatigue_point: int = 4
    performance_by_frequency: Dict[str, Dict[str, float]] = Field(default_factory=dict)
    frequency_recommendations: List[str] = Field(default_factory=list)
    estimated_impact: Optional[Dict[str, float]] = None

class CrossChannelAnalysis(BaseModel):
    """
    Analysis of cross-channel behavior between search and display
    """
    customer_id: str
    channel_sequence: List[str] = Field(default_factory=list)
    sequence_pattern: str = "unknown"
    interaction_effects: Dict[str, Any] = Field(default_factory=dict)
    attribution_overlap: float = 0.0
    synergy_score: float = 0.0
    optimization_opportunities: List[str] = Field(default_factory=list)
    recommended_strategy: Optional[str] = None

class DisplayAttributionResult(BaseModel):
    """
    Display-specific attribution result
    """
    customer_id: str
    conversion_id: Optional[str] = None
    impression_contributions: Dict[str, float] = Field(default_factory=dict)
    creative_contributions: Dict[str, float] = Field(default_factory=dict)
    campaign_contributions: Dict[str, float] = Field(default_factory=dict)
    placement_contributions: Dict[str, float] = Field(default_factory=dict)
    total_attribution_weight: float = 0.0
    confidence_score: float = 0.0
    viewability_impact: float = 0.0
    frequency_impact: float = 0.0
    attribution_method: str = "display_enhanced"
    error: Optional[str] = None