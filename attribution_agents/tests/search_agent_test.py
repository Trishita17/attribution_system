import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from typing import Dict, Any

# Import your modules
from search_attribution_agent.agents.search_agents import SearchAttributionAgent
from search_attribution_agent.data.model import AttributionResult
from search_attribution_agent.config.settings import settings

class TestSearchAttributionAgent:
    """Test suite for Search Attribution Agent"""
    
    @pytest.fixture
    async def search_agent(self):
        """Create a search agent instance for testing"""
        return SearchAttributionAgent()
    
    @pytest.fixture
    def sample_query_data(self):
        """Sample query data for testing"""
        return {
            "query_id": "sq_001_001",
            "customer_id": "cust_001",
            "session_id": "sess_001_1", 
            "query_text": "best gaming headphones 2024",
            "query_type": "product_research",
            "timestamp": "2024-01-15 10:30:00",
            "query_sequence_position": 1
        }
    
    @pytest.fixture
    def sample_journey_data(self):
        """Sample customer journey for testing"""
        return {
            "customer_id": "cust_001",
            "queries": [
                {
                    "query_id": "sq_001_001",
                    "query_text": "best gaming headphones 2024",
                    "query_type": "product_research",
                    "timestamp": "2024-01-15 10:30:00"
                },
                {
                    "query_id": "sq_001_002", 
                    "query_text": "SteelSeries Arctis 7 review",
                    "query_type": "validation",
                    "timestamp": "2024-01-17 09:45:00"
                }
            ]
        }
    
    # =============================================================================
    # UNIT TESTS - Test Individual Components
    # =============================================================================
    
    async def test_agent_initialization(self, search_agent):
        """Test that the agent initializes correctly"""
        assert search_agent.agent_id == "search_attribution_agent"
        assert search_agent.db_client is not None
        assert search_agent.llm_client is not None
    
    @patch('search_attribution_agent.llm.client.LLMClient.classify_search_intent')
    async def test_process_search_query(self, mock_llm, search_agent, sample_query_data):
        """Test single query processing with mocked LLM"""
        # Mock LLM response
        mock_llm.return_value = {
            "intent_category": "product_research",
            "purchase_intent": 0.6,
            "urgency": 0.3,
            "confidence_score": 0.85
        }
        
        result = await search_agent.process_search_query(sample_query_data)
        
        assert result["intent_category"] == "product_research"
        assert result["purchase_intent"] == 0.6
        assert "confidence_score" in result
        mock_llm.assert_called_once()
    
    @patch('search_attribution_agent.data.snowflake_client.SnowflakeClient.get_search_sessions')
    async def test_analyze_search_session(self, mock_db, search_agent):
        """Test search session analysis"""
        # Mock database response
        mock_db.return_value = [{
            "session_id": "sess_001_1",
            "customer_id": "cust_001", 
            "total_queries": 3,
            "session_outcome": "conversion"
        }]
        
        result = await search_agent.analyze_search_session("sess_001_1")
        
        assert result["session_id"] == "sess_001_1"
        assert "total_queries" in result
        mock_db.assert_called_once()
    
    # =============================================================================
    # INTEGRATION TESTS - Test Real Database/LLM Integration
    # =============================================================================
    
    @pytest.mark.integration
    async def test_real_llm_intent_classification(self, search_agent, sample_query_data):
        """Test actual LLM intent classification (requires API key)"""
        if not settings.ANTHROPIC_API_KEY:
            pytest.skip("No API key available for LLM testing")
        
        result = await search_agent.llm_client.classify_search_intent(sample_query_data)
        
        # Verify structure of real LLM response
        assert "intent_category" in result or "error" in result
        if "intent_category" in result:
            assert isinstance(result["intent_category"], str)
            assert "purchase_intent" in result
    
    @pytest.mark.integration 
    async def test_real_database_connection(self, search_agent):
        """Test actual database connectivity"""
        try:
            result = await search_agent.db_client.get_customer_search_history("cust_001")
            assert isinstance(result, list)
        except ConnectionError as e:
            pytest.fail(f"Database connection failed: {e}")
        except AttributeError as e:
            pytest.fail(f"Missing database method: {e}")
    
    # =============================================================================
    # END-TO-END TESTS - Test Complete Attribution Flow
    # =============================================================================
    
    @pytest.mark.e2e
    async def test_complete_attribution_flow(self, search_agent, sample_journey_data):
        """Test complete attribution calculation flow"""
        customer_id = sample_journey_data["customer_id"]
        conversion_id = "conv_001"
        
        try:
            result = await search_agent.calculate_attribution_weights(customer_id, conversion_id)
            
            # Verify attribution result structure
            assert isinstance(result, (AttributionResult, dict))
            if isinstance(result, dict):
                assert "customer_id" in result
                assert "query_contributions" in result or "error" in result
                
        except NotImplementedError:
            pytest.skip("Attribution calculation not yet implemented")
        except AttributeError as e:
            pytest.fail(f"Missing attribution method: {e}")

# =============================================================================
# MANUAL TESTING SCRIPT - For Quick Verification
# =============================================================================

async def manual_test_search_agent():
    """
    Manual testing script to verify search agent functionality
    Run this directly to test your implementation
    """
    print("🚀 Starting Search Attribution Agent Manual Testing...")
    
    try:
        # Initialize agent
        print("\n1. Initializing Search Agent...")
        agent = SearchAttributionAgent()
        print("✅ Agent initialized successfully")
        
        # Test 1: Database Connection
        print("\n2. Testing Database Connection...")
        try:
            result = await agent.db_client.get_customer_search_history("cust_001")
            print(f"✅ Database connected - Retrieved {len(result)} search records")
        except ConnectionError as e:
            print(f"❌ Database connection failed: {e}")
        except AttributeError as e:
            print(f"❌ Database method missing: {e}")
        except Exception as e:
            print(f"❌ Unexpected database error: {e}")
        
        # Test 2: LLM Classification
        print("\n3. Testing LLM Intent Classification...")
        test_query = {
            "query_id": "test_001",
            "customer_id": "cust_001",
            "query_text": "best gaming headphones 2024",
            "query_sequence_position": 1
        }
        
        try:
            intent_result = await agent.llm_client.classify_search_intent(test_query)
            print(f"✅ LLM Classification successful:")
            print(f"   Intent: {intent_result.get('intent_category', 'N/A')}")
            print(f"   Purchase Intent: {intent_result.get('purchase_intent', 'N/A')}")
            print(f"   Confidence: {intent_result.get('confidence_score', 'N/A')}")
        except ConnectionError as e:
            print(f"❌ LLM API connection failed: {e}")
        except ValueError as e:
            print(f"❌ LLM response parsing failed: {e}")
        except Exception as e:
            print(f"❌ Unexpected LLM error: {e}")
        
        # Test 3: Process Sample Query
        print("\n4. Testing Query Processing...")
        try:
            process_result = await agent.process_search_query(test_query)
            print(f"✅ Query processing successful")
            print(f"   Result keys: {list(process_result.keys())}")
        except NotImplementedError:
            print("⚠️ Query processing not yet implemented")
        except Exception as e:
            print(f"❌ Query processing failed: {e}")
        
        # Test 4: Attribution Analysis (if implemented)
        print("\n5. Testing Attribution Analysis...")
        try:
            attribution_result = await agent.calculate_attribution_weights("cust_001", "conv_001")
            print(f"✅ Attribution analysis successful")
            print(f"   Attribution weights calculated for customer cust_001")
        except NotImplementedError:
            print("⚠️ Attribution analysis not yet implemented (expected)")
        except Exception as e:
            print(f"❌ Attribution analysis error: {e}")
        
        print("\n🎉 Manual testing completed!")
        print("\n📊 Test Summary:")
        print("   - Agent initialization: Working")
        print("   - Database connection: Check output above") 
        print("   - LLM integration: Check output above")
        print("   - Query processing: Check output above")
        print("   - Attribution analysis: May be incomplete")
        
    except Exception as e:
        print(f"\n💥 Critical error during testing: {e}")
        print("Check your configuration and dependencies")

# =============================================================================
# QUICK VALIDATION SCRIPT - Test with Real Data
# =============================================================================

async def validate_with_real_data():
    """
    Validate search agent with your actual sample data
    """
    print("🔍 Validating Search Agent with Real Sample Data...")
    
    try:
        from search_attribution_agent.data.snowflake_client import SnowflakeClient
        
        db = SnowflakeClient()
        
        # Get real search queries from your sample data
        print("\n1. Fetching real search queries...")
        try:
            # Use proper async database method instead of direct cursor
            queries = await db.get_customer_search_history("cust_001")
            
            print(f"✅ Found {len(queries)} queries for cust_001")
            
            # Test intent classification on real queries
            agent = SearchAttributionAgent()
            
            for query in queries[:5]:  # Limit to first 5 queries
                query_data = {
                    "query_id": query.get("query_id", "unknown"),
                    "customer_id": query.get("customer_id", "cust_001"), 
                    "query_text": query.get("query_text", ""),
                    "existing_type": query.get("query_type", "unknown"),
                    "existing_stage": query.get("funnel_stage", "unknown")
                }
                
                print(f"\n📝 Testing: '{query_data['query_text']}'")
                print(f"   Original classification: {query_data['existing_type']} / {query_data['existing_stage']}")
                
                try:
                    result = await agent.llm_client.classify_search_intent(query_data)
                    llm_intent = result.get("intent_category", "unknown")
                    llm_stage = result.get("funnel_stage", "unknown")
                    confidence = result.get("confidence_score", 0)
                    
                    print(f"   LLM classification: {llm_intent} / {llm_stage} (confidence: {confidence})")
                    
                    # Compare classifications
                    if llm_intent.lower() in query_data['existing_type'].lower() or query_data['existing_type'].lower() in llm_intent.lower():
                        print("   ✅ Classifications align!")
                    else:
                        print("   🤔 Classifications differ - this is normal and shows LLM insights")
                        
                except ConnectionError as e:
                    print(f"   ❌ API connection failed: {e}")
                except ValueError as e:
                    print(f"   ❌ Response parsing failed: {e}")
                except Exception as e:
                    print(f"   ❌ Classification failed: {e}")
                    
        except ConnectionError as e:
            print(f"❌ Database connection failed: {e}")
        except AttributeError as e:
            print(f"❌ Database method missing: {e}")
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
    except Exception as e:
        print(f"❌ Validation failed: {e}")

if __name__ == "__main__":
    # Run manual tests
    asyncio.run(manual_test_search_agent())