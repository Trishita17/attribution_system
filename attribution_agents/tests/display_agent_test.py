import asyncio
import pytest
from unittest.mock import Mock, AsyncMock, patch
from agents.display_agent import DisplayAttributionAgent
from data.models import DisplayInsights, AttributionResult, CreativePerformance

class TestDisplayAttributionAgent:
    """
    Test suite for Display Attribution Agent
    """
    
    @pytest.fixture
    async def display_agent(self):
        """Create a display agent instance for testing"""
        return DisplayAttributionAgent()
    
    @pytest.fixture
    def sample_creative_data(self):
        """Sample creative performance data"""
        return {
            "creative_id": "cr_gaming_001",
            "creative_data": {
                "creative_type": "video",
                "campaign_id": "camp_gaming",
                "total_impressions": 10000,
                "unique_viewers": 6500,
                "avg_viewability": 0.92,
                "click_through_rate": 0.045,
                "conversion_rate": 0.025,
                "brand_lift_score": 0.18
            },
            "performance_metrics": {
                "ctr": 0.045,
                "cvr": 0.025,
                "viewability": 0.92,
                "brand_lift": 0.18
            }
        }
    
    @pytest.fixture
    def sample_display_journey(self):
        """Sample customer display journey"""
        return {
            "customer_id": "cust_001",
            "display_touchpoints": [
                {
                    "impression_id": "imp_001_001",
                    "creative_id": "cr_gaming_001", 
                    "ad_format": "video",
                    "viewability_score": 0.95,
                    "timestamp": "2024-01-14T20:30:00"
                },
                {
                    "impression_id": "imp_001_002",
                    "creative_id": "cr_gaming_002",
                    "ad_format": "banner", 
                    "viewability_score": 0.88,
                    "timestamp": "2024-01-16T14:20:00"
                }
            ]
        }
    
    # =============================================================================
    # UNIT TESTS
    # =============================================================================
    
    async def test_agent_initialization(self, display_agent):
        """Test that the display agent initializes correctly"""
        assert display_agent.agent_id == "display_attribution_agent"
        assert display_agent.db_client is not None
        assert display_agent.llm_client is not None
    
    @patch('data.snowflake_client.SnowflakeClient.get_creative_performance')
    @patch('llm.client.LLMClient.analyze_creative_performance')
    async def test_analyze_creative_performance(self, mock_llm, mock_db, display_agent, sample_creative_data):
        """Test creative performance analysis"""
        # Mock database response
        mock_db.return_value = sample_creative_data["creative_data"]
        
        # Mock LLM response
        mock_llm.return_value = {
            "performance_tier": "good_performer",
            "key_recommendations": ["Optimize targeting", "Test new formats"],
            "confidence_score": 0.85
        }
        
        result = await display_agent.analyze_creative_performance("cr_gaming_001")
        
        assert "performance_summary" in result
        assert "llm_insights" in result
        assert "optimization_recommendations" in result
        mock_db.assert_called_once()
        mock_llm.assert_called_once()
    
    @patch('data.snowflake_client.SnowflakeClient.get_customer_video_interactions')
    async def test_analyze_video_engagement(self, mock_db, display_agent):
        """Test video engagement analysis"""
        # Mock video interaction data
        mock_db.return_value = [
            {
                "interaction_id": "vid_001",
                "video_id": "vid_gaming_demo",
                "completion_rate": 0.85,
                "video_duration_seconds": 120,
                "engagement_points": [{"time": 30, "action": "pause"}]
            }
        ]
        
        result = await display_agent.analyze_video_engagement("cust_001")
        
        assert result["customer_id"] == "cust_001"
        assert "total_videos" in result
        assert "avg_completion_rate" in result
        assert "engagement_depth" in result
        mock_db.assert_called_once()
    
    @patch('data.snowflake_client.SnowflakeClient.get_customer_display_history')
    @patch('llm.client.LLMClient.analyze_display_attribution')
    async def test_calculate_display_attribution(self, mock_llm, mock_db, display_agent, sample_display_journey):
        """Test display attribution calculation"""
        # Mock database response
        mock_db.return_value = sample_display_journey["display_touchpoints"]
        
        # Mock LLM response
        mock_llm.return_value = {
            "touchpoint_contributions": {
                "imp_001_001": 0.6,
                "imp_001_002": 0.4
            },
            "confidence_score": 0.8
        }
        
        result = await display_agent.calculate_display_attribution("cust_001", "conv_001")
        
        assert isinstance(result, AttributionResult)
        assert result.customer_id == "cust_001"
        assert result.total_attribution_weight == 1.0
        mock_db.assert_called_once()
        mock_llm.assert_called_once()

# =============================================================================
# MANUAL TESTING SCRIPT
# =============================================================================

async def manual_test_display_agent():
    """
    Manual testing script for Display Attribution Agent
    """
    print("🎨 Starting Display Attribution Agent Manual Testing...")
    
    try:
        # Initialize agent
        print("\n1. Initializing Display Agent...")
        agent = DisplayAttributionAgent()
        print("✅ Display Agent initialized successfully")
        
        # Test 1: Database Connection (Creative Performance)
        print("\n2. Testing Creative Performance Retrieval...")
        try:
            # Test with a known creative from sample data
            creative_result = await agent.db_client.get_creative_performance("cr_gaming_headphones_001")
            if creative_result:
                print(f"✅ Retrieved creative data: {creative_result.get('creative_name', 'Unknown')}")
                print(f"   CTR: {creative_result.get('click_through_rate', 0):.3f}")
                print(f"   CVR: {creative_result.get('conversion_rate', 0):.3f}")
            else:
                print("⚠️ No creative data found - check sample data loading")
        except Exception as e:
            print(f"❌ Creative data retrieval failed: {str(e)}")
        
        # Test 2: Video Engagement Analysis
        print("\n3. Testing Video Engagement Analysis...")
        try:
            video_result = await agent.analyze_video_engagement("cust_001")
            print(f"✅ Video engagement analysis completed")
            print(f"   Total videos: {video_result.get('total_videos', 0)}")
            print(f"   Avg completion rate: {video_result.get('avg_completion_rate', 0):.2f}")
            print(f"   Engagement tier: {video_result.get('engagement_depth', {}).get('engagement_tier', 'unknown')}")
        except Exception as e:
            print(f"❌ Video engagement analysis failed: {str(e)}")
        
        # Test 3: Creative Performance Analysis
        print("\n4. Testing Creative Performance Analysis...")
        try:
            creative_analysis = await agent.analyze_creative_performance("cr_gaming_headphones_001")
            print(f"✅ Creative analysis completed")
            if "error" not in creative_analysis:
                print(f"   Performance tier: {creative_analysis.get('performance_summary', {}).get('performance_tier', 'unknown')}")
                recommendations = creative_analysis.get("optimization_recommendations", [])
                print(f"   Recommendations: {len(recommendations)} suggestions")
            else:
                print(f"   ⚠️ Analysis used fallback method")
        except Exception as e:
            print(f"❌ Creative analysis failed: {str(e)}")
        
        # Test 4: Display Attribution Analysis
        print("\n5. Testing Display Attribution Analysis...")
        try:
            attribution_result = await agent.calculate_display_attribution("cust_001", "conv_001")
            print(f"✅ Display attribution analysis completed")
            if attribution_result.error:
                print(f"   ⚠️ Attribution analysis: {attribution_result.error}")
            else:
                print(f"   Total attribution weight: {attribution_result.total_attribution_weight}")
                print(f"   Confidence score: {attribution_result.confidence_score}")
                print(f"   Touchpoints analyzed: {len(attribution_result.query_contributions)}")
        except Exception as e:
            print(f"❌ Attribution analysis failed: {str(e)}")
        
        # Test 5: Cross-Channel Analysis (if Search Agent available)
        print("\n6. Testing Cross-Channel Analysis...")
        try:
            cross_channel_result = await agent.analyze_cross_channel_synergy("cust_001")
            print(f"✅ Cross-channel analysis completed")
            print(f"   Analysis result: {cross_channel_result.get('analysis', 'completed')}")
            if cross_channel_result.get("optimization_opportunities"):
                print(f"   Opportunities identified: {len(cross_channel_result['optimization_opportunities'])}")
        except Exception as e:
            print(f"❌ Cross-channel analysis failed: {str(e)}")
        
        print("\n🎉 Display Agent Manual Testing Completed!")
        print("\n📊 Test Summary:")
        print("   - Agent initialization: Working")
        print("   - Database connectivity: Check output above")
        print("   - Video engagement analysis: Check output above") 
        print("   - Creative performance analysis: Check output above")
        print("   - Display attribution: Check output above")
        print("   - Cross-channel analysis: Check output above")
        
    except Exception as e:
        print(f"\n💥 Critical error during testing: {str(e)}")
        print("Check your configuration and dependencies")

# =============================================================================
# CROSS-AGENT VALIDATION
# =============================================================================

async def test_cross_agent_integration():
    """
    Test integration between Search and Display agents
    """
    print("🔗 Testing Cross-Agent Integration...")
    
    try:
        from agents.search_agent import SearchAttributionAgent
        from agents.display_agent import DisplayAttributionAgent
        
        search_agent = SearchAttributionAgent()
        display_agent = DisplayAttributionAgent()
        
        customer_id = "cust_001"
        
        print(f"\n1. Getting Search insights for {customer_id}...")
        search_insights = await search_agent.get_search_insights(customer_id)
        print(f"   Search queries: {search_insights.get('total_searches', 0)}")
        
        print(f"\n2. Getting Display insights for {customer_id}...")
        display_insights = await display_agent.get_display_insights(customer_id)
        print(f"   Display impressions: {display_insights.total_impressions}")
        
        print(f"\n3. Cross-channel synergy analysis...")
        synergy_result = await display_agent.analyze_cross_channel_synergy(
            customer_id, 
            search_insights
        )
        print(f"   Synergy analysis: {synergy_result.get('analysis', 'completed')}")
        
        print("✅ Cross-agent integration test completed")
        
    except ImportError:
        print("⚠️ Search Agent not available - skipping cross-agent test")
    except Exception as e:
        print(f"❌ Cross-agent integration failed: {str(e)}")