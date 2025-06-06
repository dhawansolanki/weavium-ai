"""
Context7 MCP client implementation for the Autogen Agents Framework.
"""

import requests
import json
from typing import Dict, Any, Optional, List
from ..config.config_manager import MCPServerConfig

class Context7Client:
    """Client for interacting with the Context7 MCP server."""
    
    def __init__(self, config: MCPServerConfig):
        """
        Initialize a Context7 client.
        
        Args:
            config: MCP server configuration
        """
        self.name = config.name
        self.endpoint = config.endpoint
        self.api_key = config.api_key
        self.headers = {
            "Content-Type": "application/json"
        }
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"
    
    def resolve_library_id(self, library_name: str) -> Dict[str, Any]:
        """
        Resolve a library name to a Context7-compatible library ID.
        
        Args:
            library_name: Library name to resolve
            
        Returns:
            Dictionary containing resolved library IDs and metadata
        """
        url = f"{self.endpoint}/resolve-library-id"
        params = {"libraryName": library_name}
            
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_library_docs(self, library_id: str, tokens: int = 10000, topic: Optional[str] = None) -> Dict[str, Any]:
        """
        Get documentation for a library from the Context7 MCP server.
        
        Args:
            library_id: Library ID in Context7-compatible format
            tokens: Maximum number of tokens to retrieve
            topic: Optional topic to focus documentation on
            
        Returns:
            Library documentation
        """
        url = f"{self.endpoint}/get-library-docs"
        params = {
            "context7CompatibleLibraryID": library_id,
            "tokens": tokens
        }
        if topic:
            params["topic"] = topic
            
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def create_autogen_tools(self) -> List[Dict[str, Any]]:
        """
        Create Autogen-compatible tool definitions for the Context7 client.
        
        Returns:
            List of tool definition dictionaries
        """
        tools = []
        
        # Resolve library ID tool
        tools.append({
            "name": "context7_resolve_library_id",
            "description": "Resolve a package/product name to a Context7-compatible library ID",
            "function": self.resolve_library_id_tool,
            "parameters": {
                "library_name": {
                    "type": "string",
                    "description": "Library name to search for and retrieve a Context7-compatible library ID"
                }
            }
        })
        
        # Get library docs tool
        tools.append({
            "name": "context7_get_library_docs",
            "description": "Fetch up-to-date documentation for a library using Context7",
            "function": self.get_library_docs_tool,
            "parameters": {
                "library_id": {
                    "type": "string",
                    "description": "Exact Context7-compatible library ID retrieved from 'context7_resolve_library_id'"
                },
                "tokens": {
                    "type": "integer",
                    "description": "Maximum number of tokens of documentation to retrieve (default: 10000)",
                    "default": 10000
                },
                "topic": {
                    "type": "string",
                    "description": "Topic to focus documentation on (e.g., 'hooks', 'routing')",
                    "default": None
                }
            }
        })
        
        return tools
    
    def resolve_library_id_tool(self, library_name: str) -> Dict[str, Any]:
        """
        Tool function for resolving a library ID.
        
        Args:
            library_name: Library name to resolve
            
        Returns:
            Resolved library ID information
        """
        try:
            result = self.resolve_library_id(library_name)
            return {
                "success": True,
                "library_name": library_name,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "library_name": library_name,
                "error": str(e)
            }
    
    def get_library_docs_tool(self, library_id: str, tokens: int = 10000, topic: Optional[str] = None) -> Dict[str, Any]:
        """
        Tool function for getting library documentation.
        
        Args:
            library_id: Library ID in Context7-compatible format
            tokens: Maximum number of tokens to retrieve
            topic: Optional topic to focus documentation on
            
        Returns:
            Library documentation
        """
        try:
            result = self.get_library_docs(library_id, tokens, topic)
            return {
                "success": True,
                "library_id": library_id,
                "topic": topic,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "library_id": library_id,
                "topic": topic,
                "error": str(e)
            }
