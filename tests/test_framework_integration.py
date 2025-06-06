"""
Integration tests for the Autogen Agents Framework.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import tempfile

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.framework import AgentFramework
from src.utils.memory_manager import MemoryManager
from src.config.config_manager import AgentConfig, MCPServerConfig

class TestFrameworkIntegration(unittest.TestCase):
    """Integration tests for the Autogen Agents Framework."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary database file for memory manager
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_db.close()
        
        # Create a framework instance
        self.framework = AgentFramework()
        
        # Create a memory manager
        self.memory_manager = MemoryManager(db_path=self.temp_db.name)
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Remove the temporary database file
        os.unlink(self.temp_db.name)
    
    @patch('autogen.ConversableAgent')
    def test_create_agent(self, mock_agent):
        """Test creating an agent."""
        # Mock the agent instance
        mock_agent_instance = MagicMock()
        mock_agent.return_value = mock_agent_instance
        
        # Create an assistant agent
        agent = self.framework.create_agent(
            agent_type="assistant",
            name="TestAssistant",
            description="Test assistant agent",
            system_message="You are a test assistant.",
            human_input_mode="NEVER"
        )
        
        # Verify the agent was created with the correct parameters
        self.assertEqual(agent.name, "TestAssistant")
        self.assertEqual(agent.description, "Test assistant agent")
        self.assertEqual(agent.system_message, "You are a test assistant.")
    
    @patch('autogen.ConversableAgent')
    def test_create_specialized_agent(self, mock_agent):
        """Test creating a specialized agent."""
        # Mock the agent instance
        mock_agent_instance = MagicMock()
        mock_agent.return_value = mock_agent_instance
        
        # Create domain knowledge
        domain_knowledge = {
            "instructions": "You are a finance specialist.",
            "guidelines": ["Follow financial regulations", "Use accurate data"],
            "examples": ["When analyzing stocks, consider market trends."]
        }
        
        # Create a specialized agent
        agent = self.framework.create_agent(
            agent_type="specialized",
            name="FinanceSpecialist",
            description="Finance specialist agent",
            system_message="You are a finance specialist.",
            domain="finance",
            domain_knowledge=domain_knowledge,
            human_input_mode="NEVER"
        )
        
        # Verify the agent was created with the correct parameters
        self.assertEqual(agent.name, "FinanceSpecialist")
        self.assertEqual(agent.description, "Finance specialist agent")
        self.assertEqual(agent.domain, "finance")
        self.assertEqual(agent.domain_knowledge, domain_knowledge)
    
    def test_register_tool(self):
        """Test registering a tool."""
        # Define a simple tool function
        def add_numbers(a, b):
            return a + b
        
        # Register the tool
        self.framework.register_tool(
            name="add_numbers",
            description="Add two numbers together",
            function=add_numbers,
            parameters={
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"}
            }
        )
        
        # Verify the tool was registered
        self.assertIn("add_numbers", self.framework.tool_registry.tools)
        tool = self.framework.tool_registry.get_tool("add_numbers")
        self.assertEqual(tool.name, "add_numbers")
        self.assertEqual(tool.description, "Add two numbers together")
        self.assertEqual(tool.function, add_numbers)
    
    @patch('src.mcp.mcp_client.MCPClient')
    def test_register_mcp_server(self, mock_mcp_client):
        """Test registering an MCP server."""
        # Mock the MCP client
        mock_client_instance = MagicMock()
        mock_mcp_client.return_value = mock_client_instance
        
        # Create MCP server config
        config = MCPServerConfig(
            name="test_server",
            endpoint="https://test-server.com/api",
            api_key="test_api_key"
        )
        
        # Register the MCP server
        self.framework.register_mcp_server(config)
        
        # Verify the MCP server was registered
        self.assertIn("test_server", self.framework.mcp_manager.servers)
    
    @patch('autogen.ConversableAgent')
    def test_memory_integration(self, mock_agent):
        """Test integration with memory manager."""
        # Mock the agent instance
        mock_agent_instance = MagicMock()
        mock_agent.return_value = mock_agent_instance
        
        # Create an assistant agent
        agent = self.framework.create_agent(
            agent_type="assistant",
            name="MemoryAgent",
            description="Agent with memory",
            system_message="You are an agent with memory.",
            human_input_mode="NEVER"
        )
        
        # Store a memory for the agent
        self.memory_manager.store_memory(
            agent_name="MemoryAgent",
            memory_type="fact",
            content="The sky is blue"
        )
        
        # Retrieve the memory
        memories = self.memory_manager.retrieve_memories("MemoryAgent", "fact")
        
        # Verify the memory was stored and retrieved correctly
        self.assertEqual(len(memories), 1)
        self.assertEqual(memories[0]["content"], "The sky is blue")
        
        # Create a conversation
        self.memory_manager.create_conversation("test-conversation", "Test Conversation")
        
        # Add a message to the conversation
        self.memory_manager.add_message(
            conversation_id="test-conversation",
            sender="User",
            receiver="MemoryAgent",
            content="Hello, agent!"
        )
        
        # Retrieve the conversation history
        history = self.memory_manager.get_conversation_history("test-conversation")
        
        # Verify the message was stored and retrieved correctly
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["sender"], "User")
        self.assertEqual(history[0]["receiver"], "MemoryAgent")
        self.assertEqual(history[0]["content"], "Hello, agent!")
    
    @patch('autogen.GroupChat')
    @patch('autogen.GroupChatManager')
    def test_group_chat(self, mock_manager, mock_group_chat):
        """Test creating and starting a group chat."""
        # Mock the group chat and manager instances
        mock_group_chat_instance = MagicMock()
        mock_group_chat.return_value = mock_group_chat_instance
        
        mock_manager_instance = MagicMock()
        mock_manager.return_value = mock_manager_instance
        
        # Create mock agents
        mock_agent1 = MagicMock()
        mock_agent1.name = "Agent1"
        
        mock_agent2 = MagicMock()
        mock_agent2.name = "Agent2"
        
        mock_user = MagicMock()
        mock_user.name = "User"
        
        # Create a group chat
        group_chat = self.framework.create_group_chat(
            agents=[mock_agent1, mock_agent2, mock_user],
            messages=[],
            max_round=10
        )
        
        # Create a group chat manager
        manager = self.framework.create_group_chat_manager(
            groupchat=group_chat,
            name="GroupChatManager",
            description="Test group chat manager",
            system_message="You are managing a group chat."
        )
        
        # Verify the group chat and manager were created
        self.assertEqual(mock_group_chat.call_count, 1)
        self.assertEqual(mock_manager.call_count, 1)
        
        # Start the group chat
        self.framework.start_group_chat(
            manager=manager,
            message="Hello, group!"
        )
        
        # Verify the group chat was started
        mock_manager_instance.initiate_chat.assert_called_once()

if __name__ == "__main__":
    unittest.main()
