#!/usr/bin/env python3
"""
Sample Application for Observability Demo
Generates metrics, logs, and traces for testing the AI-powered observability system
"""

import os
import time
import random
import logging
import psutil
import asyncio
from datetime import datetime
from typing import Dict, Any

import structlog
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Configure OpenTelemetry
resource = Resource.create({"service.name": "sample-app", "service.version": "1.0.0"})
trace.set_tracer_provider(TracerProvider(resource=resource))

# Configure OTLP exporter
otlp_exporter = OTLPSpanExporter(
    endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317"),
    insecure=True
)

span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

tracer = trace.get_tracer(__name__)

# Prometheus metrics
request_count = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')
cpu_usage = Gauge('cpu_usage_percent', 'CPU usage percentage')
memory_usage = Gauge('memory_usage_percent', 'Memory usage percentage')
disk_usage = Gauge('disk_usage_percent', 'Disk usage percentage')
error_count = Counter('errors_total', 'Total errors', ['type'])
active_users = Gauge('active_users', 'Number of active users')

# FastAPI app
app = FastAPI(
    title="Sample Observability Application",
    description="Demo app that generates metrics, logs, and traces",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instrument with OpenTelemetry
FastAPIInstrumentor.instrument_app(app)

# Global state
app_state = {
    "users": {},
    "orders": [],
    "products": [
        {"id": 1, "name": "Laptop", "price": 999.99},
        {"id": 2, "name": "Phone", "price": 699.99},
        {"id": 3, "name": "Tablet", "price": 399.99},
    ]
}


@app.middleware("http")
async def add_process_time_header(request, call_next):
    """Add request processing time to headers and metrics"""
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Record metrics
    request_duration.observe(process_time)
    request_count.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    return response


@app.get("/")
async def root():
    """Root endpoint"""
    logger.info("Root endpoint accessed")
    return {
        "service": "Sample Observability App",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "metrics": "/metrics",
            "users": "/users",
            "orders": "/orders",
            "products": "/products",
            "simulate": "/simulate",
            "error": "/error"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": time.time()
    }


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    # Update system metrics
    cpu_usage.set(psutil.cpu_percent())
    memory_usage.set(psutil.virtual_memory().percent)
    disk_usage.set(psutil.disk_usage('/').percent)
    active_users.set(len(app_state["users"]))
    
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


@app.get("/users")
async def get_users():
    """Get all users"""
    with tracer.start_as_current_span("get_users") as span:
        span.set_attribute("user_count", len(app_state["users"]))
        logger.info("Fetching users", count=len(app_state["users"]))
        return {"users": list(app_state["users"].values())}


@app.post("/users")
async def create_user(user_data: Dict[str, Any]):
    """Create a new user"""
    with tracer.start_as_current_span("create_user") as span:
        user_id = len(app_state["users"]) + 1
        user = {
            "id": user_id,
            "name": user_data.get("name", f"User {user_id}"),
            "email": user_data.get("email", f"user{user_id}@example.com"),
            "created_at": datetime.utcnow().isoformat()
        }
        
        app_state["users"][user_id] = user
        
        span.set_attribute("user_id", user_id)
        span.set_attribute("user_name", user["name"])
        
        logger.info("User created", user_id=user_id, name=user["name"])
        return user


@app.get("/orders")
async def get_orders():
    """Get all orders"""
    with tracer.start_as_current_span("get_orders") as span:
        span.set_attribute("order_count", len(app_state["orders"]))
        logger.info("Fetching orders", count=len(app_state["orders"]))
        return {"orders": app_state["orders"]}


@app.post("/orders")
async def create_order(order_data: Dict[str, Any]):
    """Create a new order"""
    with tracer.start_as_current_span("create_order") as span:
        # Simulate some processing time
        await asyncio.sleep(random.uniform(0.1, 0.5))
        
        order_id = len(app_state["orders"]) + 1
        order = {
            "id": order_id,
            "user_id": order_data.get("user_id", 1),
            "product_id": order_data.get("product_id", 1),
            "quantity": order_data.get("quantity", 1),
            "total": order_data.get("quantity", 1) * 99.99,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat()
        }
        
        app_state["orders"].append(order)
        
        span.set_attribute("order_id", order_id)
        span.set_attribute("user_id", order["user_id"])
        span.set_attribute("total", order["total"])
        
        logger.info("Order created", 
                   order_id=order_id, 
                   user_id=order["user_id"], 
                   total=order["total"])
        
        # Simulate order processing
        background_tasks = BackgroundTasks()
        background_tasks.add_task(process_order, order_id)
        
        return order


@app.get("/products")
async def get_products():
    """Get all products"""
    with tracer.start_as_current_span("get_products") as span:
        span.set_attribute("product_count", len(app_state["products"]))
        logger.info("Fetching products", count=len(app_state["products"]))
        return {"products": app_state["products"]}


@app.post("/simulate")
async def simulate_traffic():
    """Simulate various application scenarios"""
    with tracer.start_as_current_span("simulate_traffic") as span:
        scenarios = []
        
        # Create some users
        for i in range(random.randint(1, 5)):
            user_data = {"name": f"SimUser{i}", "email": f"sim{i}@test.com"}
            await create_user(user_data)
            scenarios.append(f"Created user: {user_data['name']}")
        
        # Create some orders
        for i in range(random.randint(1, 10)):
            order_data = {
                "user_id": random.randint(1, len(app_state["users"]) or 1),
                "product_id": random.randint(1, 3),
                "quantity": random.randint(1, 5)
            }
            await create_order(order_data)
            scenarios.append(f"Created order for user {order_data['user_id']}")
        
        # Simulate some errors
        if random.random() < 0.3:
            error_count.labels(type="simulation").inc()
            logger.error("Simulated error occurred", error_type="random_simulation")
            scenarios.append("Generated error log")
        
        span.set_attribute("scenarios_count", len(scenarios))
        logger.info("Traffic simulation completed", scenarios=len(scenarios))
        
        return {"message": "Traffic simulation completed", "scenarios": scenarios}


@app.get("/error")
async def trigger_error():
    """Trigger an intentional error for testing"""
    error_type = random.choice(["validation", "database", "network", "timeout"])
    
    error_count.labels(type=error_type).inc()
    
    with tracer.start_as_current_span("error_simulation") as span:
        span.set_attribute("error_type", error_type)
        
        if error_type == "validation":
            logger.error("Validation error", error_type=error_type, field="email")
            raise HTTPException(status_code=400, detail="Invalid email format")
        elif error_type == "database":
            logger.error("Database connection error", error_type=error_type)
            raise HTTPException(status_code=500, detail="Database connection failed")
        elif error_type == "network":
            logger.error("Network timeout error", error_type=error_type)
            raise HTTPException(status_code=503, detail="External service unavailable")
        else:
            logger.error("Request timeout error", error_type=error_type)
            raise HTTPException(status_code=408, detail="Request timeout")


async def process_order(order_id: int):
    """Background task to process an order"""
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order_id", order_id)
        
        # Find the order
        order = next((o for o in app_state["orders"] if o["id"] == order_id), None)
        if not order:
            logger.error("Order not found for processing", order_id=order_id)
            return
        
        # Simulate processing time
        processing_time = random.uniform(1, 5)
        await asyncio.sleep(processing_time)
        
        # Update order status
        order["status"] = "completed"
        order["completed_at"] = datetime.utcnow().isoformat()
        
        span.set_attribute("processing_time", processing_time)
        logger.info("Order processed successfully", 
                   order_id=order_id, 
                   processing_time=processing_time)


async def background_metrics_generator():
    """Generate background metrics for demo purposes"""
    while True:
        try:
            # Update system metrics
            cpu_usage.set(psutil.cpu_percent())
            memory_usage.set(psutil.virtual_memory().percent)
            disk_usage.set(psutil.disk_usage('/').percent)
            
            # Simulate varying active users
            current_users = len(app_state["users"])
            variation = random.randint(-2, 5)
            active_users.set(max(0, current_users + variation))
            
            # Occasionally generate some activity
            if random.random() < 0.1:  # 10% chance every interval
                logger.info("Background activity", 
                           cpu_percent=psutil.cpu_percent(),
                           memory_percent=psutil.virtual_memory().percent)
            
            await asyncio.sleep(30)  # Update every 30 seconds
            
        except Exception as e:
            logger.error("Error in background metrics", error=str(e))
            await asyncio.sleep(60)


@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    logger.info("Sample Observability App starting up")
    
    # Create some initial data
    initial_users = [
        {"name": "Alice Johnson", "email": "alice@example.com"},
        {"name": "Bob Smith", "email": "bob@example.com"},
        {"name": "Carol Davis", "email": "carol@example.com"}
    ]
    
    for user_data in initial_users:
        await create_user(user_data)
    
    # Start background metrics
    asyncio.create_task(background_metrics_generator())
    
    logger.info("Application initialized with sample data")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown"""
    logger.info("Sample Observability App shutting down")


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    log_level = os.getenv("LOG_LEVEL", "info").lower()
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        log_level=log_level,
        reload=False
    )