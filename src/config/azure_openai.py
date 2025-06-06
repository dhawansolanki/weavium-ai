"""
Azure OpenAI integration for the Autogen Agents Framework.
"""

from typing import Dict, Any, Optional
from .config_manager import AzureOpenAIConfig

def create_azure_openai_config(config: AzureOpenAIConfig) -> Dict[str, Any]:
    """
    Create an Azure OpenAI configuration dictionary for use with Autogen.
    
    Args:
        config: Azure OpenAI configuration
        
    Returns:
        Configuration dictionary for Autogen
    """
    return {
        "config_list": [
            {
                "model": config.deployment_name,
                "api_key": config.api_key,
                "api_type": "azure", 
                "api_version": config.api_version,
                "base_url": config.endpoint,
                "api_key": config.api_key
            }
        ],
        "temperature": 0.7,
        "cache_seed": None,  # Change this to an integer to enable caching
    }

def create_llm_config(
    config: AzureOpenAIConfig,
    temperature: float = 0.7,
    cache_seed: Optional[int] = None,
    max_tokens: Optional[int] = None,
    functions: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a complete LLM configuration for an agent.
    
    Args:
        config: Azure OpenAI configuration
        temperature: Temperature for the LLM (0.0 to 1.0)
        cache_seed: Seed for caching (None to disable)
        max_tokens: Maximum tokens to generate
        functions: Function definitions for the LLM
        
    Returns:
        LLM configuration dictionary for Autogen
    """
    llm_config = create_azure_openai_config(config)
    llm_config["temperature"] = temperature
    llm_config["cache_seed"] = cache_seed
    
    if max_tokens is not None:
        llm_config["config_list"][0]["max_tokens"] = max_tokens
    
    if functions is not None:
        llm_config["functions"] = functions
    
    return llm_config
