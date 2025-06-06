"""
Basic tools for the Autogen Agents Framework.
"""

import os
import requests
import json
from typing import Dict, Any, List, Optional
from .tool_registry import Tool, ToolRegistry

def web_search(query: str, num_results: int = 5) -> Dict[str, Any]:
    """
    Perform a web search (simulated).
    
    Args:
        query: Search query
        num_results: Number of results to return
        
    Returns:
        Search results
    """
    # This is a simulated web search function
    # In a real implementation, you would integrate with a search API
    return {
        "query": query,
        "results": [
            {
                "title": f"Result {i} for {query}",
                "url": f"https://example.com/result{i}",
                "snippet": f"This is a snippet for result {i} related to {query}..."
            }
            for i in range(1, num_results + 1)
        ]
    }

def read_file(file_path: str) -> Dict[str, Any]:
    """
    Read a file and return its contents.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File contents
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return {
            "success": True,
            "content": content,
            "file_path": file_path
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "file_path": file_path
        }

def write_file(file_path: str, content: str) -> Dict[str, Any]:
    """
    Write content to a file.
    
    Args:
        file_path: Path to the file
        content: Content to write
        
    Returns:
        Result of the operation
    """
    try:
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
        return {
            "success": True,
            "message": f"Content written to {file_path}",
            "file_path": file_path
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "file_path": file_path
        }

def http_request(url: str, method: str = "GET", headers: Optional[Dict[str, str]] = None, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Make an HTTP request.
    
    Args:
        url: URL to request
        method: HTTP method
        headers: Request headers
        data: Request data
        
    Returns:
        Response data
    """
    try:
        headers = headers or {}
        method = method.upper()
        
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            return {
                "success": False,
                "error": f"Unsupported HTTP method: {method}"
            }
        
        return {
            "success": True,
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "content": response.text,
            "url": url
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "url": url
        }

def register_basic_tools(registry: ToolRegistry) -> None:
    """
    Register basic tools with a tool registry.
    
    Args:
        registry: Tool registry to register tools with
    """
    registry.register_function(
        name="web_search",
        description="Search the web for information",
        function=web_search,
        parameters={
            "query": {
                "type": "string",
                "description": "Search query"
            },
            "num_results": {
                "type": "integer",
                "description": "Number of results to return",
                "default": 5
            }
        }
    )
    
    registry.register_function(
        name="read_file",
        description="Read a file and return its contents",
        function=read_file,
        parameters={
            "file_path": {
                "type": "string",
                "description": "Path to the file to read"
            }
        }
    )
    
    registry.register_function(
        name="write_file",
        description="Write content to a file",
        function=write_file,
        parameters={
            "file_path": {
                "type": "string",
                "description": "Path to the file to write"
            },
            "content": {
                "type": "string",
                "description": "Content to write to the file"
            }
        }
    )
    
    registry.register_function(
        name="http_request",
        description="Make an HTTP request",
        function=http_request,
        parameters={
            "url": {
                "type": "string",
                "description": "URL to request"
            },
            "method": {
                "type": "string",
                "description": "HTTP method",
                "enum": ["GET", "POST", "PUT", "DELETE"],
                "default": "GET"
            },
            "headers": {
                "type": "object",
                "description": "Request headers"
            },
            "data": {
                "type": "object",
                "description": "Request data for POST or PUT requests"
            }
        }
    )
