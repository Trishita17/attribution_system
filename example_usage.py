#!/usr/bin/env python3
"""
Example Usage of Multi-Agent Attribution System
Shows different ways users can interact with the system
"""
import requests
import json
import asyncio
from attribution_agents.agent_manager import MultiAgentAttributionManager

# API Base URL
BASE_URL = "http://localhost:8000"

def example_api_usage():
    """Example: Using the system via REST API"""
    print("🌐 API Usage Examples")
    print("=" * 50)
    
    # 1. Get customer search insights
    print("\n1. Getting Search Insights...")
    response = requests.get(f"{BASE_URL}/insights/cust_001")
    if response.status_code == 200:
        data = response.json()
        insights = data.get('data', {})
        print(f"   Customer has {insights.get('total_searches', 0)} search queries")
        print(f"   Search types: {insights.get('search_types', [])}")
    
    # 2. Get display insights
    print("\n2. Getting Display Insights...")
    response = requests.get(f"{BASE_URL}/display-insights/cust_001")
    if response.status_code == 200:
        print("   ✅ Display insights retrieved")
    
    # 3. Calculate unified attribution
    print("\n3. Calculating Cross-Channel Attribution...")
    attribution_data = {
        "customer_id": "cust_001",
        "conversion_id": "conv_001"
    }
    response = requests.post(
        f"{BASE_URL}/unified-attribution",
        json=attribution_data
    )
    if response.status_code == 200:
        data = response.json()
        attribution = data.get('data', {})
        search_weight = attribution.get('search_attribution', {}).get('total_weight', 0)
        display_weight = attribution.get('display_attribution', {}).get('total_weight', 0)
        print(f"   Search Attribution: {search_weight:.1%}")
        print(f"   Display Attribution: {display_weight:.1%}")
    
    # 4. Get comprehensive insights
    print("\n4. Getting Comprehensive Customer Analysis...")
    response = requests.get(f"{BASE_URL}/comprehensive-insights/cust_001")
    if response.status_code == 200:
        data = response.json()
        insights = data.get('data', {})
        recommendations = insights.get('unified_recommendations', [])
        print(f"   Generated {len(recommendations)} optimization recommendations")
        if recommendations:
            print(f"   Top recommendation: {recommendations[0]}")
    
    # 5. Get optimization strategy
    print("\n5. Getting Optimization Strategy...")
    response = requests.get(f"{BASE_URL}/optimize-strategy/cust_001?goals=increase_conversions")
    if response.status_code == 200:
        data = response.json()
        strategy = data.get('data', {}).get('optimization_strategy', {})
        budget = strategy.get('budget_allocation', {})
        if budget:
            print(f"   Recommended Budget - Search: {budget.get('search', 0):.1%}, Display: {budget.get('display', 0):.1%}")

async def example_direct_usage():
    """Example: Using the system directly via Python"""
    print("\n\n🐍 Direct Python Usage Examples")
    print("=" * 50)
    
    try:
        # Initialize the multi-agent manager
        manager = MultiAgentAttributionManager()
        
        # 1. Calculate unified attribution
        print("\n1. Calculating Unified Attribution...")
        attribution_result = await manager.calculate_unified_attribution("cust_001", "conv_001")
        
        if "error" not in attribution_result:
            search_weight = attribution_result.get("search_attribution", {}).get("total_weight", 0)
            display_weight = attribution_result.get("display_attribution", {}).get("total_weight", 0)
            print(f"   Search Channel: {search_weight:.1%}")
            print(f"   Display Channel: {display_weight:.1%}")
        
        # 2. Get comprehensive insights
        print("\n2. Getting Comprehensive Insights...")
        insights = await manager.get_comprehensive_insights("cust_001")
        
        if "error" not in insights:
            search_data = insights.get("search_insights", {})
            display_data = insights.get("display_insights")
            
            print(f"   Search queries: {search_data.get('total_searches', 0)}")
            if hasattr(display_data, 'total_impressions'):
                print(f"   Display impressions: {display_data.total_impressions}")
            
            recommendations = insights.get("unified_recommendations", [])
            print(f"   Optimization recommendations: {len(recommendations)}")
        
        # 3. Generate optimization strategy
        print("\n3. Generating Optimization Strategy...")
        strategy = await manager.optimize_cross_channel_strategy(
            "cust_001", 
            ["increase_conversions", "improve_efficiency"]
        )
        
        if "error" not in strategy:
            opt_strategy = strategy.get("optimization_strategy", {})
            budget_allocation = opt_strategy.get("budget_allocation", {})
            
            if budget_allocation:
                print(f"   Search budget: {budget_allocation.get('search', 0):.1%}")
                print(f"   Display budget: {budget_allocation.get('display', 0):.1%}")
            
            priorities = strategy.get("implementation_priority", [])
            high_priority = [p for p in priorities if p.get("priority") == "high"]
            print(f"   High priority optimizations: {len(high_priority)}")
    
    except Exception as e:
        print(f"   Error in direct usage: {str(e)}")

def example_business_scenarios():
    """Example: Real business scenarios"""
    print("\n\n💼 Business Scenario Examples")
    print("=" * 50)
    
    scenarios = [
        {
            "role": "Marketing Manager",
            "goal": "Optimize budget allocation across channels",
            "endpoint": f"{BASE_URL}/optimize-strategy/cust_001",
            "method": "GET"
        },
        {
            "role": "Performance Analyst", 
            "goal": "Understand attribution weights for reporting",
            "endpoint": f"{BASE_URL}/unified-attribution",
            "method": "POST",
            "data": {"customer_id": "cust_001", "conversion_id": "conv_001"}
        },
        {
            "role": "Creative Director",
            "goal": "Analyze creative performance",
            "endpoint": f"{BASE_URL}/analyze-creative-performance?creative_id=cr_gaming_headphones_001",
            "method": "POST"
        },
        {
            "role": "Data Scientist",
            "goal": "Get comprehensive customer journey data",
            "endpoint": f"{BASE_URL}/comprehensive-insights/cust_001",
            "method": "GET"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n{scenario['role']}:")
        print(f"   Goal: {scenario['goal']}")
        print(f"   API Call: {scenario['method']} {scenario['endpoint']}")
        
        if scenario['method'] == 'GET':
            print(f"   Usage: curl {scenario['endpoint']}")
        else:
            data = scenario.get('data', {})
            print(f"   Usage: curl -X {scenario['method']} {scenario['endpoint']} -H 'Content-Type: application/json' -d '{json.dumps(data)}'")

def example_integration_patterns():
    """Example: Common integration patterns"""
    print("\n\n🔧 Integration Pattern Examples")
    print("=" * 50)
    
    print("\n1. Batch Processing Pattern:")
    print("""
    # Process multiple customers
    customers = ['cust_001', 'cust_002', 'cust_003']
    for customer_id in customers:
        response = requests.get(f'{BASE_URL}/comprehensive-insights/{customer_id}')
        insights = response.json()
        # Process insights...
    """)
    
    print("\n2. Real-time Attribution Pattern:")
    print("""
    # Calculate attribution on conversion
    def on_conversion(customer_id, conversion_id):
        attribution_data = {
            "customer_id": customer_id,
            "conversion_id": conversion_id
        }
        response = requests.post(f'{BASE_URL}/unified-attribution', json=attribution_data)
        return response.json()
    """)
    
    print("\n3. Dashboard Integration Pattern:")
    print("""
    # Get data for dashboard
    def get_dashboard_data(customer_id):
        insights = requests.get(f'{BASE_URL}/comprehensive-insights/{customer_id}').json()
        strategy = requests.get(f'{BASE_URL}/optimize-strategy/{customer_id}').json()
        
        return {
            'customer_insights': insights['data'],
            'optimization_strategy': strategy['data']
        }
    """)
    
    print("\n4. Automated Optimization Pattern:")
    print("""
    # Automated budget optimization
    def optimize_campaign_budgets():
        customers = get_active_customers()
        for customer_id in customers:
            strategy = requests.get(f'{BASE_URL}/optimize-strategy/{customer_id}').json()
            budget_allocation = strategy['data']['optimization_strategy']['budget_allocation']
            
            # Apply budget changes to ad platforms
            update_search_budget(customer_id, budget_allocation['search'])
            update_display_budget(customer_id, budget_allocation['display'])
    """)

def main():
    """Run all examples"""
    print("🎯 Multi-Agent Attribution System - Usage Examples")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and healthy")
        else:
            print("⚠️ Server responded but may have issues")
    except requests.exceptions.RequestException:
        print("❌ Server is not running. Start with: python start_server.py")
        return
    
    # Run examples
    example_api_usage()
    asyncio.run(example_direct_usage())
    example_business_scenarios()
    example_integration_patterns()
    
    print("\n\n🎉 Examples completed!")
    print("📖 See USER_GUIDE.md for detailed documentation")
    print("🚀 See QUICK_START.md for immediate usage")

if __name__ == "__main__":
    main()