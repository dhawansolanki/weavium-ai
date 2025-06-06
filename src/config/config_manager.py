"""
Configuration manager for the Autogen Agents Framework.
Handles loading and validating configuration from environment variables and config files.
"""

import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field, validator

class AzureOpenAIConfig(BaseModel):
    """Configuration for Azure OpenAI API."""
    api_key: str = Field(..., description="Azure OpenAI API key")
    endpoint: str = Field(..., description="Azure OpenAI endpoint URL")
    api_version: str = Field("2023-05-15", description="Azure OpenAI API version")
    deployment_name: str = Field(..., description="Azure OpenAI deployment name")

    @validator("endpoint")
    def validate_endpoint(cls, v):
        if not v.startswith(("http://", "https://")):
            raise ValueError("Endpoint must start with http:// or https://")
        return v

class AgentConfig(BaseModel):
    """Configuration for an agent."""
    name: str = Field(..., description="Agent name")
    description: str = Field(..., description="Agent description")
    system_message: str = Field(..., description="Agent system message")
    llm_config: Dict[str, Any] = Field(..., description="LLM configuration for the agent")
    
class ToolConfig(BaseModel):
    """Configuration for a tool."""
    name: str = Field(..., description="Tool name")
    description: str = Field(..., description="Tool description")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Tool parameters")

class MCPServerConfig(BaseModel):
    """Configuration for an MCP server."""
    name: str = Field(..., description="MCP server name")
    endpoint: str = Field(..., description="MCP server endpoint URL")
    api_key: Optional[str] = Field(None, description="MCP server API key if required")

class Config(BaseModel):
    """Main configuration for the Autogen Agents Framework."""
    azure_openai: AzureOpenAIConfig
    agents: Dict[str, AgentConfig] = Field(default_factory=dict)
    tools: Dict[str, ToolConfig] = Field(default_factory=dict)
    mcp_servers: Dict[str, MCPServerConfig] = Field(default_factory=dict)

class ConfigManager:
    """Manager for loading and accessing configuration."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Path to a JSON configuration file. If None, will try to load from environment variables.
        """
        self.config = None
        self._load_config(config_path)
    
    def _load_config(self, config_path: Optional[str] = None):
        """
        Load configuration from file or environment variables.
        
        Args:
            config_path: Path to a JSON configuration file.
        """
        # Load environment variables
        load_dotenv()
        
        if config_path and os.path.exists(config_path):
            # Load from config file
            with open(config_path, 'r') as f:
                config_data = json.load(f)
        else:
            # Load from environment variables
            config_data = {
                "azure_openai": {
                    "api_key": os.getenv("AZURE_OPENAI_API_KEY", ""),
                    "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT", ""),
                    "api_version": os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15"),
                    "deployment_name": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")
                }
            }
        
        # Validate and create config object
        self.config = Config(**config_data)
    
    def get_azure_openai_config(self) -> AzureOpenAIConfig:
        """Get Azure OpenAI configuration."""
        return self.config.azure_openai
    
    def get_agent_config(self, agent_name: str) -> Optional[AgentConfig]:
        """Get configuration for a specific agent."""
        return self.config.agents.get(agent_name)
    
    def get_tool_config(self, tool_name: str) -> Optional[ToolConfig]:
        """Get configuration for a specific tool."""
        return self.config.tools.get(tool_name)
    
    def get_mcp_server_config(self, server_name: str) -> Optional[MCPServerConfig]:
        """Get configuration for a specific MCP server."""
        return self.config.mcp_servers.get(server_name)
    
    def save_config(self, config_path: str):
        """
        Save the current configuration to a file.
        
        Args:
            config_path: Path to save the configuration file.
        """
        with open(config_path, 'w') as f:
            json.dump(self.config.dict(), f, indent=2)
