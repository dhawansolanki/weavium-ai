# Autogen Agents Framework

A comprehensive framework for creating and managing multiple agents using Microsoft's Autogen library with Azure OpenAI integration, custom tools, MCP server capabilities, memory persistence, and specialized agents.

## Features

- **Multi-agent system architecture** - Create and manage multiple agents with different roles and capabilities
- **Azure OpenAI integration** - Seamless integration with Azure OpenAI services
- **Custom tool integration** - Extend agent capabilities with custom tools
- **MCP server connectivity** - Connect to Model Context Protocol servers like Context7
- **Memory persistence** - Store and retrieve agent memories and conversation history
- **Specialized agents** - Create domain-specific agents with enhanced knowledge
- **Group chat support** - Facilitate multi-agent conversations and collaborations
- **Command-line interface** - Run agents and conversations from the command line
- **Comprehensive logging** - Track agent actions and conversations
- **Docker support** - Run the framework in containerized environments

## Setup

### Basic Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure your credentials in `.env` file (see Configuration section)
4. Run an example:
   ```
   python examples/basic_conversation.py
   ```

### Installation as a Package

You can also install the framework as a package:

```
pip install -e .
```

This will make the `autogen-framework` command available in your environment.

### Docker Setup

To run the framework in a Docker container:

```
docker-compose up
```

## Project Structure

- `src/` - Core framework code
  - `agents/` - Agent definitions and configurations
    - `base_agent.py` - Base agent class
    - `assistant_agent.py` - Assistant agent implementation
    - `user_proxy_agent.py` - User proxy agent implementation
    - `specialized_agent.py` - Domain-specific agent implementation
    - `group_chat.py` - Group chat implementation
  - `tools/` - Custom tools for agents
    - `tool_registry.py` - Tool registration system
    - `basic_tools.py` - Basic tool implementations
  - `mcp/` - MCP server integration
    - `mcp_client.py` - Generic MCP client
    - `context7_client.py` - Context7-specific client
  - `config/` - Configuration utilities
    - `config_manager.py` - Configuration management
    - `azure_openai.py` - Azure OpenAI integration
  - `utils/` - Utility modules
    - `memory_manager.py` - Memory persistence
    - `logging_utils.py` - Logging utilities
  - `framework.py` - Main framework class
  - `cli.py` - Command-line interface
- `examples/` - Example implementations
  - `basic_conversation.py` - Simple conversation between two agents
  - `multi_agent_collaboration.py` - Multiple agents working together
  - `azure_openai_integration.py` - Azure OpenAI integration example
  - `mcp_server_integration.py` - MCP server integration example
  - `context7_integration_example.py` - Context7 integration example
  - `group_chat_collaboration.py` - Group chat example
  - `specialized_agent_example.py` - Domain-specific agents example
  - `memory_persistence_example.py` - Memory persistence example
  - `advanced_group_chat_with_memory.py` - Advanced group chat with memory
  - `comprehensive_framework_demo.py` - Comprehensive framework demonstration
- `tests/` - Test cases
  - `test_memory_manager.py` - Memory manager tests
  - `test_context7_client.py` - Context7 client tests
  - `test_framework_integration.py` - Framework integration tests

## Configuration

Create a `.env` file with your credentials based on the provided `.env.example`:

```
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_VERSION=2023-05-15
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name

# MCP Server Configuration
CONTEXT7_API_KEY=your_context7_api_key
CONTEXT7_ENDPOINT=https://api.context7.com/v1

# Memory Configuration
MEMORY_DB_PATH=./data/agent_memories.db
MEMORY_ENABLE=true

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=./logs/autogen_framework.log
```

## Command-Line Usage

The framework provides a command-line interface for common operations:

```
# Create an agent
./autogen-framework create-agent --type assistant --name MyAssistant --system-message "You are a helpful assistant."

# Run a conversation
./autogen-framework run-conversation --message "Hello, how can you help me?"

# Run a group chat with specialized agents
./autogen-framework run-group-chat --specialized --message "I need help with a project."
```

## Running Examples

Use the `run_example.py` script to run any of the provided examples:

```
# List available examples
python run_example.py --list

# Run a specific example
python run_example.py basic_conversation
```

## Running Tests

Use the `run_tests.py` script to run the test suite:

```
# Run all tests
python run_tests.py

# Run tests with verbose output
python run_tests.py --verbose

# Run tests in a specific directory
python run_tests.py --path tests/test_memory_manager.py
```

## Memory Persistence

The framework includes a memory manager for storing and retrieving agent memories and conversation history. To use it:

```python
from src.utils.memory_manager import MemoryManager

# Create a memory manager
memory_manager = MemoryManager(db_path="agent_memories.db")

# Store a memory
memory_manager.store_memory(
    agent_name="MyAgent",
    memory_type="fact",
    content="The sky is blue"
)

# Retrieve memories
memories = memory_manager.retrieve_memories("MyAgent", "fact")
```

## MCP Server Integration

The framework supports integration with Model Context Protocol (MCP) servers like Context7:

```python
from src.mcp.context7_client import Context7Client
from src.config.config_manager import MCPServerConfig

# Create a Context7 client
config = MCPServerConfig(
    name="context7",
    endpoint="https://api.context7.com/v1",
    api_key="your_api_key"
)
context7_client = Context7Client(config)

# Resolve a library ID
result = context7_client.resolve_library_id("React")

# Get library documentation
docs = context7_client.get_library_docs(result["libraryId"])
```

## License

MIT
