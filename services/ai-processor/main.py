#!/usr/bin/env python3
"""
AI Processor Service for Observability Platform
Handles data processing, AI analysis, and intelligent insights
"""

import asyncio
import logging
import os
import sys
from contextlib import asynccontextmanager
from typing import Dict, List, Optional

import structlog
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.config import Config
from src.data_sources import DataSourceManager
from src.ai_engine import AIEngine
from src.vector_store import VectorStore
from src.processors import DataProcessor
from src.analytics import AnalyticsEngine
from src.telemetry import setup_telemetry
from src.health import HealthChecker

# Intelligence enhancer import
try:
    from src.intelligence_enhancer import IntelligenceEnhancer, enhance_ai_response
    INTELLIGENCE_ENHANCER_AVAILABLE = True
except ImportError:
    INTELLIGENCE_ENHANCER_AVAILABLE = False

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

# Global components
config: Optional[Config] = None
data_source_manager: Optional[DataSourceManager] = None
ai_engine: Optional[AIEngine] = None
vector_store: Optional[VectorStore] = None
data_processor: Optional[DataProcessor] = None
analytics_engine: Optional[AnalyticsEngine] = None
health_checker: Optional[HealthChecker] = None


class QueryRequest(BaseModel):
    query: str
    context: Optional[Dict] = None
    include_metrics: bool = True
    include_logs: bool = True
    include_traces: bool = True
    time_range: Optional[str] = "1h"


class AnalysisRequest(BaseModel):
    type: str  # "performance", "anomaly", "root_cause"
    parameters: Optional[Dict] = None
    time_range: Optional[str] = "1h"


class ProcessDataRequest(BaseModel):
    data_type: str  # "metrics", "logs", "traces"
    data: Dict
    source: Optional[str] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global config, data_source_manager, ai_engine, vector_store, data_processor, analytics_engine, health_checker
    
    try:
        # Initialize configuration
        config = Config()
        logger.info("Configuration loaded", config_file=config.config_file)
        
        # Setup telemetry
        setup_telemetry(config)
        logger.info("Telemetry configured")
        
        # Initialize vector store
        vector_store = VectorStore(config)
        await vector_store.initialize()
        logger.info("Vector store initialized")
        
        # Initialize data sources
        data_source_manager = DataSourceManager(config)
        await data_source_manager.initialize()
        logger.info("Data source manager initialized")
        
        # Initialize AI engine
        ai_engine = AIEngine(config, vector_store)
        await ai_engine.initialize()
        logger.info("AI engine initialized")
        
        # Initialize data processor
        data_processor = DataProcessor(config, vector_store)
        await data_processor.initialize()
        logger.info("Data processor initialized")
        
        # Initialize analytics engine
        analytics_engine = AnalyticsEngine(config, data_source_manager)
        await analytics_engine.initialize()
        logger.info("Analytics engine initialized")
        
        # Initialize health checker
        health_checker = HealthChecker(config, {
            'data_source_manager': data_source_manager,
            'ai_engine': ai_engine,
            'vector_store': vector_store,
            'analytics_engine': analytics_engine
        })
        
        # Start background tasks
        asyncio.create_task(background_data_processing())
        asyncio.create_task(background_analytics())
        
        logger.info("AI Processor service started successfully")
        
        yield
        
    except Exception as e:
        logger.error("Failed to initialize AI Processor service", error=str(e))
        sys.exit(1)
    
    finally:
        # Cleanup
        if vector_store:
            await vector_store.close()
        if data_source_manager:
            await data_source_manager.close()
        if ai_engine:
            await ai_engine.close()
        if analytics_engine:
            await analytics_engine.close()
        
        logger.info("AI Processor service shut down")


# Create FastAPI app
app = FastAPI(
    title="AI Processor Service",
    description="AI-powered observability data processing and analysis",
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
    if not health_checker:
        raise HTTPException(status_code=503, detail="Service not ready")
    
    health_status = await health_checker.check_health()
    
    if health_status["status"] == "healthy":
        return health_status
    else:
        raise HTTPException(status_code=503, detail=health_status)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "AI Processor",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "query": "/query",
            "analyze": "/analyze",
            "process": "/process",
            "metrics": "/metrics"
        }
    }


@app.post("/query")
async def query_system(request: QueryRequest):
    """Process natural language queries about system performance"""
    try:
        if not ai_engine:
            raise HTTPException(status_code=503, detail="AI engine not available")
        
        logger.info("Processing query", query=request.query)
        
        # Get relevant data based on query context
        context_data = await data_source_manager.get_context_data(
            time_range=request.time_range,
            include_metrics=request.include_metrics,
            include_logs=request.include_logs,
            include_traces=request.include_traces
        )
        
        # Process query with AI engine
        response = await ai_engine.process_query(
            query=request.query,
            context=context_data,
            user_context=request.context
        )
        
        logger.info("Query processed successfully", query=request.query)
        return response
        
    except Exception as e:
        logger.error("Error processing query", error=str(e), query=request.query)
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")


@app.post("/analyze")
async def analyze_system(request: AnalysisRequest):
    """Perform specific types of analysis on system data"""
    try:
        if not analytics_engine:
            raise HTTPException(status_code=503, detail="Analytics engine not available")
        
        logger.info("Starting analysis", type=request.type, time_range=request.time_range)
        
        # Perform analysis based on type
        if request.type == "performance":
            result = await analytics_engine.analyze_performance(
                time_range=request.time_range,
                parameters=request.parameters
            )
        elif request.type == "anomaly":
            result = await analytics_engine.detect_anomalies(
                time_range=request.time_range,
                parameters=request.parameters
            )
        elif request.type == "root_cause":
            result = await analytics_engine.analyze_root_cause(
                time_range=request.time_range,
                parameters=request.parameters
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unknown analysis type: {request.type}")
        
        logger.info("Analysis completed", type=request.type)
        return result
        
    except Exception as e:
        logger.error("Error during analysis", error=str(e), type=request.type)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/process")
async def process_data(request: ProcessDataRequest, background_tasks: BackgroundTasks):
    """Process incoming observability data"""
    try:
        if not data_processor:
            raise HTTPException(status_code=503, detail="Data processor not available")
        
        logger.info("Processing data", type=request.data_type, source=request.source)
        
        # Add processing task to background
        background_tasks.add_task(
            data_processor.process_data,
            data_type=request.data_type,
            data=request.data,
            source=request.source
        )
        
        return {"status": "accepted", "message": "Data processing started"}
        
    except Exception as e:
        logger.error("Error processing data", error=str(e), type=request.data_type)
        raise HTTPException(status_code=500, detail=f"Data processing failed: {str(e)}")


@app.get("/metrics")
async def get_metrics():
    """Get system metrics and statistics"""
    try:
        if not analytics_engine:
            raise HTTPException(status_code=503, detail="Analytics engine not available")
        
        metrics = await analytics_engine.get_system_metrics()
        return metrics
        
    except Exception as e:
        logger.error("Error getting metrics", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to get metrics: {str(e)}")


async def background_data_processing():
    """Background task for continuous data processing"""
    while True:
        try:
            await asyncio.sleep(60)  # Process every minute
            
            if data_processor and data_source_manager:
                # Get recent data from all sources
                recent_data = await data_source_manager.get_recent_data()
                
                # Process the data
                await data_processor.process_batch(recent_data)
                
                logger.debug("Background data processing completed")
                
        except Exception as e:
            logger.error("Error in background data processing", error=str(e))
            await asyncio.sleep(30)  # Wait before retry


async def background_analytics():
    """Background task for continuous analytics"""
    while True:
        try:
            await asyncio.sleep(300)  # Analyze every 5 minutes
            
            if analytics_engine:
                # Perform routine analytics
                await analytics_engine.routine_analysis()
                
                logger.debug("Background analytics completed")
                
        except Exception as e:
            logger.error("Error in background analytics", error=str(e))
            await asyncio.sleep(60)  # Wait before retry


if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    log_level = os.getenv("LOG_LEVEL", "info").lower()
    
    # Run the application
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=False,
        access_log=True
    )