"""
Databricks Claude Integration for DPL Agent

Integração com Claude via Databricks Serving Endpoints,
compatível com ambiente Databricks e local development.
"""

import os
from typing import Dict, Any, Optional, List
from datetime import datetime

from ...utils import get_logger

logger = get_logger(__name__)


class DatabricksClaudeProvider:
    """
    Claude LLM Provider via Databricks Serving Endpoints.
    
    Supports both Databricks environment (production) and
    local development (simulation mode).
    """
    
    def __init__(
        self,
        endpoint_name: str = "databricks-claude-sonnet-4",
        temperature: float = 0.1
    ):
        """
        Initialize Databricks Claude provider.
        
        Args:
            endpoint_name: Name of Databricks serving endpoint
            temperature: Sampling temperature (0.0-1.0)
        """
        self.endpoint_name = endpoint_name
        self.temperature = temperature
        self.client = None
        self.connected = False
        
        self.model_config = {
            "max_tokens": 4000,
            "temperature": temperature,
            "top_p": 0.9,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        }
        
        logger.info(
            "Initializing Databricks Claude provider",
            endpoint=endpoint_name,
            temperature=temperature
        )
        
        self._setup_client()
    
    def _setup_client(self) -> None:
        """
        Setup Databricks serving client with graceful fallback.
        
        In production (Databricks): connects to serving endpoint
        In development (local): activates simulation mode
        """
        try:
            from databricks.serving import ServingEndpointsClient
            self.client = ServingEndpointsClient()
            self.connected = True
            logger.info("Databricks Claude client operational")
            
        except ImportError:
            logger.warning(
                "Databricks SDK not available - simulation mode active",
                environment="local_development"
            )
            self.connected = False
            
        except Exception as e:
            logger.error(
                "Failed to setup Databricks client - simulation mode active",
                error=str(e)
            )
            self.connected = False
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate text using Claude via Databricks endpoint.
        
        Args:
            prompt: User prompt/query
            system_prompt: Optional system instructions
            max_tokens: Optional max tokens override
            
        Returns:
            Generated text response
        """
        logger.debug("Generating response", prompt_length=len(prompt))
        
        if not self.connected or not self.client:
            return self._simulate_response(prompt)
        
        try:
            # Build messages
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            # Override config if needed
            config = self.model_config.copy()
            if max_tokens:
                config["max_tokens"] = max_tokens
            
            # Call endpoint
            response = self.client.query(
                name=self.endpoint_name,
                inputs={
                    "messages": messages,
                    **config
                }
            )
            
            # Extract response text
            if hasattr(response, 'predictions'):
                text = response.predictions[0]['candidates'][0]['message']['content']
            else:
                text = str(response)
            
            logger.info("Response generated successfully")
            return text
            
        except Exception as e:
            logger.error("Claude generation failed", error=str(e))
            return self._simulate_response(prompt, error_context=str(e))
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Multi-turn conversation via Claude.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            system_prompt: Optional system instructions
            
        Returns:
            Claude's response
        """
        if not self.connected or not self.client:
            last_user_msg = next(
                (m["content"] for m in reversed(messages) if m["role"] == "user"),
                "Hello"
            )
            return self._simulate_response(last_user_msg)
        
        try:
            # Add system prompt if provided
            full_messages = []
            if system_prompt:
                full_messages.append({"role": "system", "content": system_prompt})
            full_messages.extend(messages)
            
            response = self.client.query(
                name=self.endpoint_name,
                inputs={
                    "messages": full_messages,
                    **self.model_config
                }
            )
            
            if hasattr(response, 'predictions'):
                return response.predictions[0]['candidates'][0]['message']['content']
            else:
                return str(response)
                
        except Exception as e:
            logger.error("Chat generation failed", error=str(e))
            last_user_msg = next(
                (m["content"] for m in reversed(messages) if m["role"] == "user"),
                "Hello"
            )
            return self._simulate_response(last_user_msg, error_context=str(e))
    
    def _simulate_response(
        self,
        prompt: str,
        error_context: Optional[str] = None
    ) -> str:
        """
        Simulate Claude response for local development.
        
        Provides intelligent context-aware responses based on
        DPL domain knowledge when Databricks endpoint unavailable.
        
        Args:
            prompt: User prompt
            error_context: Optional error information
            
        Returns:
            Simulated intelligent response
        """
        logger.debug("Generating simulated response")
        
        prompt_lower = prompt.lower()
        
        # DPL troubleshooting queries
        if any(word in prompt_lower for word in ['timeout', 'erro', 'error', 'falha', 'fail']):
            return f"""DPL TROUBLESHOOTING ANALYSIS

Query: "{prompt[:100]}..."

Common timeout scenarios in DPL pipelines:

1. STREAMING TIMEOUTS (> 1h):
   - Root cause: Large data volume, checkpoint issues
   - Investigation: Check Event Hub backlog, verify checkpoint integrity
   - Tools: GetLastUpdatedAt.py, Databricks Workflows tab

2. BATCH TIMEOUTS (> 90min):
   - Root cause: Slow CosmosDB queries, SCD2 merge bottlenecks
   - Investigation: Query performance, data volume, cluster resources
   - Tools: run_ingestion manual execution, AdjustIsCurrent.py

3. IMMEDIATE ACTIONS:
   - Manual reprocessing for specific date
   - Coordinate with KPI team before reprocessing
   - Use scope: specific day (not full history)

MODE: Simulation (Databricks endpoint unavailable)
TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{f'NOTE: {error_context}' if error_context else ''}
"""
        
        # Pipeline analysis queries
        elif any(word in prompt_lower for word in ['pipeline', 'workflow', 'streaming', 'batch']):
            return f"""DPL PIPELINE ANALYSIS

Query: "{prompt[:100]}..."

DPL ARCHITECTURE OVERVIEW:

STREAMING PIPELINES (13 workflows):
- Event Hub → Bronze → Silver pattern
- Entities: visits, tasks, vendorgroups, userclientcatalog, etc.
- Trigger: file_arrival with min_time_between_triggers
- Health check: duration > 1 hour

BATCH PIPELINES (12 workflows):
- CosmosDB → Bronze → Silver pattern
- Schedule: CRON (typically every 30 minutes)
- Entities: Orders, OnTapUserSessions, PartnerGroups, Identity
- SCD2 merge for historical tracking

KEY COMPONENTS:
- run_ingestion: Batch orchestrator wrapper
- bronze_ingestion.py: Streaming Event Hub reader
- BaseTable: Parent class for all entities
- IngestionControl: Logging and monitoring

MODE: Simulation
TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        # Performance optimization queries
        elif any(word in prompt_lower for word in ['otimiz', 'performance', 'lento', 'slow']):
            return f"""DPL PERFORMANCE OPTIMIZATION

Query: "{prompt[:100]}..."

OPTIMIZATION STRATEGIES:

1. DELTA TABLE OPTIMIZATION:
   - Run OptimizeDeltaTable.py
   - OPTIMIZE table ZORDER BY (key_columns)
   - VACUUM old files (retention: 7 days)

2. CLUSTER CONFIGURATION:
   - Streaming: MEMORY_OPTIMIZED_SMALL
   - Batch: GENERAL_PURPOSE_LARGE
   - Adjust based on workload

3. QUERY OPTIMIZATION:
   - Partition pruning
   - Predicate pushdown
   - Broadcast joins for small tables

4. SCD2 MERGE PERFORMANCE:
   - Check hash_key distribution
   - Verify is_current flags
   - Use AdjustIsCurrent.py if needed

MODE: Simulation
TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        # Generic DPL query
        else:
            return f"""DPL AGENT RESPONSE

Query: "{prompt[:100]}..."

DPL CAPABILITIES:

TROUBLESHOOTING:
- Error diagnosis with severity classification
- Root cause analysis
- Actionable resolution steps
- Tool recommendations

MONITORING:
- Pipeline health analysis
- Performance metrics
- Data quality validation
- SLA compliance

OPTIMIZATION:
- Delta table optimization
- Query performance tuning
- Resource allocation
- Cost optimization

COORDINATION:
- Reprocessing workflows
- Cross-team coordination
- Impact analysis

AVAILABLE TOOLS:
- GetLastUpdatedAt.py
- AdjustIsCurrent.py
- DebugIngestion.py
- OptimizeDeltaTable.py

MODE: Simulation (connect to Databricks for full capabilities)
TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{f'NOTE: {error_context}' if error_context else ''}
"""
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get provider status information.
        
        Returns:
            Status dictionary with connection and config info
        """
        return {
            "provider": "databricks_claude",
            "endpoint": self.endpoint_name,
            "connected": self.connected,
            "client_available": self.client is not None,
            "model_config": self.model_config,
            "features": [
                "generate",
                "chat",
                "simulation_fallback",
                "databricks_native"
            ]
        }


def create_databricks_claude(
    endpoint_name: str = "databricks-claude-sonnet-4",
    temperature: float = 0.1
) -> DatabricksClaudeProvider:
    """
    Factory function to create Databricks Claude provider.
    
    Args:
        endpoint_name: Databricks serving endpoint name
        temperature: Sampling temperature
        
    Returns:
        Configured DatabricksClaudeProvider instance
    """
    return DatabricksClaudeProvider(
        endpoint_name=endpoint_name,
        temperature=temperature
    )

