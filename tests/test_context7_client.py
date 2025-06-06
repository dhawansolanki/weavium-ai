"""
Unit tests for the Context7 MCP client.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.mcp.context7_client import Context7Client
from src.config.config_manager import MCPServerConfig

class TestContext7Client(unittest.TestCase):
    """Test cases for the Context7 MCP client."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = MCPServerConfig(
            name="context7",
            endpoint="https://api.context7.com/v1",
            api_key="test_api_key"
        )
        self.client = Context7Client(self.config)
    
    def test_init(self):
        """Test client initialization."""
        self.assertEqual(self.client.name, "context7")
        self.assertEqual(self.client.endpoint, "https://api.context7.com/v1")
        self.assertEqual(self.client.api_key, "test_api_key")
        self.assertEqual(self.client.headers["Content-Type"], "application/json")
        self.assertEqual(self.client.headers["Authorization"], "Bearer test_api_key")
    
    @patch('requests.get')
    def test_resolve_library_id(self, mock_get):
        """Test resolving a library ID."""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "libraryId": "/vercel/next.js",
            "version": "latest",
            "description": "The React Framework for the Web"
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.client.resolve_library_id("next.js")
        
        # Verify the result
        self.assertEqual(result["libraryId"], "/vercel/next.js")
        self.assertEqual(result["version"], "latest")
        self.assertEqual(result["description"], "The React Framework for the Web")
        
        # Verify the request
        mock_get.assert_called_once_with(
            "https://api.context7.com/v1/resolve-library-id",
            headers=self.client.headers,
            params={"libraryName": "next.js"}
        )
    
    @patch('requests.get')
    def test_get_library_docs(self, mock_get):
        """Test getting library documentation."""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "libraryId": "/vercel/next.js",
            "documentation": "Next.js documentation content...",
            "codeSnippets": ["example code 1", "example code 2"]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.client.get_library_docs("/vercel/next.js", tokens=5000, topic="routing")
        
        # Verify the result
        self.assertEqual(result["libraryId"], "/vercel/next.js")
        self.assertEqual(result["documentation"], "Next.js documentation content...")
        self.assertEqual(result["codeSnippets"], ["example code 1", "example code 2"])
        
        # Verify the request
        mock_get.assert_called_once_with(
            "https://api.context7.com/v1/get-library-docs",
            headers=self.client.headers,
            params={
                "context7CompatibleLibraryID": "/vercel/next.js",
                "tokens": 5000,
                "topic": "routing"
            }
        )
    
    def test_create_autogen_tools(self):
        """Test creating Autogen-compatible tools."""
        tools = self.client.create_autogen_tools()
        
        # Verify that we have two tools
        self.assertEqual(len(tools), 2)
        
        # Verify the resolve library ID tool
        resolve_tool = tools[0]
        self.assertEqual(resolve_tool["name"], "context7_resolve_library_id")
        self.assertEqual(resolve_tool["function"], self.client.resolve_library_id_tool)
        self.assertIn("library_name", resolve_tool["parameters"])
        
        # Verify the get library docs tool
        docs_tool = tools[1]
        self.assertEqual(docs_tool["name"], "context7_get_library_docs")
        self.assertEqual(docs_tool["function"], self.client.get_library_docs_tool)
        self.assertIn("library_id", docs_tool["parameters"])
        self.assertIn("tokens", docs_tool["parameters"])
        self.assertIn("topic", docs_tool["parameters"])
    
    @patch('src.mcp.context7_client.Context7Client.resolve_library_id')
    def test_resolve_library_id_tool(self, mock_resolve):
        """Test the resolve library ID tool function."""
        # Mock successful response
        mock_resolve.return_value = {
            "libraryId": "/vercel/next.js",
            "version": "latest"
        }
        
        # Call the tool function
        result = self.client.resolve_library_id_tool("next.js")
        
        # Verify the result
        self.assertTrue(result["success"])
        self.assertEqual(result["library_name"], "next.js")
        self.assertEqual(result["result"]["libraryId"], "/vercel/next.js")
        
        # Mock exception
        mock_resolve.side_effect = Exception("API error")
        
        # Call the tool function
        result = self.client.resolve_library_id_tool("next.js")
        
        # Verify the result
        self.assertFalse(result["success"])
        self.assertEqual(result["library_name"], "next.js")
        self.assertEqual(result["error"], "API error")
    
    @patch('src.mcp.context7_client.Context7Client.get_library_docs')
    def test_get_library_docs_tool(self, mock_get_docs):
        """Test the get library docs tool function."""
        # Mock successful response
        mock_get_docs.return_value = {
            "libraryId": "/vercel/next.js",
            "documentation": "Documentation content"
        }
        
        # Call the tool function
        result = self.client.get_library_docs_tool("/vercel/next.js", 5000, "routing")
        
        # Verify the result
        self.assertTrue(result["success"])
        self.assertEqual(result["library_id"], "/vercel/next.js")
        self.assertEqual(result["topic"], "routing")
        self.assertEqual(result["result"]["documentation"], "Documentation content")
        
        # Mock exception
        mock_get_docs.side_effect = Exception("API error")
        
        # Call the tool function
        result = self.client.get_library_docs_tool("/vercel/next.js", 5000, "routing")
        
        # Verify the result
        self.assertFalse(result["success"])
        self.assertEqual(result["library_id"], "/vercel/next.js")
        self.assertEqual(result["topic"], "routing")
        self.assertEqual(result["error"], "API error")

if __name__ == "__main__":
    unittest.main()
