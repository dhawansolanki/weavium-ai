# Autogen Agents Framework Documentation (Part 4)

## Command Line Interface

The Autogen Agents Framework includes a powerful command-line interface (CLI) that allows users to create agents, run conversations, and manage the framework without writing code.

### Installation

The CLI is automatically installed when you install the framework:

```bash
pip install autogen-agents-framework
```

This installs the `autogen-framework` command.

### Available Commands

#### Create Agent

Create a new agent:

```bash
autogen-framework create-agent <agent_type> <name> <description> [options]
```

Options:
- `--system-message TEXT`: System message for the agent
- `--llm-config FILE`: Path to LLM configuration file
- `--tools TEXT`: Comma-separated list of tool names
- `--human-input-mode TEXT`: Human input mode (ALWAYS, TERMINATE, NEVER)
- `--code-execution-config FILE`: Path to code execution configuration file

Example:
```bash
autogen-framework create-agent assistant ResearchAssistant "Research specialist" --system-message "You are a research specialist."
```

#### Run Conversation

Run a conversation between two agents:

```bash
autogen-framework run-conversation <sender> <receiver> <message> [options]
```

Options:
- `--max-turns INTEGER`: Maximum number of conversation turns
- `--save-history`: Save conversation history to memory

Example:
```bash
autogen-framework run-conversation UserProxy ResearchAssistant "Find information about climate change"
```

#### Run Group Chat

Run a group chat with multiple agents:

```bash
autogen-framework run-group-chat <manager> <agents> <message> [options]
```

Options:
- `--max-rounds INTEGER`: Maximum number of conversation rounds
- `--save-history`: Save conversation history to memory

Example:
```bash
autogen-framework run-group-chat GroupChatManager "UserProxy,ResearchAssistant,Coder,Planner" "Create a climate change visualization app"
```

#### List Agents

List all available agents:

```bash
autogen-framework list-agents
```

#### List Tools

List all available tools:

```bash
autogen-framework list-tools [--category TEXT]
```

#### Memory Commands

Manage the memory system:

```bash
# Store a memory
autogen-framework store-memory <agent_name> <memory_type> <content>

# Retrieve memories
autogen-framework retrieve-memories <agent_name> [--memory-type TEXT]

# Search memories
autogen-framework search-memories <query>
```

### Configuration

The CLI can be configured through environment variables or a configuration file:

```bash
# Set environment variables
export AUTOGEN_FRAMEWORK_CONFIG_FILE=./config.json

# Or use command-line options
autogen-framework --config-file ./config.json <command>
```

## Examples

The Autogen Agents Framework includes several example scripts that demonstrate different aspects of the framework.

### Basic Agent Example

This example demonstrates the basic functionality of creating agents and initiating a conversation:

```python
# basic_agent_example.py
import os
import sys
import dotenv
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

# Load environment variables from .env file
dotenv.load_dotenv()

from src.framework import AgentFramework
from src.utils.logging_utils import setup_logger, get_default_log_file

def main():
    """Run the basic agent example."""
    
    # Set up logging
    log_file = os.getenv("LOG_FILE", get_default_log_file())
    logger = setup_logger(
        name="basic_agent_example",
        level=os.getenv("LOG_LEVEL", "INFO"),
        log_file=log_file
    )
    logger.info("Starting basic agent example")
    
    # Create the agent framework
    framework = AgentFramework()
    logger.info("Created agent framework")
    
    # Create an assistant agent
    assistant = framework.create_agent(
        agent_type="assistant",
        name="BasicAssistant",
        description="A helpful assistant that can answer questions",
        system_message="You are a helpful assistant. Answer questions concisely and accurately.",
        llm_config=None  # Use default config or None for local testing
    )
    logger.info("Created assistant agent")
    
    # Create a user proxy agent
    user_proxy = framework.create_agent(
        agent_type="user_proxy",
        name="UserProxy",
        description="A proxy for the human user",
        system_message="You are a proxy for the human user. You help facilitate the conversation.",
        human_input_mode="NEVER"  # Don't require human input for this example
    )
    logger.info("Created user proxy agent")
    
    # Initiate a conversation
    logger.info("Starting conversation")
    user_proxy.initiate_chat(
        assistant,
        message="Hello! Can you tell me what the agent framework does?"
    )
    
    logger.info("Basic agent example completed")

if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    os.makedirs("./logs", exist_ok=True)
    
    main()
```

### Memory Example

This example demonstrates the memory system:

```python
# simple_memory_example.py
import os
import sys
import uuid
import dotenv
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

# Load environment variables from .env file
dotenv.load_dotenv()

from src.utils.memory_manager import MemoryManager
from src.utils.logging_utils import setup_logger, get_default_log_file

def main():
    """Run the simple memory example."""
    
    # Set up logging
    log_file = os.getenv("LOG_FILE", get_default_log_file())
    logger = setup_logger(
        name="simple_memory_example",
        level=os.getenv("LOG_LEVEL", "INFO"),
        log_file=log_file
    )
    logger.info("Starting simple memory example")
    
    # Create a memory manager
    memory_db_path = os.getenv("MEMORY_DB_PATH", "./data/simple_memory.db")
    memory_manager = MemoryManager(db_path=memory_db_path)
    logger.info(f"Created memory manager with database at {memory_db_path}")
    
    # Generate a unique conversation ID
    conversation_id = str(uuid.uuid4())
    memory_manager.create_conversation(conversation_id, "Simple Memory Example")
    logger.info(f"Created conversation with ID: {conversation_id}")
    
    # Store some memories
    memory_manager.store_memory(
        agent_name="Assistant",
        memory_type="fact",
        content={
            "subject": "user",
            "predicate": "likes",
            "object": "Python programming"
        }
    )
    logger.info("Stored fact memory for Assistant")
    
    memory_manager.store_memory(
        agent_name="Assistant",
        memory_type="skill",
        content={
            "skill_name": "coding",
            "proficiency": "expert",
            "description": "Ability to write clean, efficient Python code"
        }
    )
    logger.info("Stored skill memory for Assistant")
    
    # Add some messages to the conversation
    memory_manager.add_message(
        conversation_id=conversation_id,
        sender="User",
        receiver="Assistant",
        content="Hello, can you help me with a Python problem?"
    )
    logger.info("Added user message to conversation")
    
    memory_manager.add_message(
        conversation_id=conversation_id,
        sender="Assistant",
        receiver="User",
        content="Of course! I'd be happy to help with your Python problem. What specifically are you working on?"
    )
    logger.info("Added assistant message to conversation")
    
    # Retrieve and print conversation history
    print("\n=== Conversation History ===")
    history = memory_manager.get_conversation_history(conversation_id)
    for i, message in enumerate(history, 1):
        print(f"{i}. {message['timestamp']} - {message['sender']} to {message['receiver']}: {message['content']}")
    
    # Retrieve and print agent memories
    print("\n=== Agent Memories ===")
    memories = memory_manager.retrieve_memories("Assistant")
    for memory in memories:
        print(f"- Type: {memory['memory_type']}")
        if isinstance(memory['content'], dict):
            for key, value in memory['content'].items():
                print(f"  {key}: {value}")
        else:
            print(f"  Content: {memory['content']}")
    
    # Search for memories
    print("\n=== Memory Search ===")
    search_results = memory_manager.search_memories("Python")
    print(f"Found {len(search_results)} memories containing 'Python':")
    for memory in search_results:
        print(f"- Agent: {memory['agent_name']}")
        print(f"- Type: {memory['memory_type']}")
        if isinstance(memory['content'], dict):
            for key, value in memory['content'].items():
                print(f"  {key}: {value}")
        else:
            print(f"  Content: {memory['content']}")
    
    logger.info("Simple memory example completed")

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    os.makedirs("./data", exist_ok=True)
    
    # Create logs directory if it doesn't exist
    os.makedirs("./logs", exist_ok=True)
    
    main()
```

### Comprehensive Framework Demo

This example demonstrates the full capabilities of the framework, including multi-agent interactions, memory persistence, MCP integration, specialized agents, and group chat management:

```python
# comprehensive_framework_demo.py
# (See the examples directory for the full implementation)
```

## Testing

The Autogen Agents Framework includes a comprehensive test suite to ensure reliability and correctness.

### Running Tests

To run the tests, use the `run_tests.py` script:

```bash
python run_tests.py
```

Options:
- `--verbose`: Enable verbose output
- `--test-path`: Specify a specific test path to run

### Test Structure

The tests are organized into the following categories:

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test interactions between components
- **End-to-End Tests**: Test complete workflows

### Writing Tests

When contributing to the framework, it's important to write tests for new features:

```python
import unittest
from src.framework import AgentFramework

class TestAgentFramework(unittest.TestCase):
    def setUp(self):
        self.framework = AgentFramework()
    
    def test_create_agent(self):
        agent = self.framework.create_agent(
            agent_type="assistant",
            name="TestAgent",
            description="Test agent",
            system_message="You are a test agent."
        )
        self.assertEqual(agent.name, "TestAgent")
        self.assertEqual(agent.description, "Test agent")
```

## Deployment

The Autogen Agents Framework can be deployed in various environments, from local development to production.

### Local Development

For local development, you can install the framework directly:

```bash
pip install -e .
```

### Docker Deployment

For containerized deployment, use the provided Dockerfile:

```bash
# Build the Docker image
docker build -t autogen-agents-framework .

# Run the container
docker run -it --rm autogen-agents-framework
```

### Production Deployment

For production deployment, consider the following best practices:

- **Environment Variables**: Use environment variables for configuration
- **Secrets Management**: Use a secrets manager for API keys
- **Logging**: Configure appropriate logging levels
- **Monitoring**: Set up monitoring for the application
- **Scaling**: Consider horizontal scaling for high-traffic applications

## Best Practices

### Agent Design

- **Clear Roles**: Give each agent a clear, specific role
- **Detailed System Messages**: Provide detailed system messages to guide agent behavior
- **Appropriate Tools**: Equip agents with the tools they need for their roles
- **Memory Usage**: Use the memory system to maintain context and knowledge

### Memory Management

- **Structured Memories**: Use structured memories (dictionaries) for better organization
- **Memory Types**: Use appropriate memory types for different kinds of information
- **Regular Cleanup**: Periodically clean up outdated or irrelevant memories
- **Search Optimization**: Use specific search queries to find relevant memories

### Conversation Management

- **Clear Instructions**: Provide clear instructions to agents at the start of conversations
- **Appropriate Max Rounds**: Set an appropriate maximum number of rounds for group chats
- **Conversation History**: Save conversation history for important interactions
- **Error Handling**: Implement error handling for conversation failures

### Tool Development

- **Clear Descriptions**: Provide clear descriptions for tools
- **Parameter Validation**: Validate tool parameters to prevent errors
- **Error Handling**: Implement error handling for tool failures
- **Documentation**: Document tool usage and examples

## Troubleshooting

### Common Issues

#### Agent Creation Errors

- **Issue**: Error creating an agent
- **Solution**: Check the agent type and parameters, ensure the LLM configuration is correct

#### Memory Database Errors

- **Issue**: Error accessing the memory database
- **Solution**: Check the database path, ensure the directory exists and is writable

#### Tool Execution Errors

- **Issue**: Error executing a tool
- **Solution**: Check the tool parameters, ensure the tool function is properly implemented

#### MCP Integration Errors

- **Issue**: Error connecting to MCP server
- **Solution**: Check the API key and URL, ensure the server is accessible

### Debugging

- **Enable Debug Logging**: Set `LOG_LEVEL=DEBUG` for detailed logs
- **Check Logs**: Review the log file for error messages
- **Use Verbose Mode**: Use the `--verbose` flag with CLI commands
- **Test Components**: Test individual components to isolate issues

## Future Roadmap

The Autogen Agents Framework is under active development, with several planned enhancements:

### Short-term Goals

- **Enhanced Memory System**: Improved memory retrieval and organization
- **Additional MCP Integrations**: Support for more MCP servers
- **Expanded Tool Library**: More built-in tools for common tasks
- **Improved Documentation**: More examples and tutorials

### Medium-term Goals

- **Web Interface**: A web-based interface for managing agents and conversations
- **Agent Marketplace**: A marketplace for sharing and discovering agents
- **Performance Optimization**: Improved performance for large-scale deployments
- **Advanced Analytics**: Analytics for agent performance and conversation metrics

### Long-term Goals

- **Multi-modal Agents**: Support for agents that can process and generate images, audio, and video
- **Agent Learning**: Agents that can learn and improve over time
- **Collaborative Agent Networks**: Networks of agents that can collaborate across organizations
- **Autonomous Agent Systems**: Systems of agents that can operate autonomously

## Contributing

Contributions to the Autogen Agents Framework are welcome! Here's how you can contribute:

### Getting Started

1. **Fork the Repository**: Fork the repository on GitHub
2. **Clone Your Fork**: Clone your fork to your local machine
3. **Create a Branch**: Create a branch for your changes
4. **Make Changes**: Make your changes to the codebase
5. **Run Tests**: Run the tests to ensure your changes don't break anything
6. **Submit a Pull Request**: Submit a pull request with your changes

### Contribution Guidelines

- **Code Style**: Follow the project's code style (PEP 8 for Python)
- **Documentation**: Document your changes with docstrings and comments
- **Tests**: Write tests for new features and bug fixes
- **Commit Messages**: Write clear, descriptive commit messages

### Code of Conduct

The Autogen Agents Framework project adheres to a code of conduct that promotes a welcoming and inclusive community. Please read and follow the code of conduct when participating in the project.

## License

The Autogen Agents Framework is released under the MIT License:

```
MIT License

Copyright (c) 2023 Your Name or Organization

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
