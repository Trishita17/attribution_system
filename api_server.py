#!/usr/bin/env python3
"""
FastAPI server for Search Attribution Agent
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from attribution_agents.agents.search_agents import SearchAttributionAgent
from attribution_agents.agents.display_agents import DisplayAttributionAgent
from attribution_agents.agent_manager import MultiAgentAttributionManager

app = FastAPI(title="Multi-Agent Attribution API")
search_agent = SearchAttributionAgent()
display_agent = DisplayAttributionAgent()
agent_manager = MultiAgentAttributionManager()

class QueryRequest(BaseModel):
    query_id: str
    customer_id: str
    query_text: str
    query_sequence_position: int = 1

class AttributionRequest(BaseModel):
    customer_id: str
    conversion_id: str

class DisplayInteractionRequest(BaseModel):
    interaction_id: str
    customer_id: str
    ad_format: str
    interaction_type: str
    timestamp: str = None

@app.post("/process-query")
async def process_query(request: QueryRequest):
    """Process a search query and classify intent"""
    try:
        result = await search_agent.process_search_query(request.dict())
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/calculate-attribution")
async def calculate_attribution(request: AttributionRequest):
    """Calculate attribution weights for customer journey"""
    try:
        result = await search_agent.calculate_attribution_weights(
            request.customer_id, 
            request.conversion_id
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/insights/{customer_id}")
async def get_insights(customer_id: str):
    """Get customer search insights"""
    try:
        result = await search_agent.get_search_insights(customer_id)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Display Agent Endpoints
@app.post("/analyze-creative-performance")
async def analyze_creative_performance(creative_id: str):
    """Analyze creative performance"""
    try:
        result = await display_agent.analyze_creative_performance(creative_id)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-video-engagement")
async def analyze_video_engagement(customer_id: str):
    """Analyze video engagement patterns"""
    try:
        result = await display_agent.analyze_video_engagement(customer_id)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/calculate-display-attribution")
async def calculate_display_attribution(request: AttributionRequest):
    """Calculate attribution weights for display journey"""
    try:
        result = await display_agent.calculate_display_attribution(
            request.customer_id, 
            request.conversion_id
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/display-insights/{customer_id}")
async def get_display_insights(customer_id: str):
    """Get customer display insights"""
    try:
        result = await display_agent.get_display_insights(customer_id)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Unified Multi-Agent Endpoints
@app.post("/unified-attribution")
async def unified_attribution(request: AttributionRequest):
    """Calculate unified attribution across search and display channels"""
    try:
        result = await agent_manager.calculate_unified_attribution(
            request.customer_id, 
            request.conversion_id
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/comprehensive-insights/{customer_id}")
async def comprehensive_insights(customer_id: str):
    """Get comprehensive insights from both search and display agents"""
    try:
        result = await agent_manager.get_comprehensive_insights(customer_id)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/optimize-strategy/{customer_id}")
async def optimize_strategy(customer_id: str, goals: str = None):
    """Generate cross-channel optimization strategy"""
    try:
        optimization_goals = goals.split(',') if goals else None
        result = await agent_manager.optimize_cross_channel_strategy(
            customer_id, 
            optimization_goals
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Cross-Channel Analysis
@app.get("/cross-channel-analysis/{customer_id}")
async def cross_channel_analysis(customer_id: str):
    """Analyze cross-channel synergy between search and display"""
    try:
        search_insights = await search_agent.get_search_insights(customer_id)
        result = await display_agent.analyze_cross_channel_synergy(customer_id, search_insights)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "database": "snowflake_connected",
        "agents": {
            "search_attribution_agent": "active",
            "display_attribution_agent": "active"
        },
        "endpoints": {
            "search": ["/process-query", "/calculate-attribution", "/insights/{customer_id}"],
            "display": ["/analyze-creative-performance", "/analyze-video-engagement", "/calculate-display-attribution", "/display-insights/{customer_id}"],
            "unified": ["/unified-attribution", "/comprehensive-insights/{customer_id}", "/optimize-strategy/{customer_id}"],
            "cross_channel": ["/cross-channel-analysis/{customer_id}"]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)