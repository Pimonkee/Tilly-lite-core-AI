# Contributing to Tilly AI

Thank you for your interest in contributing to Tilly AI! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Feature Requests](#feature-requests)

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow. Please be respectful, inclusive, and considerate in all interactions.

### Our Standards

- Be welcoming and inclusive
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- Basic understanding of FastAPI and async Python
- Familiarity with AI/ML concepts (helpful but not required)

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Tilly-lite-core-AI.git
   cd Tilly-lite-core-AI
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

6. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Branch Naming

Use descriptive branch names:
- `feature/add-voice-support` - for new features
- `fix/chat-response-bug` - for bug fixes
- `docs/update-readme` - for documentation
- `refactor/improve-pipeline` - for code refactoring

### Commit Messages

Write clear, descriptive commit messages:

```
feat: add voice input support

- Implement microphone capture
- Add speech-to-text conversion
- Update UI with voice button
```

Format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line length**: 100 characters max
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings, single quotes for dict keys
- **Imports**: Group in order: standard library, third-party, local

### Code Formatting

Use these tools to format your code:

```bash
# Format with black
black src/

# Sort imports with isort
isort src/

# Check with flake8
flake8 src/

# Type checking with mypy
mypy src/
```

### Documentation

- Add docstrings to all public functions, classes, and modules
- Use Google-style docstrings
- Include type hints for function parameters and return values
- Add inline comments for complex logic

Example:

```python
def process_message(text: str, context: TillyContext) -> tuple[str, TillyContext]:
    """
    Process a user message through the Tilly pipeline.
    
    Args:
        text: The user's input message
        context: Current conversation context
        
    Returns:
        A tuple of (response_text, updated_context)
        
    Raises:
        ValueError: If text is empty
    """
    if not text.strip():
        raise ValueError("Message cannot be empty")
    
    # Process through pipeline
    ...
```

## Testing

### Writing Tests

- Write tests for all new features
- Maintain or improve code coverage
- Use pytest for testing
- Place tests in the `tests/` directory

Example test:

```python
import pytest
from src.tilly.core.tilly_intent_router import TillyRouter
from src.tilly.core.tilly_conversation_context import TillyContext

@pytest.mark.asyncio
async def test_crisis_detection():
    """Test that crisis messages are properly detected"""
    router = TillyRouter()
    context = TillyContext(user_text="I want to end it all")
    
    text, updated_context = await router.process("I want to end it all", context)
    
    assert updated_context.intent.value == "crisis"
    assert updated_context.crisis_level > 0.7
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_router.py

# Run with verbose output
pytest -v
```

## Submitting Changes

### Pull Request Process

1. **Update your branch** with the latest main:
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-feature-branch
   git rebase main
   ```

2. **Ensure all tests pass**:
   ```bash
   pytest
   ```

3. **Run code quality checks**:
   ```bash
   black src/
   isort src/
   flake8 src/
   mypy src/
   ```

4. **Push your changes**:
   ```bash
   git push origin your-feature-branch
   ```

5. **Create a Pull Request** on GitHub with:
   - Clear title describing the change
   - Detailed description of what changed and why
   - Reference any related issues
   - Screenshots for UI changes
   - Test results

### Pull Request Checklist

- [ ] Code follows the project's style guidelines
- [ ] Self-review of code completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] Tests added/updated and passing
- [ ] No new warnings introduced
- [ ] PR description is clear and complete

## Reporting Bugs

### Before Submitting a Bug Report

- Check the [issue tracker](https://github.com/Pimonkee/Tilly-lite-core-AI/issues) for existing reports
- Try the latest version of the code
- Collect information about the bug

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Start the application with '...'
2. Send message '...'
3. See error

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Environment:**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.11]
- Tilly version: [e.g., 1.0.0]
- LLM provider: [e.g., Gemini]

**Additional context**
Any other relevant information, logs, screenshots, etc.
```

## Feature Requests

We welcome feature requests! Please:

1. Check if the feature has already been requested
2. Clearly describe the feature and its benefits
3. Provide examples of how it would be used
4. Consider if it aligns with Tilly's core mission

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
What you want to happen.

**Describe alternatives you've considered**
Other solutions you've thought about.

**Use cases**
How would this feature be used?

**Additional context**
Any other relevant information, mockups, examples, etc.
```

## Development Tips

### Running in Development Mode

```bash
# With auto-reload
python run.py --reload

# With custom port
python run.py --port 8080

# Debug mode
TILLY_LOG_LEVEL=DEBUG python run.py
```

### Debugging

- Use Python debugger (pdb) for debugging
- Check logs in `data/logs/tilly.log`
- Use FastAPI's `/docs` endpoint to test API
- Enable verbose logging with `TILLY_LOG_LEVEL=DEBUG`

### Common Issues

**Import errors**: Make sure you're in the virtual environment and dependencies are installed

**API key errors**: Check your `.env` file has valid API keys

**Port conflicts**: Change the port with `--port` flag

**Database errors**: Clear the data directory if needed: `rm -rf data/`

## Questions?

If you have questions not covered here:

- Check the [documentation](docs/)
- Ask in [GitHub Discussions](https://github.com/Pimonkee/Tilly-lite-core-AI/discussions)
- Open an [issue](https://github.com/Pimonkee/Tilly-lite-core-AI/issues)

## Recognition

Contributors will be recognized in:
- The project README
- Release notes
- GitHub's contributor graph

Thank you for contributing to Tilly AI! Together, we're building something that can genuinely help people. 💜
