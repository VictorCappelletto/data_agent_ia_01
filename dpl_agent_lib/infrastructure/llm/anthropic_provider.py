"""
DPL Agent v3.0 - Anthropic LLM Provider

Implements LLMServicePort using Anthropic's Claude models.
Provides text generation, streaming, and tool calling capabilities.
"""

import os
from typing import List, Dict, Any, Optional, AsyncIterator

from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage, SystemMessage, AIMessage

from ...domain.ports.hdl_repository_port import LLMServicePort


class AnthropicLLMProvider(LLMServicePort):
    """
    Anthropic Claude implementation of LLMServicePort.
    
    Features:
    - Claude 3.5 Sonnet support
    - Streaming responses
    - Tool calling (function calling)
    - Configurable temperature and max tokens
    """
    
    def __init__(
        self,
        model: str = "claude-3-5-sonnet-20241022",
        api_key: Optional[str] = None,
        default_temperature: float = 0.1,
        default_max_tokens: int = 4096
    ):
        """
        Initialize Anthropic provider.
        
        Args:
            model: Claude model to use
            api_key: Anthropic API key (defaults to env var)
            default_temperature: Default temperature
            default_max_tokens: Default max tokens
        """
        self.model_name = model
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.default_temperature = default_temperature
        self.default_max_tokens = default_max_tokens
        
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        
        # Initialize LangChain ChatAnthropic
        self._client = ChatAnthropic(
            model=self.model_name,
            anthropic_api_key=self.api_key,
            temperature=self.default_temperature,
            max_tokens=self.default_max_tokens
        )
    
    async def generate(
        self,
        prompt: str,
        temperature: float = 0.1,
        max_tokens: int = 4096,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate text response.
        
        Args:
            prompt: User prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            system_prompt: Optional system prompt
            
        Returns:
            Generated text
        """
        # Create messages
        messages = []
        
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        
        messages.append(HumanMessage(content=prompt))
        
        # Configure client for this request
        client = ChatAnthropic(
            model=self.model_name,
            anthropic_api_key=self.api_key,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # Generate
        response = await client.ainvoke(messages)
        
        return response.content
    
    async def generate_stream(
        self,
        prompt: str,
        temperature: float = 0.1,
        max_tokens: int = 4096,
        system_prompt: Optional[str] = None
    ) -> AsyncIterator[str]:
        """
        Generate streaming text response.
        
        Args:
            prompt: User prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            system_prompt: Optional system prompt
            
        Yields:
            Text chunks as they are generated
        """
        # Create messages
        messages = []
        
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        
        messages.append(HumanMessage(content=prompt))
        
        # Configure client for streaming
        client = ChatAnthropic(
            model=self.model_name,
            anthropic_api_key=self.api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            streaming=True
        )
        
        # Stream response
        async for chunk in client.astream(messages):
            if hasattr(chunk, "content") and chunk.content:
                yield chunk.content
    
    async def generate_with_tools(
        self,
        prompt: str,
        tools: List[Dict[str, Any]],
        temperature: float = 0.1
    ) -> Dict[str, Any]:
        """
        Generate response with tool calling.
        
        Args:
            prompt: User prompt
            tools: List of tool definitions
            temperature: Sampling temperature
            
        Returns:
            Response with tool calls
        """
        # Create messages
        messages = [HumanMessage(content=prompt)]
        
        # Configure client with tools
        client = ChatAnthropic(
            model=self.model_name,
            anthropic_api_key=self.api_key,
            temperature=temperature
        )
        
        # Bind tools to model
        client_with_tools = client.bind_tools(tools)
        
        # Generate
        response = await client_with_tools.ainvoke(messages)
        
        # Extract tool calls if present
        result = {
            "content": response.content,
            "tool_calls": []
        }
        
        if hasattr(response, "tool_calls") and response.tool_calls:
            result["tool_calls"] = [
                {
                    "name": tc["name"],
                    "args": tc["args"],
                    "id": tc.get("id")
                }
                for tc in response.tool_calls
            ]
        
        return result
    
    async def create_embedding(self, text: str) -> List[float]:
        """
        Create text embedding.
        
        Note: Anthropic doesn't provide embeddings directly.
        This would typically use OpenAI or another embedding service.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        raise NotImplementedError(
            "Anthropic doesn't provide embeddings. "
            "Use OpenAI or another embedding service."
        )
    
    def get_client(self) -> ChatAnthropic:
        """
        Get underlying LangChain client.
        
        Returns:
            ChatAnthropic instance
        """
        return self._client
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get model information.
        
        Returns:
            Model metadata
        """
        return {
            "provider": "Anthropic",
            "model": self.model_name,
            "default_temperature": self.default_temperature,
            "default_max_tokens": self.default_max_tokens,
            "supports_streaming": True,
            "supports_tool_calling": True,
            "supports_vision": "claude-3" in self.model_name
        }


# ============================================================================
# SYSTEM PROMPTS
# ============================================================================

DPL_SYSTEM_PROMPT = """You are an expert DPL (Harmonized Data Layer) specialist assistant.

Your role is to help with:
- DPL pipeline troubleshooting and debugging
- Architecture questions about streaming and batch pipelines
- Performance optimization recommendations
- Data quality validation
- Workflow orchestration
- SCD2 (Slowly Changing Dimension Type 2) operations

You have access to comprehensive DPL documentation covering:
- Streaming architecture (hdl_stm): Bronze and silver layers
- Batch architecture (hdl): CosmosDB ingestion, transformations
- Databricks workflows and triggers
- Common troubleshooting scenarios
- DPL utilities and tools

When responding:
1. Be specific and actionable
2. Reference relevant DPL components when applicable
3. Provide step-by-step guidance for complex tasks
4. Include code examples when helpful
5. Mention relevant tools (e.g., AdjustIsCurrent.py, DebugIngestion.py)
6. Consider both streaming and batch pipeline implications

Always ground your responses in the provided DPL documentation context."""


TROUBLESHOOTING_SYSTEM_PROMPT = """You are an DPL troubleshooting specialist.

Your primary focus is diagnosing and resolving DPL pipeline issues:
- Pipeline timeouts
- Data quality problems
- SCD2 merge issues
- Connection failures
- Performance bottlenecks

When troubleshooting:
1. Identify the error type and severity
2. Determine affected components (entity, pipeline, workflow)
3. Suggest immediate mitigation steps
4. Provide root cause analysis
5. Recommend long-term fixes
6. Reference relevant debugging tools

Use the provided DPL knowledge base to inform your diagnosis and solutions."""


ARCHITECTURE_SYSTEM_PROMPT = """You are an DPL architecture expert.

Your focus is explaining DPL system design and components:
- Overall architecture (streaming + batch)
- Pipeline flows and data movement
- Layer responsibilities (bronze, silver, gold)
- Entity relationships
- Workflow orchestration
- Integration points

When explaining architecture:
1. Start with high-level overview
2. Drill down into specific components as needed
3. Use diagrams or visual descriptions when helpful
4. Explain design decisions and trade-offs
5. Connect concepts to real DPL implementations

Ground all explanations in the actual DPL codebase structure."""


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_anthropic_provider(
    model: str = "claude-3-5-sonnet-20241022",
    temperature: float = 0.1,
    max_tokens: int = 4096
) -> AnthropicLLMProvider:
    """
    Factory function to create AnthropicLLMProvider.
    
    Args:
        model: Claude model to use
        temperature: Default temperature
        max_tokens: Default max tokens
        
    Returns:
        Initialized AnthropicLLMProvider
    """
    return AnthropicLLMProvider(
        model=model,
        default_temperature=temperature,
        default_max_tokens=max_tokens
    )


def get_system_prompt(intent: str) -> str:
    """
    Get appropriate system prompt based on intent.
    
    Args:
        intent: User intent (troubleshooting, architecture, etc.)
        
    Returns:
        System prompt string
    """
    prompts = {
        "troubleshooting": TROUBLESHOOTING_SYSTEM_PROMPT,
        "architecture": ARCHITECTURE_SYSTEM_PROMPT,
    }
    
    return prompts.get(intent, DPL_SYSTEM_PROMPT)

