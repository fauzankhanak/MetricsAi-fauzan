"""
Configuration management for AI Processor Service
"""

import os
import yaml
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LLMConfig(BaseModel):
    provider: str = "openai"
    model: str = "gpt-4"
    api_key: Optional[str] = None
    temperature: float = 0.1
    max_tokens: int = 2048
    timeout: int = 30


class EmbeddingsConfig(BaseModel):
    provider: str = "openai"
    model: str = "text-embedding-ada-002"
    dimension: int = 1536
    batch_size: int = 100


class VectorDBConfig(BaseModel):
    provider: str = "qdrant"
    url: str = "http://qdrant:6333"
    collection_name: str = "observability_data"
    distance_metric: str = "cosine"


class AIConfig(BaseModel):
    llm: LLMConfig = LLMConfig()
    embeddings: EmbeddingsConfig = EmbeddingsConfig()
    vector_db: VectorDBConfig = VectorDBConfig()


class MetricsProcessingConfig(BaseModel):
    aggregation_window: str = "5m"
    retention_period: str = "7d"
    anomaly_detection: Dict[str, Any] = {
        "enabled": True,
        "sensitivity": 0.8,
        "min_samples": 100
    }
    important_metrics: list = [
        "cpu_usage_percent",
        "memory_usage_percent",
        "disk_usage_percent",
        "network_bytes_total",
        "http_request_duration",
        "http_requests_total",
        "error_rate",
        "response_time"
    ]


class LogsProcessingConfig(BaseModel):
    parsing: Dict[str, Any] = {
        "enabled": True,
        "extract_structured": True,
        "severity_detection": True
    }
    filtering: Dict[str, Any] = {
        "exclude_patterns": ["health-check", "ping", "metrics"],
        "include_severity": ["ERROR", "WARN", "FATAL"]
    }
    clustering: Dict[str, Any] = {
        "enabled": True,
        "similarity_threshold": 0.85,
        "max_clusters": 1000
    }


class TracesProcessingConfig(BaseModel):
    sampling_rate: float = 0.1
    error_traces_sampling_rate: float = 1.0
    slow_traces_threshold: str = "1s"
    analysis: Dict[str, bool] = {
        "dependency_mapping": True,
        "bottleneck_detection": True,
        "error_propagation": True
    }


class DataProcessingConfig(BaseModel):
    metrics: MetricsProcessingConfig = MetricsProcessingConfig()
    logs: LogsProcessingConfig = LogsProcessingConfig()
    traces: TracesProcessingConfig = TracesProcessingConfig()


class PerformanceAnalysisConfig(BaseModel):
    metrics_correlation: bool = True
    trend_analysis: bool = True
    capacity_planning: bool = True
    sla_monitoring: bool = True
    thresholds: Dict[str, float] = {
        "cpu_high": 80,
        "memory_high": 85,
        "disk_high": 90,
        "response_time_high": 2000,
        "error_rate_high": 5
    }


class AnomalyDetectionConfig(BaseModel):
    algorithms: list = ["isolation_forest", "local_outlier_factor", "one_class_svm"]
    sensitivity: float = 0.1
    min_anomaly_score: float = 0.5
    correlation_window: str = "1h"


class RootCauseConfig(BaseModel):
    enabled: bool = True
    correlation_threshold: float = 0.7
    time_window: str = "15m"
    max_depth: int = 5


class AnalysisConfig(BaseModel):
    performance: PerformanceAnalysisConfig = PerformanceAnalysisConfig()
    anomaly_detection: AnomalyDetectionConfig = AnomalyDetectionConfig()
    root_cause: RootCauseConfig = RootCauseConfig()


class ChatConfig(BaseModel):
    response: Dict[str, Any] = {
        "max_length": 1000,
        "include_charts": True,
        "include_metrics": True,
        "include_recommendations": True
    }
    query_processing: Dict[str, Any] = {
        "intent_classification": True,
        "entity_extraction": True,
        "context_window": 10
    }
    quick_queries: list = [
        "Show me system performance overview",
        "What are the current issues?",
        "Analyze recent errors",
        "Show me slow requests",
        "Performance trends in the last hour",
        "Resource utilization summary"
    ]


class DataSourceConfig(BaseModel):
    prometheus: Dict[str, Any] = {
        "url": "http://prometheus:9090",
        "timeout": 30,
        "max_points": 10000
    }
    elasticsearch: Dict[str, Any] = {
        "url": "http://elasticsearch:9200",
        "timeout": 30,
        "max_results": 1000,
        "indices": {
            "logs": "observability-logs",
            "traces": "observability-traces"
        }
    }
    jaeger: Dict[str, Any] = {
        "url": "http://jaeger:16686",
        "timeout": 30,
        "max_traces": 100
    }


class CacheConfig(BaseModel):
    redis: Dict[str, Any] = {
        "enabled": False,
        "url": "redis://redis:6379"
    }
    memory: Dict[str, Any] = {
        "enabled": True,
        "max_size_mb": 512,
        "ttl_seconds": 300
    }


class MonitoringConfig(BaseModel):
    metrics_port: int = 5001
    health_check_port: int = 5002
    log_level: str = "INFO"
    telemetry: Dict[str, Any] = {
        "enabled": True,
        "export_interval": "30s"
    }


class Config:
    """Main configuration class"""
    
    def __init__(self, config_file: str = "/app/config.yml"):
        self.config_file = config_file
        self._config_data = self._load_config()
        
        # Initialize configuration sections
        self.ai = AIConfig(**self._config_data.get("ai", {}))
        self.data_processing = DataProcessingConfig(**self._config_data.get("data_processing", {}))
        self.analysis = AnalysisConfig(**self._config_data.get("analysis", {}))
        self.chat = ChatConfig(**self._config_data.get("chat", {}))
        self.data_sources = DataSourceConfig(**self._config_data.get("data_sources", {}))
        self.cache = CacheConfig(**self._config_data.get("cache", {}))
        self.monitoring = MonitoringConfig(**self._config_data.get("monitoring", {}))
        
        # Override with environment variables
        self._apply_env_overrides()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(self.config_file, 'r') as f:
                config_data = yaml.safe_load(f)
            return config_data or {}
        except FileNotFoundError:
            # Return default configuration if file doesn't exist
            return {}
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML configuration: {e}")
    
    def _apply_env_overrides(self):
        """Apply environment variable overrides"""
        # OpenAI API Key
        if os.getenv("OPENAI_API_KEY"):
            self.ai.llm.api_key = os.getenv("OPENAI_API_KEY")
        
        # Data source URLs
        if os.getenv("PROMETHEUS_URL"):
            self.data_sources.prometheus["url"] = os.getenv("PROMETHEUS_URL")
        
        if os.getenv("ELASTICSEARCH_URL"):
            self.data_sources.elasticsearch["url"] = os.getenv("ELASTICSEARCH_URL")
        
        if os.getenv("JAEGER_URL"):
            self.data_sources.jaeger["url"] = os.getenv("JAEGER_URL")
        
        if os.getenv("QDRANT_URL"):
            self.ai.vector_db.url = os.getenv("QDRANT_URL")
        
        # Monitoring configuration
        if os.getenv("LOG_LEVEL"):
            self.monitoring.log_level = os.getenv("LOG_LEVEL").upper()
        
        if os.getenv("METRICS_PORT"):
            self.monitoring.metrics_port = int(os.getenv("METRICS_PORT"))
        
        if os.getenv("HEALTH_CHECK_PORT"):
            self.monitoring.health_check_port = int(os.getenv("HEALTH_CHECK_PORT"))
    
    def get_llm_config(self) -> Dict[str, Any]:
        """Get LLM configuration as dictionary"""
        return self.ai.llm.model_dump()
    
    def get_embeddings_config(self) -> Dict[str, Any]:
        """Get embeddings configuration as dictionary"""
        return self.ai.embeddings.model_dump()
    
    def get_vector_db_config(self) -> Dict[str, Any]:
        """Get vector database configuration as dictionary"""
        return self.ai.vector_db.model_dump()
    
    def get_data_source_config(self, source: str) -> Dict[str, Any]:
        """Get configuration for a specific data source"""
        return getattr(self.data_sources, source, {})
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert entire configuration to dictionary"""
        return {
            "ai": self.ai.model_dump(),
            "data_processing": self.data_processing.model_dump(),
            "analysis": self.analysis.model_dump(),
            "chat": self.chat.model_dump(),
            "data_sources": self.data_sources.model_dump(),
            "cache": self.cache.model_dump(),
            "monitoring": self.monitoring.model_dump()
        }