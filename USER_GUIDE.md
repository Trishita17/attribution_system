# Multi-Agent Attribution System - User Guide

## 🚀 Quick Start

### 1. Start the System
```bash
cd attribution_system
source venv/bin/activate
python start_server.py
```
Server runs at: `http://localhost:8000`

### 2. Check System Health
```bash
curl http://localhost:8000/health
```

## 📊 How to Use the System

### **Method 1: API Endpoints (Recommended)**

#### Get Customer Search Insights
```bash
curl http://localhost:8000/insights/cust_001
```

#### Get Customer Display Insights  
```bash
curl http://localhost:8000/display-insights/cust_001
```

#### Calculate Unified Attribution
```bash
curl -X POST http://localhost:8000/unified-attribution \
  -H "Content-Type: application/json" \
  -d '{"customer_id": "cust_001", "conversion_id": "conv_001"}'
```

#### Get Comprehensive Customer Analysis
```bash
curl http://localhost:8000/comprehensive-insights/cust_001
```

#### Get Optimization Strategy
```bash
curl "http://localhost:8000/optimize-strategy/cust_001?goals=increase_conversions,improve_efficiency"
```

### **Method 2: Python Scripts**

#### Run Complete Demo
```bash
python use_agent.py
```

#### Test Individual Components
```bash
python test_integration.py
```

#### Test API Endpoints
```bash
python test_api_simple.py
```

## 🎯 Use Cases

### **Marketing Manager**
- **Goal**: Understand customer journey and optimize budget allocation
- **Use**: 
  ```bash
  curl http://localhost:8000/comprehensive-insights/cust_001
  curl http://localhost:8000/optimize-strategy/cust_001
  ```

### **Performance Analyst**
- **Goal**: Analyze attribution weights and channel effectiveness
- **Use**:
  ```bash
  curl -X POST http://localhost:8000/unified-attribution \
    -H "Content-Type: application/json" \
    -d '{"customer_id": "cust_001", "conversion_id": "conv_001"}'
  ```

### **Creative Team**
- **Goal**: Optimize ad creative performance
- **Use**:
  ```bash
  curl -X POST "http://localhost:8000/analyze-creative-performance?creative_id=cr_gaming_headphones_001"
  ```

### **Data Scientist**
- **Goal**: Access raw attribution data for modeling
- **Use**: Direct API calls or Python integration:
  ```python
  from attribution_agents.agent_manager import MultiAgentAttributionManager
  
  manager = MultiAgentAttributionManager()
  results = await manager.calculate_unified_attribution("cust_001", "conv_001")
  ```

## 📈 What You Get

### **Attribution Analysis**
- Cross-channel attribution weights
- Search vs Display contribution percentages
- Touchpoint-level attribution scores

### **Customer Insights**
- Search behavior patterns
- Display engagement metrics
- Video interaction analysis
- Cross-device behavior

### **Optimization Recommendations**
- Budget allocation suggestions
- Creative optimization tips
- Frequency capping recommendations
- Cross-channel coordination strategies

## 🔧 Integration Options

### **1. REST API Integration**
```javascript
// JavaScript example
fetch('http://localhost:8000/comprehensive-insights/cust_001')
  .then(response => response.json())
  .then(data => console.log(data));
```

### **2. Python Integration**
```python
import requests

# Get customer insights
response = requests.get('http://localhost:8000/insights/cust_001')
insights = response.json()

# Calculate attribution
attribution_data = {
    "customer_id": "cust_001", 
    "conversion_id": "conv_001"
}
response = requests.post(
    'http://localhost:8000/unified-attribution',
    json=attribution_data
)
attribution = response.json()
```

### **3. Direct Python Library Usage**
```python
from attribution_agents.agents.search_agents import SearchAttributionAgent
from attribution_agents.agents.display_agents import DisplayAttributionAgent

# Initialize agents
search_agent = SearchAttributionAgent()
display_agent = DisplayAttributionAgent()

# Get insights
search_insights = await search_agent.get_search_insights("cust_001")
display_insights = await display_agent.get_display_insights("cust_001")
```

## 📋 Available Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | System status |
| `/insights/{customer_id}` | GET | Search insights |
| `/display-insights/{customer_id}` | GET | Display insights |
| `/unified-attribution` | POST | Cross-channel attribution |
| `/comprehensive-insights/{customer_id}` | GET | Complete analysis |
| `/optimize-strategy/{customer_id}` | GET | Optimization recommendations |
| `/cross-channel-analysis/{customer_id}` | GET | Channel synergy analysis |

## 🎛️ Configuration

### **Environment Variables** (`.env` file)
```bash
# Snowflake Connection
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_DATABASE=MULTI_AGENT_ATTRIBUTION
SNOWFLAKE_SCHEMA=ATTRIBUTION_SCHEMA

# LLM Configuration  
ANTHROPIC_API_KEY=your_api_key
LLM_MODEL=claude-3-haiku-20240307
```

## 🔍 Monitoring & Troubleshooting

### **Check Logs**
```bash
tail -f server.log
```

### **Test Database Connection**
```bash
python -c "
from attribution_agents.data.snowflake_client import SnowflakeClient
import asyncio
async def test(): 
    client = SnowflakeClient()
    print('✅ Connected to Snowflake')
asyncio.run(test())
"
```

### **Common Issues**
- **500 Error**: Check Snowflake credentials in `.env`
- **404 Error**: Ensure server is running on port 8000
- **Connection Error**: Verify Snowflake account and network access

## 📊 Sample Response Formats

### **Attribution Response**
```json
{
  "status": "success",
  "data": {
    "customer_id": "cust_001",
    "search_attribution": {
      "total_weight": 0.643,
      "contributions": {"q_001": 0.2, "q_002": 0.443}
    },
    "display_attribution": {
      "total_weight": 0.357,
      "contributions": {"imp_001": 0.357}
    },
    "unified_attribution": {
      "total_weight": 1.0,
      "channel_weights": {"search": 0.643, "display": 0.357}
    }
  }
}
```

### **Optimization Response**
```json
{
  "status": "success", 
  "data": {
    "optimization_strategy": {
      "budget_allocation": {"search": 0.9, "display": 0.1},
      "search_optimizations": ["Target decision-stage keywords"],
      "display_optimizations": ["Improve creative viewability"]
    },
    "expected_impact": {
      "attribution_accuracy": "15-25% improvement expected"
    }
  }
}
```

## 🎯 Best Practices

1. **Regular Monitoring**: Check `/health` endpoint regularly
2. **Batch Processing**: Use comprehensive insights for multiple customers
3. **Data Freshness**: Ensure Snowflake data is updated regularly  
4. **Error Handling**: Always check response status before processing
5. **Rate Limiting**: Don't exceed reasonable API call frequency

## 🚀 Getting Started Checklist

- [ ] System running (`python start_server.py`)
- [ ] Health check passes (`curl http://localhost:8000/health`)
- [ ] Test with sample customer (`curl http://localhost:8000/insights/cust_001`)
- [ ] Review sample responses
- [ ] Integrate with your application
- [ ] Set up monitoring and logging