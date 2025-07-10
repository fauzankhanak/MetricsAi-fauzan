#!/usr/bin/env python3
"""
AI Intelligence Enhancement Script
Imports historical data and enhances AI system intelligence
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add the services directory to the path
sys.path.append(str(Path(__file__).parent.parent / "services" / "ai-processor" / "src"))

from intelligence_enhancer import IntelligenceEnhancer, EnvironmentLearner


def load_historical_incidents(file_path: str) -> List[Dict[str, Any]]:
    """Load historical incidents from JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Invalid JSON in file: {file_path}")
        return []


def load_metrics_history(file_path: str) -> List[Dict[str, Any]]:
    """Load historical metrics for baseline learning"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []


def enhance_with_domain_knowledge():
    """Add observability domain knowledge to the system"""
    
    domain_knowledge = {
        "architecture_patterns": {
            "microservices": {
                "common_issues": [
                    "Service discovery failures",
                    "Network partitions",
                    "Cascade failures",
                    "Circuit breaker activation"
                ],
                "monitoring_focus": [
                    "Service-to-service latency",
                    "Request success rates",
                    "Service dependency health",
                    "Resource utilization per service"
                ]
            },
            "monolith": {
                "common_issues": [
                    "Memory leaks",
                    "Database connection exhaustion",
                    "Thread pool saturation",
                    "Single points of failure"
                ],
                "monitoring_focus": [
                    "Overall application health",
                    "Database performance",
                    "JVM metrics",
                    "Application server metrics"
                ]
            }
        },
        
        "technology_patterns": {
            "kubernetes": {
                "common_issues": [
                    "Pod restarts and crashes",
                    "Resource limits exceeded",
                    "Node resource exhaustion",
                    "Network policy issues"
                ],
                "solutions": [
                    "Adjust resource requests/limits",
                    "Implement horizontal pod autoscaling",
                    "Monitor node health",
                    "Review network policies"
                ]
            },
            "docker": {
                "common_issues": [
                    "Container memory limits",
                    "Image size optimization",
                    "Volume mount issues",
                    "Network connectivity"
                ],
                "solutions": [
                    "Optimize container resource usage",
                    "Use multi-stage builds",
                    "Monitor container metrics",
                    "Implement health checks"
                ]
            }
        },
        
        "database_patterns": {
            "postgresql": {
                "common_issues": [
                    "Connection pool exhaustion",
                    "Lock contention",
                    "Slow query performance",
                    "Vacuum/analyze issues"
                ],
                "solutions": [
                    "Tune connection pool settings",
                    "Optimize query performance",
                    "Monitor lock waits",
                    "Configure auto-vacuum properly"
                ]
            },
            "mysql": {
                "common_issues": [
                    "InnoDB buffer pool sizing",
                    "Query cache effectiveness",
                    "Replication lag",
                    "Table lock contention"
                ],
                "solutions": [
                    "Optimize buffer pool size",
                    "Review query cache configuration",
                    "Monitor replication health",
                    "Use appropriate storage engines"
                ]
            }
        }
    }
    
    # Save domain knowledge
    config_path = Path("config/ai-domain-knowledge.json")
    config_path.parent.mkdir(exist_ok=True)
    
    with open(config_path, 'w') as f:
        json.dump(domain_knowledge, f, indent=2)
    
    print(f"✅ Domain knowledge saved to {config_path}")
    return domain_knowledge


def generate_sample_incidents() -> List[Dict[str, Any]]:
    """Generate sample incidents for testing"""
    
    sample_incidents = [
        {
            "id": "INC-001",
            "title": "High CPU usage on UserService",
            "timestamp": "2024-01-15T10:30:00Z",
            "symptoms": ["high_cpu", "slow_response", "user_complaints"],
            "metrics": {
                "cpu": 92,
                "memory": 78,
                "latency": 3200,
                "error_rate": 2.1
            },
            "root_cause": "Inefficient query causing CPU spike during peak hours",
            "solution": "Optimized database query and added proper indexing",
            "prevention": [
                "Implement query performance monitoring",
                "Add database query review to deployment process",
                "Set up proactive CPU alerts at 80% threshold"
            ],
            "duration_minutes": 45,
            "impact": "High - 15% of users experienced slow responses"
        },
        
        {
            "id": "INC-002", 
            "title": "Memory leak in PaymentService",
            "timestamp": "2024-01-20T14:15:00Z",
            "symptoms": ["memory_climb", "frequent_restarts", "oom_errors"],
            "metrics": {
                "cpu": 45,
                "memory": 95,
                "latency": 1200,
                "error_rate": 8.5
            },
            "root_cause": "Unclosed HTTP connections in payment processing",
            "solution": "Fixed connection cleanup in finally blocks",
            "prevention": [
                "Implement connection monitoring",
                "Add resource leak detection tests",
                "Configure proper connection timeouts"
            ],
            "duration_minutes": 120,
            "impact": "Critical - Payment processing was intermittently failing"
        },
        
        {
            "id": "INC-003",
            "title": "Database connection pool exhaustion", 
            "timestamp": "2024-01-25T09:45:00Z",
            "symptoms": ["connection_timeouts", "database_errors", "slow_queries"],
            "metrics": {
                "cpu": 55,
                "memory": 70,
                "latency": 5000,
                "error_rate": 12.3,
                "db_connections": 500,
                "db_max_connections": 500
            },
            "root_cause": "Sudden traffic spike exceeded database connection limit",
            "solution": "Increased connection pool size and implemented connection pooling optimization",
            "prevention": [
                "Monitor connection pool utilization",
                "Implement adaptive connection scaling",
                "Add alerts for connection pool usage > 80%"
            ],
            "duration_minutes": 30,
            "impact": "Medium - Some requests failed but most users unaffected"
        },
        
        {
            "id": "INC-004",
            "title": "Cascade failure from upstream service",
            "timestamp": "2024-02-01T16:20:00Z", 
            "symptoms": ["error_spike", "timeout_increase", "service_degradation"],
            "metrics": {
                "cpu": 25,
                "memory": 55,
                "latency": 8000,
                "error_rate": 25.8
            },
            "root_cause": "Upstream authentication service failure caused timeouts across all services",
            "solution": "Implemented circuit breaker pattern and fallback mechanisms",
            "prevention": [
                "Add circuit breakers to all external service calls",
                "Implement graceful degradation",
                "Set up cross-service dependency monitoring"
            ],
            "duration_minutes": 90,
            "impact": "High - Multiple services affected, significant user impact"
        }
    ]
    
    return sample_incidents


def generate_sample_metrics() -> List[Dict[str, Any]]:
    """Generate sample metrics history for baseline learning"""
    
    import random
    from datetime import timedelta
    
    base_time = datetime.now() - timedelta(days=30)
    metrics_history = []
    
    for i in range(30 * 24):  # 30 days of hourly metrics
        timestamp = base_time + timedelta(hours=i)
        
        # Simulate normal patterns with some variations
        hour = timestamp.hour
        is_business_hours = 9 <= hour <= 17
        is_weekend = timestamp.weekday() >= 5
        
        # Base values during business hours vs off hours
        base_cpu = 45 if is_business_hours and not is_weekend else 25
        base_memory = 60 if is_business_hours and not is_weekend else 40
        base_latency = 150 if is_business_hours and not is_weekend else 80
        base_error_rate = 0.5 if is_business_hours and not is_weekend else 0.1
        
        # Add some randomness
        cpu = max(10, min(95, base_cpu + random.randint(-15, 15)))
        memory = max(20, min(90, base_memory + random.randint(-10, 10)))
        latency = max(50, min(3000, base_latency + random.randint(-50, 100)))
        error_rate = max(0, min(10, base_error_rate + random.uniform(-0.3, 0.8)))
        
        metrics_history.append({
            "timestamp": timestamp.isoformat(),
            "cpu": cpu,
            "memory": memory, 
            "latency": latency,
            "error_rate": error_rate,
            "requests_per_second": random.randint(10, 100),
            "active_connections": random.randint(50, 300)
        })
    
    return metrics_history


def train_ai_system(incidents_file: str = None, metrics_file: str = None):
    """Train the AI system with historical data"""
    
    print("🚀 Starting AI Intelligence Enhancement...")
    
    # Initialize the intelligence enhancer
    enhancer = IntelligenceEnhancer()
    learner = enhancer.environment_learner
    
    # Load or generate historical incidents
    if incidents_file:
        incidents = load_historical_incidents(incidents_file)
        print(f"📚 Loaded {len(incidents)} incidents from {incidents_file}")
    else:
        incidents = generate_sample_incidents()
        print(f"📚 Generated {len(incidents)} sample incidents for training")
    
    # Load or generate metrics history
    if metrics_file:
        metrics_history = load_metrics_history(metrics_file)
        print(f"📊 Loaded {len(metrics_history)} metric samples from {metrics_file}")
    else:
        metrics_history = generate_sample_metrics()
        print(f"📊 Generated {len(metrics_history)} metric samples for training")
    
    # Learn baselines from metrics history
    print("\n🎯 Learning environment baselines...")
    baselines = learner.learn_baselines(metrics_history)
    
    print("Learned baselines:")
    for metric, baseline in baselines.items():
        if isinstance(baseline, dict):
            print(f"  {metric}: {baseline.get('normal_range', 'N/A')} (median: {baseline.get('median', 'N/A')})")
    
    # Learn patterns from incidents
    print("\n🧠 Learning from historical incidents...")
    for incident in incidents:
        learner.learn_from_incident(incident)
    
    print(f"Learned {len(learner.patterns)} incident patterns:")
    for pattern_key, pattern_data in learner.patterns.items():
        print(f"  {pattern_key}: {pattern_data['root_cause']} (confidence: {pattern_data['confidence']:.2f})")
    
    # Add domain knowledge
    print("\n📖 Adding observability domain knowledge...")
    domain_knowledge = enhance_with_domain_knowledge()
    
    # Save the trained model data
    model_data = {
        "baselines": baselines,
        "learned_patterns": learner.patterns,
        "incident_history": learner.incidents,
        "domain_knowledge": domain_knowledge,
        "training_timestamp": datetime.utcnow().isoformat(),
        "training_stats": {
            "incidents_processed": len(incidents),
            "metrics_samples": len(metrics_history),
            "patterns_learned": len(learner.patterns)
        }
    }
    
    model_path = Path("data/ai-intelligence-model.json")
    model_path.parent.mkdir(exist_ok=True)
    
    with open(model_path, 'w') as f:
        json.dump(model_data, f, indent=2, default=str)
    
    print(f"\n✅ AI intelligence model saved to {model_path}")
    
    # Test the enhanced AI
    print("\n🧪 Testing enhanced AI intelligence...")
    test_enhanced_ai(enhancer)
    
    print("\n🎉 AI Intelligence Enhancement Complete!")
    print("\n📝 Next steps:")
    print("1. Restart the AI processor service to load the new intelligence")
    print("2. Test the system with questions like:")
    print("   - 'Why is my CPU high?'")
    print("   - 'What should I check for memory issues?'")
    print("   - 'Analyze this error pattern for me'")
    print("3. The AI will now provide much more intelligent responses!")


def test_enhanced_ai(enhancer: IntelligenceEnhancer):
    """Test the enhanced AI with sample scenarios"""
    
    test_scenarios = [
        {
            "name": "High CPU scenario",
            "metrics": {"cpu": 92, "memory": 78, "latency": 3200, "error_rate": 2.1},
            "logs": ["UserService: Query execution time exceeded 3000ms", "High CPU usage detected"],
            "traces": [{"service": "UserService", "operation": "getUserData", "duration": 3200}],
            "query": "Why is my CPU so high?"
        },
        {
            "name": "Memory pressure scenario", 
            "metrics": {"cpu": 85, "memory": 94, "latency": 1500, "error_rate": 1.2},
            "logs": ["GC pressure detected", "Memory usage above threshold"],
            "traces": [{"service": "PaymentService", "operation": "processPayment", "duration": 1500}],
            "query": "Memory usage is very high, what should I do?"
        },
        {
            "name": "Database bottleneck scenario",
            "metrics": {"cpu": 55, "memory": 70, "latency": 5000, "error_rate": 12.3, "db_connections": 495},
            "logs": ["Database connection timeout", "Connection pool exhausted"],
            "traces": [{"service": "UserService", "operation": "database_query", "duration": 5000}],
            "query": "Database queries are timing out"
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n🧪 Testing: {scenario['name']}")
        
        response = enhancer.analyze_performance_issue(
            scenario['metrics'],
            scenario['logs'], 
            scenario['traces'],
            scenario['query']
        )
        
        print(f"Analysis: {response.get('analysis', {}).get('primary_root_cause', 'No root cause identified')}")
        print(f"Confidence: {response.get('analysis', {}).get('confidence', 0) * 100:.1f}%")
        print(f"Immediate actions: {len(response.get('immediate_actions', []))} suggested")


def import_your_incidents(file_path: str):
    """Import your actual incidents from a JSON file"""
    
    print(f"📥 Importing incidents from {file_path}...")
    
    # Expected format for incidents file:
    sample_format = {
        "incidents": [
            {
                "title": "Incident title",
                "timestamp": "2024-01-15T10:30:00Z",
                "symptoms": ["symptom1", "symptom2"], 
                "metrics": {"cpu": 90, "memory": 80},
                "root_cause": "Description of root cause",
                "solution": "What fixed the issue",
                "prevention": ["prevention step 1", "prevention step 2"]
            }
        ]
    }
    
    if not Path(file_path).exists():
        print(f"❌ File not found: {file_path}")
        print("\n📝 Expected file format:")
        print(json.dumps(sample_format, indent=2))
        
        # Create a sample file
        sample_file = Path("sample_incidents.json")
        with open(sample_file, 'w') as f:
            json.dump(sample_format, f, indent=2)
        print(f"\n📁 Sample file created: {sample_file}")
        return
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        incidents = data.get('incidents', [])
        if not incidents:
            print("❌ No incidents found in file")
            return
        
        # Train the system
        train_ai_system(incidents_file=file_path)
        
    except Exception as e:
        print(f"❌ Error importing incidents: {e}")


def main():
    parser = argparse.ArgumentParser(description="Enhance AI Intelligence")
    parser.add_argument('--incidents', help='Path to incidents JSON file')
    parser.add_argument('--metrics', help='Path to metrics history JSON file')
    parser.add_argument('--demo', action='store_true', help='Run with sample data')
    parser.add_argument('--import-incidents', help='Import your incidents from JSON file')
    
    args = parser.parse_args()
    
    if args.import_incidents:
        import_your_incidents(args.import_incidents)
    elif args.demo:
        train_ai_system()
    else:
        train_ai_system(args.incidents, args.metrics)


if __name__ == "__main__":
    main()