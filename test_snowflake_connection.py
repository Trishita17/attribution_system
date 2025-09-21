#!/usr/bin/env python3

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from attribution_agents.data.snowflake_client import SnowflakeClient
import json

async def test_connection_and_get_data():
    """Test Snowflake connection and retrieve actual data"""
    
    try:
        print("🔌 Connecting to Snowflake...")
        client = SnowflakeClient()
        
        # Test basic connection by getting available customers
        cursor = client.connection.cursor()
        
        print("📊 Getting available customers...")
        cursor.execute("SELECT DISTINCT customer_id FROM search_queries LIMIT 5")
        customers = cursor.fetchall()
        
        if customers:
            print(f"✅ Found {len(customers)} customers:")
            for customer in customers:
                print(f"   - {customer[0]}")
            
            # Test with first customer
            test_customer = customers[0][0]
            print(f"\n🔍 Testing with customer: {test_customer}")
            
            # Get search history
            search_data = await client.get_customer_search_history(test_customer)
            print(f"📈 Search queries: {len(search_data)}")
            
            # Get display history  
            display_data = await client.get_customer_display_history(test_customer)
            print(f"📺 Display impressions: {len(display_data)}")
            
            # Get video interactions
            video_data = await client.get_customer_video_interactions(test_customer)
            print(f"🎥 Video interactions: {len(video_data)}")
            
            print(f"\n📋 Sample search query:")
            if search_data:
                print(json.dumps(search_data[0], indent=2, default=str))
            
            print(f"\n📋 Sample display impression:")
            if display_data:
                print(json.dumps(display_data[0], indent=2, default=str))
                
            return test_customer
            
        else:
            print("❌ No customers found in database")
            return None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

if __name__ == "__main__":
    customer_id = asyncio.run(test_connection_and_get_data())
    if customer_id:
        print(f"\n✅ Ready to test with customer: {customer_id}")
    else:
        print("\n❌ Connection test failed")