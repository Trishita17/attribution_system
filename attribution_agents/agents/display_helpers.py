"""
Helper methods for Display Attribution Agent
"""
from typing import Dict, List, Any

def _identify_creative_strengths(creative_data: Dict) -> List[str]:
    ctr = creative_data.get("click_through_rate", 0)
    return ["High engagement"] if ctr > 0.03 else ["Baseline performance"]

def _identify_improvement_areas(creative_data: Dict) -> List[str]:
    ctr = creative_data.get("click_through_rate", 0)
    return ["Increase engagement"] if ctr < 0.025 else ["Maintain performance"]

def _compare_to_benchmarks(creative_data: Dict) -> Dict[str, str]:
    ctr = creative_data.get("click_through_rate", 0)
    return {"ctr_vs_benchmark": "above" if ctr > 0.03 else "below"}

def _assess_creative_competitiveness(creative_data: Dict) -> Dict[str, Any]:
    ctr = creative_data.get("click_through_rate", 0)
    cvr = creative_data.get("conversion_rate", 0)
    if ctr >= 0.05 and cvr >= 0.03:
        tier = "top_performer"
    elif ctr >= 0.03 or cvr >= 0.02:
        tier = "good_performer"
    else:
        tier = "underperformer"
    return {"competitive_position": tier}

def _find_fatigue_point(frequency_data: Dict) -> int:
    return 4

def _identify_content_preferences(video_data: List[Dict]) -> Dict[str, Any]:
    return {"preferred_length": 30}

def _determine_optimal_length(video_data: List[Dict]) -> int:
    return 30

def _analyze_drop_off_patterns(video_data: List[Dict]) -> Dict[str, Any]:
    return {"common_drop_off": "15s"}

def _generate_video_recommendations(engagement_analysis: Dict, llm_analysis: Dict) -> List[str]:
    return ["Optimize video length"]

def _identify_preferred_formats(display_history: List[Dict]) -> List[str]:
    return ["banner"] if not display_history else list(set(item.get("ad_format", "banner") for item in display_history))

def _calculate_customer_optimal_frequency(display_history: List[Dict]) -> int:
    return 2

def _calculate_brand_affinity(display_history: List[Dict]) -> float:
    return 0.7

def _analyze_creative_engagement(display_history: List[Dict]) -> Dict[str, Any]:
    return {"engagement_score": 0.7}

def _analyze_cross_device_patterns(display_history: List[Dict]) -> Dict[str, Any]:
    return {"device_diversity": "medium"}

def _count_channel_transitions(sequence: List[str]) -> Dict[str, int]:
    transitions = {}
    for i in range(len(sequence) - 1):
        key = f"{sequence[i]}_to_{sequence[i+1]}"
        transitions[key] = transitions.get(key, 0) + 1
    return transitions

def _identify_dominant_channel(sequence: List[str]) -> str:
    return max(set(sequence), key=sequence.count) if sequence else "unknown"

def _measure_interaction_effects(display_touchpoints: List[Dict], search_touchpoints: List[Dict]) -> Dict[str, Any]:
    return {"synergy_detected": bool(display_touchpoints and search_touchpoints)}

def _calculate_attribution_overlap(display_touchpoints: List[Dict], search_touchpoints: List[Dict]) -> float:
    return 0.3 if display_touchpoints and search_touchpoints else 0.0

def _determine_optimal_channel_timing(display_touchpoints: List[Dict], search_touchpoints: List[Dict]) -> Dict[str, str]:
    return {"display_timing": "awareness"}

def _identify_cross_channel_opportunities(synergy_analysis: Dict, llm_analysis: Dict) -> List[str]:
    return ["Coordinate messaging"]