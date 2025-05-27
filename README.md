# AI Agent

A modular AI Agent implementation built with Python, designed for extensibility and maintainability.

## Features

- Modular architecture with clean separation of concerns
- Type-safe implementation with comprehensive type hints
- Async support for concurrent operations
- Comprehensive logging and error handling
- Configuration management with environment variables
- Full test coverage with pytest

## Project Structure

```
src/
├── ai_agent/
│   ├── __init__.py
│   ├── main.py              # Entry point and CLI
│   ├── config.py            # Configuration management
│   ├── models/              # Data classes and DTOs
│   │   ├── __init__.py
│   │   ├── agent.py         # Agent-related models
│   │   └── message.py       # Message models
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── agent_service.py # Core agent logic
│   │   ├── llm_service.py   # LLM integration
│   │   └── memory_service.py# Memory management
│   └── utils/               # Utility functions
│       ├── __init__.py
│       ├── logger.py        # Logging setup
│       └── helpers.py       # Helper functions
tests/                       # Test suite
├── __init__.py
├── test_services/
├── test_models/
└── test_utils/
```

## Setup

### Prerequisites

- Python 3.11+
- Poetry (recommended) or pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-agent
   ```

2. **Install dependencies with Poetry**
   ```bash
   poetry install
   ```

   Or with pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Install pre-commit hooks (recommended)**
   ```bash
   poetry run pre-commit install
   ```

## Usage

### Basic Usage

```bash
# Run the AI agent
poetry run ai-agent

# Or with Python
poetry run python -m ai_agent.main
```

### Development

```bash
# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=src --cov-report=html

# Format code
poetry run black src tests

# Lint code
poetry run flake8 src tests

# Type checking
poetry run mypy src
```

## Configuration

The agent uses environment variables for configuration. Copy `.env.example` to `.env` and modify as needed:

```bash
# LLM Configuration
OPENAI_API_KEY=your_openai_api_key
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.7

# Agent Configuration
AGENT_NAME=AI Assistant
AGENT_DESCRIPTION=A helpful AI agent

# Logging
LOG_LEVEL=INFO
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 