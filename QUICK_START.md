# Quick Start Guide

## 🚀 Start Using in 3 Steps

### Step 1: Start the System
```bash
cd attribution_system
source venv/bin/activate
python start_server.py
```

### Step 2: Test the System
```bash
# Check if running
curl http://localhost:8000/health

# Get customer insights
curl http://localhost:8000/insights/cust_001
```

### Step 3: Get Attribution Analysis
```bash
# Complete customer analysis
curl http://localhost:8000/comprehensive-insights/cust_001

# Cross-channel attribution
curl -X POST http://localhost:8000/unified-attribution \
  -H "Content-Type: application/json" \
  -d '{"customer_id": "cust_001", "conversion_id": "conv_001"}'
```

## 🎯 Common Use Cases

### Marketing Manager - Budget Optimization
```bash
curl http://localhost:8000/optimize-strategy/cust_001
```
**Returns**: Budget allocation recommendations, optimization strategies

### Analyst - Attribution Analysis  
```bash
curl -X POST http://localhost:8000/unified-attribution \
  -H "Content-Type: application/json" \
  -d '{"customer_id": "cust_001", "conversion_id": "conv_001"}'
```
**Returns**: Cross-channel attribution weights, touchpoint contributions

### Creative Team - Performance Analysis
```bash
curl -X POST "http://localhost:8000/analyze-creative-performance?creative_id=cr_gaming_headphones_001"
```
**Returns**: Creative performance tier, optimization recommendations

## 📊 What You Get

- **Attribution Weights**: Search 64.3%, Display 35.7%
- **Customer Journey**: 9 search queries + 5 display impressions
- **Optimization Tips**: Budget allocation, creative improvements
- **Cross-Channel Insights**: Channel synergy analysis

## 🔧 Integration Examples

### JavaScript
```javascript
fetch('http://localhost:8000/comprehensive-insights/cust_001')
  .then(response => response.json())
  .then(data => console.log(data.data.unified_recommendations));
```

### Python
```python
import requests
response = requests.get('http://localhost:8000/insights/cust_001')
insights = response.json()
print(f"Customer has {insights['data']['total_searches']} searches")
```

### cURL
```bash
# Get all customer insights
curl http://localhost:8000/comprehensive-insights/cust_001 | jq '.data.unified_recommendations'
```

## 🎛️ Key Endpoints

| What You Want | Endpoint |
|---------------|----------|
| Customer search behavior | `GET /insights/{customer_id}` |
| Display ad performance | `GET /display-insights/{customer_id}` |
| Complete customer analysis | `GET /comprehensive-insights/{customer_id}` |
| Attribution calculation | `POST /unified-attribution` |
| Optimization strategy | `GET /optimize-strategy/{customer_id}` |

## ✅ Success Indicators

- Health check returns `"status": "healthy"`
- Customer insights show real data from your Snowflake database
- Attribution analysis provides realistic channel weights
- Optimization recommendations are actionable

**You're ready to use the system for real attribution analysis!**