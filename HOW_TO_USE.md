# How Users Can Use This Multi-Agent Attribution System

## 🎯 **What This System Does**
Analyzes customer journeys across search and display channels, calculates attribution weights, and provides optimization recommendations using AI-powered agents.

## 👥 **Who Can Use It**

### **Marketing Managers**
- **Need**: Budget allocation decisions
- **Use**: Get optimization strategies and budget recommendations
- **How**: `curl http://localhost:8000/optimize-strategy/cust_001`

### **Performance Analysts** 
- **Need**: Attribution analysis for reporting
- **Use**: Calculate cross-channel attribution weights
- **How**: `curl -X POST http://localhost:8000/unified-attribution -d '{"customer_id":"cust_001","conversion_id":"conv_001"}'`

### **Creative Teams**
- **Need**: Creative performance insights
- **Use**: Analyze ad creative effectiveness
- **How**: `curl -X POST "http://localhost:8000/analyze-creative-performance?creative_id=cr_gaming_headphones_001"`

### **Data Scientists**
- **Need**: Raw attribution data for modeling
- **Use**: Direct Python integration or comprehensive API data
- **How**: `curl http://localhost:8000/comprehensive-insights/cust_001`

## 🚀 **3 Ways to Use the System**

### **1. REST API (Easiest)**
```bash
# Start system
python start_server.py

# Get customer analysis
curl http://localhost:8000/comprehensive-insights/cust_001

# Calculate attribution
curl -X POST http://localhost:8000/unified-attribution \
  -H "Content-Type: application/json" \
  -d '{"customer_id": "cust_001", "conversion_id": "conv_001"}'
```

### **2. Python Integration**
```python
import requests

# Get insights
response = requests.get('http://localhost:8000/insights/cust_001')
insights = response.json()

# Process results
print(f"Customer has {insights['data']['total_searches']} searches")
```

### **3. Direct Python Library**
```python
from attribution_agents.agent_manager import MultiAgentAttributionManager

manager = MultiAgentAttributionManager()
results = await manager.calculate_unified_attribution("cust_001", "conv_001")
```

## 📊 **What You Get**

### **Real Results from Your Data:**
- **Search Attribution**: 64.3% (9 search queries)
- **Display Attribution**: 35.7% (5 display impressions)  
- **Budget Recommendations**: 90% search, 10% display
- **Optimization Tips**: Specific actionable recommendations

### **Key Insights:**
- Cross-channel attribution weights
- Customer journey analysis
- Creative performance metrics
- Budget allocation suggestions
- Optimization strategies

## 🔧 **Integration Examples**

### **Dashboard Integration**
```javascript
// Get data for marketing dashboard
fetch('http://localhost:8000/comprehensive-insights/cust_001')
  .then(response => response.json())
  .then(data => {
    updateDashboard(data.data.unified_recommendations);
  });
```

### **Automated Optimization**
```python
# Automated budget optimization
def optimize_budgets():
    customers = get_active_customers()
    for customer_id in customers:
        strategy = requests.get(f'http://localhost:8000/optimize-strategy/{customer_id}').json()
        budget = strategy['data']['optimization_strategy']['budget_allocation']
        
        # Apply to ad platforms
        update_search_budget(customer_id, budget['search'])
        update_display_budget(customer_id, budget['display'])
```

### **Reporting Integration**
```python
# Generate attribution reports
def generate_attribution_report(customer_ids):
    report_data = []
    for customer_id in customer_ids:
        attribution = requests.post('http://localhost:8000/unified-attribution', 
                                  json={"customer_id": customer_id, "conversion_id": "conv_001"}).json()
        report_data.append(attribution['data'])
    
    return create_report(report_data)
```

## 📋 **Available Endpoints**

| What You Want | Endpoint | Method |
|---------------|----------|---------|
| Customer search behavior | `/insights/{customer_id}` | GET |
| Display ad performance | `/display-insights/{customer_id}` | GET |
| Complete customer analysis | `/comprehensive-insights/{customer_id}` | GET |
| Cross-channel attribution | `/unified-attribution` | POST |
| Optimization recommendations | `/optimize-strategy/{customer_id}` | GET |
| Creative performance | `/analyze-creative-performance` | POST |
| System health | `/health` | GET |

## 🎛️ **System Requirements**

### **To Run:**
- Python 3.8+
- Snowflake database access
- Environment variables configured

### **To Use:**
- HTTP client (curl, browser, Python requests)
- Customer IDs from your database
- Basic understanding of attribution concepts

## ✅ **Success Indicators**

- Health check returns `"database": "snowflake_connected"`
- Customer insights show your real data (9 searches, 5 impressions)
- Attribution analysis provides realistic weights (64.3% search, 35.7% display)
- Optimization recommendations are specific and actionable

## 🔍 **Troubleshooting**

### **Common Issues:**
- **Server not responding**: Run `python start_server.py`
- **500 errors**: Check Snowflake credentials in `.env` file
- **No data returned**: Verify customer IDs exist in your database
- **Attribution errors**: Ensure conversion IDs are valid

### **Check System Status:**
```bash
# Health check
curl http://localhost:8000/health

# Test with known customer
curl http://localhost:8000/insights/cust_001

# Check server logs
tail -f server.log
```

## 🎯 **Getting Started**

1. **Start the system**: `python start_server.py`
2. **Test health**: `curl http://localhost:8000/health`
3. **Try sample customer**: `curl http://localhost:8000/comprehensive-insights/cust_001`
4. **Review results**: Check attribution weights and recommendations
5. **Integrate**: Use API endpoints in your applications

## 💡 **Best Practices**

- **Monitor regularly**: Check `/health` endpoint
- **Batch process**: Use comprehensive insights for multiple customers
- **Handle errors**: Always check response status codes
- **Cache results**: Attribution calculations can be cached for performance
- **Update data**: Ensure Snowflake data is fresh for accurate results

**Your multi-agent attribution system is ready to provide real insights from your Snowflake data!**