"""
MCP (Model Context Protocol) client implementation for the Autogen Agents Framework.
"""

import requests
import json
from typing import Dict, Any, Optional, List
from ..config.config_manager import MCPServerConfig

class MCPClient:
    """Client for interacting with MCP servers."""
    
    def __init__(self, config: MCPServerConfig):
        """
        Initialize an MCP client.
        
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
    
    def list_resources(self, cursor: Optional[str] = None) -> Dict[str, Any]:
        """
        List available resources from the MCP server.
        
        Args:
            cursor: Pagination cursor
            
        Returns:
            Dictionary containing resources and pagination information
        """
        url = f"{self.endpoint}/resources"
        params = {}
        if cursor:
            params["cursor"] = cursor
            
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def read_resource(self, uri: str) -> Dict[str, Any]:
        """
        Read a specific resource from the MCP server.
        
        Args:
            uri: Resource URI
            
        Returns:
            Resource content
        """
        url = f"{self.endpoint}/resource"
        params = {"uri": uri}
            
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_library_docs(self, library_id: str, tokens: int = 10000, topic: Optional[str] = None) -> Dict[str, Any]:
        """
        Get documentation for a library from the MCP server.
        
        Args:
            library_id: Library ID in Context7-compatible format
            tokens: Maximum number of tokens to retrieve
            topic: Optional topic to focus documentation on
            
        Returns:
            Library documentation
        """
        url = f"{self.endpoint}/library/docs"
        params = {
            "context7CompatibleLibraryID": library_id,
            "tokens": tokens
        }
        if topic:
            params["topic"] = topic
            
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def resolve_library_id(self, library_name: str) -> Dict[str, Any]:
        """
        Resolve a library name to a Context7-compatible library ID.
        
        Args:
            library_name: Library name to resolve
            
        Returns:
            Dictionary containing resolved library IDs and metadata
        """
        url = f"{self.endpoint}/library/resolve"
        params = {"libraryName": library_name}
            
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def create_autogen_tool(self) -> Dict[str, Any]:
        """
        Create an Autogen-compatible tool definition for this MCP client.
        
        Returns:
            Tool definition dictionary
        """
        return {
            "name": f"mcp_{self.name}",
            "description": f"Access the {self.name} MCP server for additional capabilities",
            "function": self.execute_mcp_command,
            "parameters": {
                "command": {
                    "type": "string",
                    "enum": ["list_resources", "read_resource", "get_library_docs", "resolve_library_id"],
                    "description": "The MCP command to execute"
                },
                "params": {
                    "type": "object",
                    "description": "Parameters for the MCP command"
                }
            }
        }
    
    def execute_mcp_command(self, command: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an MCP command.
        
        Args:
            command: Command to execute
            params: Command parameters
            
        Returns:
            Command result
        """
        if command == "list_resources":
            return self.list_resources(params.get("cursor"))
        elif command == "read_resource":
            return self.read_resource(params["uri"])
        elif command == "get_library_docs":
            return self.get_library_docs(
                params["context7CompatibleLibraryID"],
                params.get("tokens", 10000),
                params.get("topic")
            )
        elif command == "resolve_library_id":
            return self.resolve_library_id(params["libraryName"])
        else:
            raise ValueError(f"Unknown MCP command: {command}")


class MCPManager:
    """Manager for MCP clients."""
    
    def __init__(self):
        """Initialize an MCP manager."""
        self.clients: Dict[str, MCPClient] = {}
    
    def register_client(self, config: MCPServerConfig) -> MCPClient:
        """
        Register an MCP client.
        
        Args:
            config: MCP server configuration
            
        Returns:
            The registered MCP client
        """
        client = MCPClient(config)
        self.clients[config.name] = client
        return client
    
    def get_client(self, name: str) -> Optional[MCPClient]:
        """
        Get an MCP client by name.
        
        Args:
            name: Client name
            
        Returns:
            The MCP client, or None if not found
        """
        return self.clients.get(name)
    
    def get_all_clients(self) -> List[MCPClient]:
        """
        Get all registered MCP clients.
        
        Returns:
            List of all MCP clients
        """
        return list(self.clients.values())
    
    def create_autogen_tools(self) -> List[Dict[str, Any]]:
        """
        Create Autogen-compatible tool definitions for all registered MCP clients.
        
        Returns:
            List of tool definition dictionaries
        """
        return [client.create_autogen_tool() for client in self.clients.values()]
