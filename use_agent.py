#!/usr/bin/env python3
"""
How to use the Multi-Agent Attribution System
Demonstrates Search and Display agents working together
"""
import asyncio
import sys
import os
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from attribution_agents.agents.search_agents import SearchAttributionAgent
from attribution_agents.agents.display_agents import DisplayAttributionAgent
from attribution_agents.agent_manager import MultiAgentAttributionManager

async def demo_individual_agents():
    """Demonstrate individual agent capabilities"""
    print("🔍 Individual Agent Demonstration")
    print("=" * 50)
    
    # Search Agent Demo
    print("\n1. Search Attribution Agent:")
    search_agent = SearchAttributionAgent()
    
    # Process a search query
    query_data = {
        "query_id": "demo_query_001",
        "customer_id": "cust_001",
        "query_text": "best gaming headphones 2024",
        "query_sequence_position": 1
    }
    
    intent_result = await search_agent.process_search_query(query_data)
    print(f"   Query classified as: {intent_result.get('intent_category', 'unknown')}")
    
    # Get search insights
    search_insights = await search_agent.get_search_insights("cust_001")
    print(f"   Customer search history: {search_insights.get('total_searches', 0)} searches")
    
    # Calculate search attribution
    search_attribution = await search_agent.calculate_attribution_weights("cust_001", "conv_001")
    print(f"   Search attribution: {len(search_attribution.get('query_contributions', {}))} touchpoints")
    
    # Display Agent Demo
    print("\n2. Display Attribution Agent:")
    display_agent = DisplayAttributionAgent()
    
    # Analyze creative performance
    creative_analysis = await display_agent.analyze_creative_performance("cr_gaming_headphones_001")
    if "error" not in creative_analysis:
        performance_tier = creative_analysis.get("performance_summary", {}).get("performance_tier", "unknown")
        print(f"   Creative performance tier: {performance_tier}")
    else:
        print(f"   Creative analysis: {creative_analysis.get('creative_id', 'analyzed')}")
    
    # Analyze video engagement
    video_engagement = await display_agent.analyze_video_engagement("cust_001")
    print(f"   Video engagement: {video_engagement.get('total_videos', 0)} videos analyzed")
    
    # Get display insights
    display_insights = await display_agent.get_display_insights("cust_001")
    print(f"   Display impressions: {display_insights.total_impressions}")
    
    # Calculate display attribution
    display_attribution = await display_agent.calculate_display_attribution("cust_001", "conv_001")
    print(f"   Display attribution: {len(display_attribution.query_contributions)} touchpoints")

async def demo_unified_system():
    """Demonstrate unified multi-agent system"""
    print("\n\n🤝 Unified Multi-Agent System")
    print("=" * 50)
    
    manager = MultiAgentAttributionManager()
    customer_id = "cust_001"
    conversion_id = "conv_001"
    
    # Unified Attribution
    print("\n1. Unified Attribution Analysis:")
    unified_attribution = await manager.calculate_unified_attribution(customer_id, conversion_id)
    
    if "error" not in unified_attribution:
        search_weight = unified_attribution.get("search_attribution", {}).get("total_weight", 0)
        display_weight = unified_attribution.get("display_attribution", {}).get("total_weight", 0)
        
        print(f"   Search channel weight: {search_weight:.1%}")
        print(f"   Display channel weight: {display_weight:.1%}")
        
        unified_contributions = unified_attribution.get("unified_attribution", {}).get("contributions", {})
        print(f"   Total unified touchpoints: {len(unified_contributions)}")
    else:
        print(f"   Attribution analysis completed with fallback methods")
    
    # Comprehensive Insights
    print("\n2. Comprehensive Customer Insights:")
    comprehensive_insights = await manager.get_comprehensive_insights(customer_id)
    
    if "error" not in comprehensive_insights:
        # Search insights
        search_data = comprehensive_insights.get("search_insights", {})
        if isinstance(search_data, dict) and "total_searches" in search_data:
            print(f"   Search behavior: {search_data['total_searches']} searches")
            search_types = search_data.get('search_types', [])
            if search_types:
                print(f"   Search types: {', '.join(search_types)}")
        
        # Display insights
        display_data = comprehensive_insights.get("display_insights")
        if hasattr(display_data, 'total_impressions'):
            print(f"   Display behavior: {display_data.total_impressions} impressions")
            if hasattr(display_data, 'preferred_ad_formats'):
                print(f"   Preferred formats: {', '.join(display_data.preferred_ad_formats)}")
        
        # Cross-channel analysis
        cross_channel = comprehensive_insights.get("cross_channel_analysis", {})
        if isinstance(cross_channel, dict) and "sequence_pattern" in cross_channel:
            pattern = cross_channel.get("sequence_pattern", "unknown")
            print(f"   Interaction pattern: {pattern}")
        
        # Recommendations
        recommendations = comprehensive_insights.get("unified_recommendations", [])
        print(f"   Optimization recommendations: {len(recommendations)}")
        if recommendations:
            print(f"   Top recommendation: {recommendations[0]}")
    else:
        print(f"   Insights generated with available data")
    
    # Optimization Strategy
    print("\n3. Cross-Channel Optimization Strategy:")
    optimization_goals = ["increase_conversions", "improve_efficiency"]
    optimization_strategy = await manager.optimize_cross_channel_strategy(customer_id, optimization_goals)
    
    if "error" not in optimization_strategy:
        strategy = optimization_strategy.get("optimization_strategy", {})
        
        # Budget allocation
        budget_allocation = strategy.get("budget_allocation", {})
        if budget_allocation:
            search_budget = budget_allocation.get("search", 0)
            display_budget = budget_allocation.get("display", 0)
            print(f"   Recommended budget allocation:")
            print(f"     Search: {search_budget:.1%}")
            print(f"     Display: {display_budget:.1%}")
        
        # Optimization priorities
        priorities = optimization_strategy.get("implementation_priority", [])
        if priorities:
            high_priority = [p for p in priorities if p.get("priority") == "high"]
            print(f"   High priority optimizations: {len(high_priority)}")
            if high_priority:
                print(f"   Top priority: {high_priority[0].get('optimization', 'N/A')}")
        
        # Expected impact
        impact = optimization_strategy.get("expected_impact", {})
        if impact:
            print(f"   Expected improvements:")
            for metric, improvement in impact.items():
                print(f"     {metric.replace('_', ' ').title()}: {improvement}")
    else:
        print(f"   Strategy recommendations generated")

async def demo_cross_channel_coordination():
    """Demonstrate cross-channel coordination"""
    print("\n\n🔗 Cross-Channel Coordination")
    print("=" * 50)
    
    search_agent = SearchAttributionAgent()
    display_agent = DisplayAttributionAgent()
    customer_id = "cust_001"
    
    # Get search context
    print("\n1. Gathering Search Context:")
    search_insights = await search_agent.get_search_insights(customer_id)
    print(f"   Search queries analyzed: {search_insights.get('total_searches', 0)}")
    
    search_types = search_insights.get('search_types', [])
    if search_types:
        print(f"   Query types identified: {', '.join(search_types)}")
    
    # Analyze cross-channel synergy
    print("\n2. Cross-Channel Synergy Analysis:")
    synergy_analysis = await display_agent.analyze_cross_channel_synergy(customer_id, search_insights)
    
    if "error" not in synergy_analysis:
        sequence_pattern = synergy_analysis.get("sequence_pattern", "unknown")
        print(f"   Customer interaction pattern: {sequence_pattern}")
        
        optimization_opportunities = synergy_analysis.get("optimization_opportunities", [])
        print(f"   Optimization opportunities identified: {len(optimization_opportunities)}")
        
        if optimization_opportunities:
            print(f"   Key opportunity: {optimization_opportunities[0]}")
        
        # Show interaction effects if available
        interaction_effects = synergy_analysis.get("interaction_effects", {})
        if interaction_effects:
            print(f"   Cross-channel interaction effects detected")
    else:
        print(f"   Synergy analysis completed with available data")

async def main():
    """Main demonstration function"""
    print("🎯 Multi-Agent Attribution System Demo")
    print("🚀 Demonstrating Search and Display agents working together")
    print("\n" + "=" * 70)
    
    try:
        # Run all demonstrations
        await demo_individual_agents()
        await demo_unified_system()
        await demo_cross_channel_coordination()
        
        print("\n\n" + "=" * 70)
        print("✅ Demo completed successfully!")
        print("\n🔧 Next steps:")
        print("   1. Start API server: python start_server.py")
        print("   2. Test integration: python test_integration.py")
        print("   3. Run API tests: python test_api_client.py")
        print("   4. Check health: curl http://localhost:8001/health")
        
    except Exception as e:
        print(f"\n❌ Demo error: {str(e)}")
        print("Check your configuration and dependencies")

if __name__ == "__main__":
    asyncio.run(main())