#!/usr/bin/env python3
"""
Chat API Service for Observability Platform
Provides REST and WebSocket APIs for chat functionality
"""

import os
import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from contextlib import asynccontextmanager

import structlog
import uvicorn
import httpx
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Metrics
chat_requests_total = Counter('chat_requests_total', 'Total chat requests', ['status'])
chat_response_duration = Histogram('chat_response_duration_seconds', 'Chat response duration')
websocket_connections = Counter('websocket_connections_total', 'Total WebSocket connections')

# Global configuration
AI_PROCESSOR_URL = os.getenv("AI_PROCESSOR_URL", "http://ai-processor:5000")
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://prometheus:9090")
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://elasticsearch:9200")
JAEGER_URL = os.getenv("JAEGER_URL", "http://jaeger:16686")

# Global HTTP client
http_client: Optional[httpx.AsyncClient] = None

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_sessions: Dict[str, Dict] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.user_sessions[session_id] = {
            "websocket": websocket,
            "connected_at": datetime.utcnow(),
            "message_count": 0,
            "context": []
        }
        websocket_connections.inc()
        logger.info("WebSocket connection established", session_id=session_id)

    def disconnect(self, websocket: WebSocket, session_id: str):
        self.active_connections.remove(websocket)
        if session_id in self.user_sessions:
            del self.user_sessions[session_id]
        logger.info("WebSocket connection closed", session_id=session_id)

    async def send_personal_message(self, message: dict, session_id: str):
        if session_id in self.user_sessions:
            websocket = self.user_sessions[session_id]["websocket"]
            await websocket.send_text(json.dumps(message))

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))

manager = ConnectionManager()


# Pydantic models
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    context: Optional[Dict] = None
    include_metrics: bool = True
    include_logs: bool = True
    include_traces: bool = True
    time_range: str = "1h"


class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: datetime
    metadata: Optional[Dict] = None
    suggestions: Optional[List[str]] = None


class SystemStatus(BaseModel):
    status: str
    services: Dict[str, Any]
    timestamp: datetime


class QuickQuery(BaseModel):
    query: str
    description: str
    category: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global http_client
    
    # Initialize HTTP client
    http_client = httpx.AsyncClient(timeout=30.0)
    logger.info("Chat API service started")
    
    yield
    
    # Cleanup
    if http_client:
        await http_client.aclose()
    logger.info("Chat API service shut down")


# Create FastAPI app
app = FastAPI(
    title="Chat API Service",
    description="REST and WebSocket API for observability chat interface",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check AI processor connection
        ai_health = await check_service_health(f"{AI_PROCESSOR_URL}/health")
        
        # Check data sources
        prometheus_health = await check_service_health(f"{PROMETHEUS_URL}/-/healthy")
        elasticsearch_health = await check_service_health(f"{ELASTICSEARCH_URL}/_cluster/health")
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow(),
            "services": {
                "ai_processor": ai_health,
                "prometheus": prometheus_health,
                "elasticsearch": elasticsearch_health
            },
            "active_connections": len(manager.active_connections),
            "total_sessions": len(manager.user_sessions)
        }
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        raise HTTPException(status_code=503, detail="Service unhealthy")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Chat API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "chat": "/chat",
            "ws": "/ws/{session_id}",
            "status": "/status",
            "quick_queries": "/quick-queries"
        }
    }


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(message: ChatMessage):
    """Process chat message via REST API"""
    start_time = datetime.utcnow()
    
    try:
        # Generate session ID if not provided
        session_id = message.session_id or f"rest_{int(datetime.utcnow().timestamp())}"
        
        logger.info("Processing chat message", session_id=session_id, message=message.message[:100])
        
        # Send request to AI processor
        ai_request = {
            "query": message.message,
            "context": message.context,
            "include_metrics": message.include_metrics,
            "include_logs": message.include_logs,
            "include_traces": message.include_traces,
            "time_range": message.time_range
        }
        
        response = await http_client.post(
            f"{AI_PROCESSOR_URL}/query",
            json=ai_request,
            timeout=60.0
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"AI processor error: {response.text}"
            )
        
        ai_response = response.json()
        
        # Record metrics
        duration = (datetime.utcnow() - start_time).total_seconds()
        chat_response_duration.observe(duration)
        chat_requests_total.labels(status="success").inc()
        
        # Create response
        chat_response = ChatResponse(
            response=ai_response.get("response", "No response available"),
            session_id=session_id,
            timestamp=datetime.utcnow(),
            metadata=ai_response.get("metadata"),
            suggestions=ai_response.get("suggestions", [])
        )
        
        logger.info("Chat message processed successfully", session_id=session_id)
        return chat_response
        
    except Exception as e:
        chat_requests_total.labels(status="error").inc()
        logger.error("Error processing chat message", error=str(e), session_id=session_id)
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time chat"""
    await manager.connect(websocket, session_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Update session context
            if session_id in manager.user_sessions:
                manager.user_sessions[session_id]["message_count"] += 1
                manager.user_sessions[session_id]["context"].append({
                    "user": message_data.get("message"),
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            # Process message
            try:
                ai_request = {
                    "query": message_data.get("message"),
                    "context": message_data.get("context"),
                    "include_metrics": message_data.get("include_metrics", True),
                    "include_logs": message_data.get("include_logs", True),
                    "include_traces": message_data.get("include_traces", True),
                    "time_range": message_data.get("time_range", "1h")
                }
                
                response = await http_client.post(
                    f"{AI_PROCESSOR_URL}/query",
                    json=ai_request,
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    ai_response = response.json()
                    
                    # Send response back to client
                    ws_response = {
                        "type": "response",
                        "response": ai_response.get("response"),
                        "metadata": ai_response.get("metadata"),
                        "suggestions": ai_response.get("suggestions", []),
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    
                    await manager.send_personal_message(ws_response, session_id)
                    
                    # Update session context
                    if session_id in manager.user_sessions:
                        manager.user_sessions[session_id]["context"].append({
                            "assistant": ai_response.get("response"),
                            "timestamp": datetime.utcnow().isoformat()
                        })
                    
                    chat_requests_total.labels(status="success").inc()
                    
                else:
                    error_response = {
                        "type": "error",
                        "error": f"AI processor error: {response.text}",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    await manager.send_personal_message(error_response, session_id)
                    chat_requests_total.labels(status="error").inc()
                    
            except Exception as e:
                error_response = {
                    "type": "error",
                    "error": f"Processing error: {str(e)}",
                    "timestamp": datetime.utcnow().isoformat()
                }
                await manager.send_personal_message(error_response, session_id)
                chat_requests_total.labels(status="error").inc()
                logger.error("WebSocket message processing error", error=str(e), session_id=session_id)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)


@app.get("/status", response_model=SystemStatus)
async def system_status():
    """Get overall system status"""
    try:
        # Get status from various services
        services = {}
        
        # AI Processor status
        try:
            ai_response = await http_client.get(f"{AI_PROCESSOR_URL}/health")
            services["ai_processor"] = {
                "status": "healthy" if ai_response.status_code == 200 else "unhealthy",
                "response_time": ai_response.elapsed.total_seconds()
            }
        except:
            services["ai_processor"] = {"status": "unreachable"}
        
        # Data sources status
        for name, url in [
            ("prometheus", f"{PROMETHEUS_URL}/-/healthy"),
            ("elasticsearch", f"{ELASTICSEARCH_URL}/_cluster/health")
        ]:
            try:
                response = await http_client.get(url)
                services[name] = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "response_time": response.elapsed.total_seconds()
                }
            except:
                services[name] = {"status": "unreachable"}
        
        overall_status = "healthy" if all(
            s.get("status") == "healthy" for s in services.values()
        ) else "degraded"
        
        return SystemStatus(
            status=overall_status,
            services=services,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error("Error getting system status", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get system status")


@app.get("/quick-queries", response_model=List[QuickQuery])
async def get_quick_queries():
    """Get predefined quick queries"""
    return [
        QuickQuery(
            query="Show me system performance overview",
            description="Get an overview of current system performance metrics",
            category="performance"
        ),
        QuickQuery(
            query="What are the current issues?",
            description="Identify any ongoing issues or anomalies",
            category="troubleshooting"
        ),
        QuickQuery(
            query="Analyze recent errors",
            description="Review and analyze recent error logs",
            category="troubleshooting"
        ),
        QuickQuery(
            query="Show me slow requests",
            description="Find requests with high response times",
            category="performance"
        ),
        QuickQuery(
            query="Performance trends in the last hour",
            description="View performance trends over the past hour",
            category="analysis"
        ),
        QuickQuery(
            query="Resource utilization summary",
            description="Get CPU, memory, and disk usage summary",
            category="monitoring"
        ),
        QuickQuery(
            query="Top error patterns",
            description="Show the most common error patterns",
            category="troubleshooting"
        ),
        QuickQuery(
            query="Database performance metrics",
            description="Review database performance and query times",
            category="performance"
        )
    ]


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()


async def check_service_health(url: str) -> Dict[str, Any]:
    """Check health of a service"""
    try:
        response = await http_client.get(url, timeout=5.0)
        return {
            "status": "healthy" if response.status_code == 200 else "unhealthy",
            "response_time": response.elapsed.total_seconds(),
            "status_code": response.status_code
        }
    except Exception as e:
        return {
            "status": "unreachable",
            "error": str(e)
        }


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    log_level = os.getenv("LOG_LEVEL", "info").lower()
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=False
    )