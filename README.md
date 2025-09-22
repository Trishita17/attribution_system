# Attribution System

A multi-agent attribution system with search agents and display agents for analyzing customer search behavior and calculating attribution weights.

## 🚀 Quick Start

### 1. Setup Virtual Environment
```bash
cd attribution_system
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Start the API Server
```bash
# Option 1: Using the startup script (recommended)
python start_server.py

# Option 2: Direct uvicorn command
source venv/bin/activate
uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Test the System
```bash
# In a new terminal window
cd attribution_system
source venv/bin/activate
python test_api_simple.py
```

## 📡 API Endpoints

The server runs on `http://localhost:8000` with the following endpoints:

- **Health Check**: `GET /health`
- **Process Query**: `POST /process-query`
- **Calculate Attribution**: `POST /calculate-attribution`
- **Get Insights**: `GET /insights/{customer_id}`
- **API Documentation**: `http://localhost:8000/docs`

## 🧪 Testing

### Database Connection Test
```bash
# Test Snowflake connection
python test_snowflake_connection.py
```

### API Tests
```bash
# Test API endpoints (requires server to be running)
python test_api_simple.py
```

### Agent Tests
```bash
# Run unit tests for agents
python -m pytest attribution_agents/tests/
```

### Example API Usage

#### Process a Search Query
```bash
curl -X POST "http://localhost:8000/process-query" \
  -H "Content-Type: application/json" \
  -d '{
    "query_id": "q001",
    "customer_id": "c123",
    "query_text": "best running shoes",
    "query_sequence_position": 1
  }'
```

#### Calculate Attribution
```bash
curl -X POST "http://localhost:8000/calculate-attribution" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "c123",
    "conversion_id": "conv456"
  }'
```

#### Get Customer Insights
```bash
curl "http://localhost:8000/insights/c123"
```

## 🏗️ Project Structure

```
attribution_system/
├── attribution_agents/              # Core agent modules
│   ├── agents/                     # Agent implementations
│   │   ├── __init__.py
│   │   ├── display_agents.py       # Display attribution agent
│   │   ├── display_helpers.py      # Display agent utilities
│   │   └── search_agents.py        # Search attribution agent
│   ├── config/                     # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py             # Environment settings
│   ├── data/                       # Data layer
│   │   ├── __init__.py
│   │   ├── model.py                # Data models
│   │   └── snowflake_client.py     # Database client
│   ├── llm/                        # LLM integration
│   │   ├── __init__.py
│   │   └── client.py               # Anthropic Claude client
│   ├── services/                   # Service layer
│   │   ├── __init__.py
│   │   ├── handlers.py             # Request handlers
│   │   └── server.py               # Core server logic
│   ├── tests/                      # Unit tests
│   │   ├── display_agent_test.py   # Display agent tests
│   │   └── search_agent_test.py    # Search agent tests
│   ├── .env.example                # Environment template
│   ├── agent_manager.py            # Agent coordination
│   └── requirements.txt            # Agent dependencies
├── .gitignore                      # Git ignore rules
├── api_server.py                   # FastAPI server
├── example_usage.py                # Usage examples
├── FUTURE_ENHANCEMENTS.md          # Roadmap and planned features
├── HOW_TO_USE.md                   # Usage instructions
├── QUICK_START.md                  # Quick setup guide
├── README.md                       # This file
├── requirements.txt                # Main dependencies
├── SECURITY.md                     # Security guidelines
├── setup.sh                        # Automated setup script
├── start_server.py                 # Server startup script
├── SYSTEM_FLOW_EXPLAINED.md        # Technical architecture
├── test_api_simple.py              # API integration tests
├── test_snowflake_connection.py    # Database connection test
├── use_agent.py                    # Agent usage examples
└── USER_GUIDE.md                   # Comprehensive user guide
```

## ⚙️ Configuration

### Environment Setup
1. Copy the example environment file:
   ```bash
   cp attribution_agents/.env.example attribution_agents/.env
   ```

2. Update the `.env` file with your credentials:
   - `SNOWFLAKE_ACCOUNT`: Your Snowflake account identifier
   - `SNOWFLAKE_USER`: Snowflake username
   - `SNOWFLAKE_PASSWORD`: Snowflake password (or leave empty for SSO)
   - `ANTHROPIC_API_KEY`: Your Claude API key

⚠️ **Security Note**: Never commit the `.env` file to version control. See [SECURITY.md](SECURITY.md) for detailed security guidelines.

## 🔧 Development

### Adding New Agents
1. Create agent class in `attribution_agents/agents/`
2. Implement required methods
3. Add to API endpoints in `api_server.py`

### Running in Development Mode
```bash
# Start with auto-reload
python start_server.py
```

## 📊 Features

- **Search Intent Classification**: Analyze search queries and classify intent
- **Attribution Calculation**: Calculate multi-touch attribution weights
- **Customer Insights**: Generate behavioral insights from search history
- **RESTful API**: Easy integration with external systems
- **Async Processing**: High-performance async operations

## 🛠️ Troubleshooting

### Common Issues

1. **Import Errors**: Make sure virtual environment is activated
2. **Port Already in Use**: Change port in `start_server.py` or kill existing process
3. **Database Connection**: Verify Snowflake credentials in `.env` file
4. **API Key Issues**: Check Anthropic API key is valid

### Logs
Server logs are displayed in the terminal. Check for any error messages during startup.

## 🎯 Future Enhancements

See [FUTURE_ENHANCEMENTS.md](FUTURE_ENHANCEMENTS.md) for detailed roadmap including:

- **Frontend Dashboard**: React/Vue.js dashboard for attribution analytics
- **MCP Migration**: Model Context Protocol implementation
- **Advanced Analytics**: ML-powered predictive attribution
- **Enterprise Features**: Security, scalability, and compliance
- **Integration Ecosystem**: Third-party platform integrations

## 📚 Documentation

- [Quick Start Guide](QUICK_START.md) - Get up and running quickly
- [User Guide](USER_GUIDE.md) - Comprehensive usage instructions
- [System Flow](SYSTEM_FLOW_EXPLAINED.md) - Technical architecture overview
- [Security Guidelines](SECURITY.md) - Security best practices
- [Future Enhancements](FUTURE_ENHANCEMENTS.md) - Roadmap and planned features

---

**Ready to run!** 🚀 Start with `python start_server.py` and test with `python test_api_client.py`