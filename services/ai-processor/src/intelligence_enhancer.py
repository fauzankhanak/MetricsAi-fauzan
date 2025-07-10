#!/usr/bin/env python3
"""
Intelligence Enhancer for AI Processor
Adds observability-specific knowledge and pattern recognition to make AI smarter
"""

import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import structlog

logger = structlog.get_logger()


@dataclass
class Pattern:
    """Represents a detected pattern in observability data"""
    name: str
    confidence: float
    symptoms: List[str]
    root_cause: str
    solutions: List[str]
    prevention: List[str]


class ObservabilityKnowledgeBase:
    """Built-in observability expertise for smart AI responses"""
    
    def __init__(self):
        self.performance_patterns = self._load_performance_patterns()
        self.error_patterns = self._load_error_patterns()
        self.threshold_rules = self._load_threshold_rules()
        self.solution_database = self._load_solution_database()
    
    def _load_performance_patterns(self) -> Dict[str, Dict]:
        """Load common performance patterns and their signatures"""
        return {
            "memory_pressure_gc": {
                "symptoms": ["high_cpu", "high_memory", "gc_pressure"],
                "triggers": {"cpu": ">80", "memory": ">80", "gc_time": ">100ms"},
                "root_cause": "Memory pressure causing excessive garbage collection",
                "solutions": [
                    "Increase heap size (-Xmx)",
                    "Optimize object allocation patterns", 
                    "Review memory leaks",
                    "Consider G1GC for better latency"
                ],
                "confidence": 0.95
            },
            
            "database_bottleneck": {
                "symptoms": ["slow_queries", "connection_pool_full", "high_latency"],
                "triggers": {"db_latency": ">1000ms", "connections": ">90%", "cpu_db": ">70"},
                "root_cause": "Database performance degradation",
                "solutions": [
                    "Optimize slow queries",
                    "Add database indexes", 
                    "Scale connection pool",
                    "Consider read replicas"
                ],
                "confidence": 0.90
            },
            
            "cascade_failure": {
                "symptoms": ["error_spike", "latency_increase", "resource_exhaustion"],
                "triggers": {"error_rate": ">5%", "latency": ">2x_normal", "timeouts": ">10"},
                "root_cause": "Upstream service failure causing downstream impact",
                "solutions": [
                    "Implement circuit breaker",
                    "Add timeout/retry logic",
                    "Scale failing service",
                    "Enable graceful degradation"
                ],
                "confidence": 0.85
            },
            
            "resource_leak": {
                "symptoms": ["memory_climb", "connection_growth", "handle_increase"],
                "triggers": {"memory_trend": "increasing", "connections_trend": "increasing"},
                "root_cause": "Resource leak in application code",
                "solutions": [
                    "Analyze heap dumps",
                    "Check connection cleanup",
                    "Review file handle usage",
                    "Add resource monitoring"
                ],
                "confidence": 0.80
            }
        }
    
    def _load_error_patterns(self) -> Dict[str, Dict]:
        """Load common error patterns and solutions"""
        return {
            "OutOfMemoryError": {
                "immediate_actions": [
                    "Restart affected service",
                    "Check heap dump if available",
                    "Scale memory temporarily"
                ],
                "investigation": [
                    "Analyze memory usage patterns",
                    "Review recent code changes",
                    "Check for memory leaks"
                ],
                "prevention": [
                    "Set proper heap limits",
                    "Add memory monitoring",
                    "Implement memory alerts"
                ]
            },
            
            "ConnectionTimeout": {
                "immediate_actions": [
                    "Check network connectivity",
                    "Verify service health",
                    "Scale connection pool"
                ],
                "investigation": [
                    "Analyze connection patterns",
                    "Check service load",
                    "Review timeout settings"
                ],
                "prevention": [
                    "Implement connection pooling",
                    "Add circuit breakers",
                    "Set appropriate timeouts"
                ]
            },
            
            "DatabaseLockTimeout": {
                "immediate_actions": [
                    "Check for long-running transactions",
                    "Identify blocking queries",
                    "Consider query cancellation"
                ],
                "investigation": [
                    "Analyze query execution plans",
                    "Review transaction scope",
                    "Check index usage"
                ],
                "prevention": [
                    "Optimize query performance",
                    "Minimize transaction scope",
                    "Add query timeouts"
                ]
            }
        }
    
    def _load_threshold_rules(self) -> Dict[str, Dict]:
        """Load intelligent threshold rules"""
        return {
            "cpu": {
                "normal": "<60%",
                "warning": "60-80%", 
                "critical": ">80%",
                "emergency": ">95%"
            },
            "memory": {
                "normal": "<70%",
                "warning": "70-85%",
                "critical": ">85%", 
                "emergency": ">95%"
            },
            "latency": {
                "excellent": "<100ms",
                "good": "100-500ms",
                "acceptable": "500ms-2s",
                "poor": ">2s"
            },
            "error_rate": {
                "excellent": "<0.1%",
                "good": "0.1-1%", 
                "warning": "1-5%",
                "critical": ">5%"
            }
        }
    
    def _load_solution_database(self) -> Dict[str, List[str]]:
        """Load comprehensive solution database"""
        return {
            "high_cpu": [
                "Profile CPU usage to identify hotspots",
                "Check for inefficient algorithms",
                "Review thread pool configurations",
                "Consider horizontal scaling",
                "Optimize database queries",
                "Check for busy-wait loops"
            ],
            
            "high_memory": [
                "Analyze heap dumps for memory leaks",
                "Review object lifecycle management", 
                "Optimize caching strategies",
                "Consider memory-efficient data structures",
                "Scale memory or optimize allocation",
                "Check for unnecessary object retention"
            ],
            
            "high_latency": [
                "Identify slow components in request path",
                "Optimize database queries and indexes",
                "Review network latency and bandwidth",
                "Implement caching strategies",
                "Consider async processing",
                "Check for resource contention"
            ],
            
            "high_error_rate": [
                "Analyze error logs for patterns",
                "Check service dependencies",
                "Review recent deployments",
                "Implement circuit breakers",
                "Add retry logic with backoff",
                "Monitor upstream service health"
            ]
        }


class EnvironmentLearner:
    """Learns environment-specific patterns and baselines"""
    
    def __init__(self):
        self.baselines = {}
        self.patterns = {}
        self.incidents = []
    
    def learn_baselines(self, metrics_history: List[Dict]) -> Dict[str, Any]:
        """Learn normal baselines from historical data"""
        if not metrics_history:
            return self._default_baselines()
        
        baselines = {}
        
        # Calculate percentiles for key metrics
        for metric in ['cpu', 'memory', 'latency', 'error_rate']:
            values = [m.get(metric, 0) for m in metrics_history if m.get(metric) is not None]
            if values:
                baselines[metric] = {
                    'median': self._percentile(values, 50),
                    'p95': self._percentile(values, 95),
                    'p99': self._percentile(values, 99),
                    'normal_range': f"{self._percentile(values, 10)}-{self._percentile(values, 90)}"
                }
        
        self.baselines = baselines
        return baselines
    
    def _percentile(self, values: List[float], percentile: int) -> float:
        """Calculate percentile of values"""
        sorted_values = sorted(values)
        index = int(len(sorted_values) * percentile / 100)
        return sorted_values[min(index, len(sorted_values) - 1)]
    
    def _default_baselines(self) -> Dict[str, Any]:
        """Default baselines when no historical data available"""
        return {
            'cpu': {'normal_range': '20-60%', 'median': 40},
            'memory': {'normal_range': '30-70%', 'median': 50}, 
            'latency': {'normal_range': '50-200ms', 'median': 100},
            'error_rate': {'normal_range': '0-1%', 'median': 0.1}
        }
    
    def is_anomaly(self, metric: str, value: float) -> bool:
        """Detect if current value is anomalous"""
        if metric not in self.baselines:
            return False
        
        baseline = self.baselines[metric]
        threshold = baseline.get('p95', 0) * 1.5  # 50% above 95th percentile
        return value > threshold
    
    def learn_from_incident(self, incident: Dict[str, Any]):
        """Learn from resolved incidents"""
        self.incidents.append({
            'timestamp': datetime.utcnow(),
            'symptoms': incident.get('symptoms', []),
            'root_cause': incident.get('root_cause', ''),
            'solution': incident.get('solution', ''),
            'metrics': incident.get('metrics', {})
        })
        
        # Update pattern recognition
        self._update_patterns(incident)
    
    def _update_patterns(self, incident: Dict[str, Any]):
        """Update learned patterns from incident"""
        symptoms = incident.get('symptoms', [])
        root_cause = incident.get('root_cause', '')
        
        pattern_key = '_'.join(sorted(symptoms))
        
        if pattern_key in self.patterns:
            self.patterns[pattern_key]['occurrences'] += 1
            self.patterns[pattern_key]['confidence'] += 0.1
        else:
            self.patterns[pattern_key] = {
                'symptoms': symptoms,
                'root_cause': root_cause,
                'solution': incident.get('solution', ''),
                'occurrences': 1,
                'confidence': 0.5
            }


class IntelligenceEnhancer:
    """Main class that enhances AI intelligence with observability expertise"""
    
    def __init__(self):
        self.knowledge_base = ObservabilityKnowledgeBase()
        self.environment_learner = EnvironmentLearner()
        self.context_builder = ContextBuilder()
    
    def analyze_performance_issue(self, 
                                metrics: Dict[str, Any],
                                logs: List[str],
                                traces: List[Dict],
                                user_query: str) -> Dict[str, Any]:
        """Comprehensive analysis of performance issues"""
        
        # Detect patterns
        detected_patterns = self._detect_patterns(metrics, logs, traces)
        
        # Build context
        context = self.context_builder.build_context(metrics, logs, traces, self.environment_learner.baselines)
        
        # Generate intelligent response
        response = self._generate_intelligent_response(
            detected_patterns, context, user_query
        )
        
        return response
    
    def _detect_patterns(self, 
                        metrics: Dict[str, Any],
                        logs: List[str], 
                        traces: List[Dict]) -> List[Pattern]:
        """Detect known patterns in observability data"""
        
        detected_patterns = []
        
        # Check performance patterns
        for pattern_name, pattern_def in self.knowledge_base.performance_patterns.items():
            confidence = self._calculate_pattern_confidence(
                pattern_def, metrics, logs, traces
            )
            
            if confidence > 0.6:  # Threshold for pattern detection
                pattern = Pattern(
                    name=pattern_name,
                    confidence=confidence,
                    symptoms=pattern_def['symptoms'],
                    root_cause=pattern_def['root_cause'],
                    solutions=pattern_def['solutions'],
                    prevention=pattern_def.get('prevention', [])
                )
                detected_patterns.append(pattern)
        
        # Check learned patterns from environment
        for pattern_key, pattern_data in self.environment_learner.patterns.items():
            if pattern_data['confidence'] > 0.7:
                current_symptoms = self._extract_symptoms(metrics, logs, traces)
                if set(pattern_data['symptoms']).intersection(set(current_symptoms)):
                    pattern = Pattern(
                        name=f"learned_{pattern_key}",
                        confidence=pattern_data['confidence'],
                        symptoms=pattern_data['symptoms'],
                        root_cause=pattern_data['root_cause'],
                        solutions=[pattern_data['solution']],
                        prevention=[]
                    )
                    detected_patterns.append(pattern)
        
        return sorted(detected_patterns, key=lambda p: p.confidence, reverse=True)
    
    def _calculate_pattern_confidence(self,
                                    pattern_def: Dict,
                                    metrics: Dict[str, Any],
                                    logs: List[str],
                                    traces: List[Dict]) -> float:
        """Calculate confidence score for pattern match"""
        
        triggers = pattern_def.get('triggers', {})
        confidence = 0.0
        total_triggers = len(triggers)
        
        if total_triggers == 0:
            return 0.0
        
        for trigger, condition in triggers.items():
            if self._evaluate_condition(trigger, condition, metrics, logs, traces):
                confidence += 1.0 / total_triggers
        
        return confidence
    
    def _evaluate_condition(self,
                          trigger: str,
                          condition: str, 
                          metrics: Dict[str, Any],
                          logs: List[str],
                          traces: List[Dict]) -> bool:
        """Evaluate if a condition is met"""
        
        if trigger in metrics:
            value = metrics[trigger]
            
            # Parse condition (e.g., ">80", ">90%", ">1000ms")
            if condition.startswith('>'):
                threshold = self._parse_threshold(condition[1:])
                return value > threshold
            elif condition.startswith('<'):
                threshold = self._parse_threshold(condition[1:])
                return value < threshold
        
        # Check logs for specific patterns
        if trigger in ['timeouts', 'errors', 'gc_pressure']:
            return any(trigger.lower() in log.lower() for log in logs)
        
        return False
    
    def _parse_threshold(self, threshold_str: str) -> float:
        """Parse threshold string to numeric value"""
        threshold_str = threshold_str.strip()
        
        if threshold_str.endswith('%'):
            return float(threshold_str[:-1])
        elif threshold_str.endswith('ms'):
            return float(threshold_str[:-2])
        else:
            return float(threshold_str)
    
    def _extract_symptoms(self,
                         metrics: Dict[str, Any],
                         logs: List[str],
                         traces: List[Dict]) -> List[str]:
        """Extract symptoms from current observability data"""
        
        symptoms = []
        
        # Check metric-based symptoms
        if metrics.get('cpu', 0) > 80:
            symptoms.append('high_cpu')
        if metrics.get('memory', 0) > 80:
            symptoms.append('high_memory')
        if metrics.get('latency', 0) > 2000:
            symptoms.append('high_latency')
        if metrics.get('error_rate', 0) > 5:
            symptoms.append('high_error_rate')
        
        # Check log-based symptoms
        log_text = ' '.join(logs).lower()
        if 'timeout' in log_text:
            symptoms.append('timeouts')
        if 'outofmemoryerror' in log_text:
            symptoms.append('memory_errors')
        if 'connection' in log_text and 'pool' in log_text:
            symptoms.append('connection_issues')
        
        return symptoms
    
    def _generate_intelligent_response(self,
                                     patterns: List[Pattern],
                                     context: Dict[str, Any],
                                     user_query: str) -> Dict[str, Any]:
        """Generate intelligent response with solutions"""
        
        if not patterns:
            return self._generate_general_response(context, user_query)
        
        # Use highest confidence pattern
        primary_pattern = patterns[0]
        
        response = {
            'analysis': {
                'detected_patterns': [
                    {
                        'name': p.name,
                        'confidence': p.confidence,
                        'root_cause': p.root_cause
                    } for p in patterns[:3]  # Top 3 patterns
                ],
                'primary_root_cause': primary_pattern.root_cause,
                'confidence': primary_pattern.confidence
            },
            'context': context,
            'immediate_actions': primary_pattern.solutions[:3],
            'detailed_solutions': primary_pattern.solutions,
            'prevention_strategies': primary_pattern.prevention,
            'monitoring_recommendations': self._generate_monitoring_recommendations(primary_pattern),
            'related_patterns': [p.name for p in patterns[1:3]]
        }
        
        return response
    
    def _generate_general_response(self,
                                 context: Dict[str, Any],
                                 user_query: str) -> Dict[str, Any]:
        """Generate response when no specific patterns detected"""
        
        return {
            'analysis': {
                'status': 'No specific patterns detected',
                'confidence': 0.3
            },
            'context': context,
            'general_recommendations': [
                'Check recent deployments and changes',
                'Review service dependencies',
                'Analyze trends over longer time periods',
                'Verify monitoring and alerting coverage'
            ]
        }
    
    def _generate_monitoring_recommendations(self, pattern: Pattern) -> List[str]:
        """Generate monitoring recommendations based on detected pattern"""
        
        recommendations = []
        
        if 'memory' in pattern.name:
            recommendations.extend([
                'Set memory usage alerts at 85% threshold',
                'Monitor GC frequency and duration',
                'Track heap dump generation triggers'
            ])
        
        if 'database' in pattern.name:
            recommendations.extend([
                'Monitor database connection pool utilization',
                'Set alerts for slow query detection',
                'Track database lock wait times'
            ])
        
        if 'cpu' in pattern.name:
            recommendations.extend([
                'Monitor CPU usage trends',
                'Set alerts for sustained high CPU',
                'Track thread pool utilization'
            ])
        
        return recommendations


class ContextBuilder:
    """Builds intelligent context for AI responses"""
    
    def build_context(self,
                     metrics: Dict[str, Any],
                     logs: List[str],
                     traces: List[Dict],
                     baselines: Dict[str, Any]) -> Dict[str, Any]:
        """Build comprehensive context for AI analysis"""
        
        context = {
            'current_state': self._analyze_current_state(metrics, baselines),
            'trends': self._analyze_trends(metrics),
            'correlations': self._find_correlations(metrics, logs, traces),
            'severity': self._assess_severity(metrics, baselines),
            'time_context': self._get_time_context(),
            'environment_health': self._assess_environment_health(metrics)
        }
        
        return context
    
    def _analyze_current_state(self,
                             metrics: Dict[str, Any],
                             baselines: Dict[str, Any]) -> Dict[str, str]:
        """Analyze current state vs baselines"""
        
        state = {}
        
        for metric, value in metrics.items():
            if metric in baselines:
                baseline = baselines[metric]
                if isinstance(baseline, dict) and 'median' in baseline:
                    if value > baseline['median'] * 1.5:
                        state[metric] = 'significantly_above_normal'
                    elif value > baseline['median'] * 1.2:
                        state[metric] = 'above_normal'
                    elif value < baseline['median'] * 0.8:
                        state[metric] = 'below_normal'
                    else:
                        state[metric] = 'normal'
                else:
                    state[metric] = 'no_baseline'
            else:
                state[metric] = 'unknown_baseline'
        
        return state
    
    def _analyze_trends(self, metrics: Dict[str, Any]) -> Dict[str, str]:
        """Analyze metric trends (simplified)"""
        # In real implementation, this would analyze time series data
        return {
            'cpu': 'stable',
            'memory': 'increasing',
            'latency': 'stable',
            'error_rate': 'decreasing'
        }
    
    def _find_correlations(self,
                          metrics: Dict[str, Any],
                          logs: List[str],
                          traces: List[Dict]) -> List[str]:
        """Find correlations between different signals"""
        
        correlations = []
        
        # Check for common correlation patterns
        if metrics.get('cpu', 0) > 80 and metrics.get('memory', 0) > 80:
            correlations.append('High CPU and memory usage correlation detected')
        
        if metrics.get('error_rate', 0) > 5 and metrics.get('latency', 0) > 2000:
            correlations.append('Error rate and latency correlation detected')
        
        # Check log correlations
        error_logs = [log for log in logs if 'error' in log.lower()]
        if len(error_logs) > 5 and metrics.get('latency', 0) > 1000:
            correlations.append('Error logs correlate with high latency')
        
        return correlations
    
    def _assess_severity(self,
                        metrics: Dict[str, Any],
                        baselines: Dict[str, Any]) -> str:
        """Assess overall severity of the situation"""
        
        critical_metrics = 0
        warning_metrics = 0
        
        for metric, value in metrics.items():
            if metric in ['cpu', 'memory', 'latency', 'error_rate']:
                if value > 90:  # Critical threshold
                    critical_metrics += 1
                elif value > 70:  # Warning threshold
                    warning_metrics += 1
        
        if critical_metrics > 0:
            return 'critical'
        elif warning_metrics > 2:
            return 'warning'
        else:
            return 'normal'
    
    def _get_time_context(self) -> Dict[str, Any]:
        """Get time context information"""
        now = datetime.utcnow()
        
        return {
            'current_time': now.isoformat(),
            'hour_of_day': now.hour,
            'day_of_week': now.weekday(),
            'is_business_hours': 9 <= now.hour <= 17,
            'is_weekend': now.weekday() >= 5
        }
    
    def _assess_environment_health(self, metrics: Dict[str, Any]) -> str:
        """Assess overall environment health"""
        
        health_score = 100
        
        # Deduct points for issues
        if metrics.get('cpu', 0) > 80:
            health_score -= 30
        if metrics.get('memory', 0) > 80:
            health_score -= 30
        if metrics.get('error_rate', 0) > 5:
            health_score -= 40
        
        if health_score >= 80:
            return 'healthy'
        elif health_score >= 60:
            return 'degraded'
        else:
            return 'unhealthy'


# Example usage function
def enhance_ai_response(metrics: Dict[str, Any],
                       logs: List[str],
                       traces: List[Dict],
                       user_query: str) -> str:
    """Main function to enhance AI response with intelligence"""
    
    enhancer = IntelligenceEnhancer()
    
    # Analyze the situation
    analysis = enhancer.analyze_performance_issue(metrics, logs, traces, user_query)
    
    # Format intelligent response
    response = f"""
🔍 INTELLIGENT ANALYSIS:

{analysis.get('analysis', {}).get('primary_root_cause', 'Analysis in progress...')}
Confidence: {analysis.get('analysis', {}).get('confidence', 0) * 100:.1f}%

📊 CURRENT CONTEXT:
Environment Health: {analysis.get('context', {}).get('environment_health', 'Unknown')}
Severity: {analysis.get('context', {}).get('severity', 'Normal')}

💡 IMMEDIATE ACTIONS:
{chr(10).join(f"• {action}" for action in analysis.get('immediate_actions', []))}

🔧 DETAILED SOLUTIONS:
{chr(10).join(f"• {solution}" for solution in analysis.get('detailed_solutions', []))}

📈 MONITORING RECOMMENDATIONS:
{chr(10).join(f"• {rec}" for rec in analysis.get('monitoring_recommendations', []))}

🛡️ PREVENTION STRATEGIES:
{chr(10).join(f"• {strategy}" for strategy in analysis.get('prevention_strategies', []))}
"""
    
    return response