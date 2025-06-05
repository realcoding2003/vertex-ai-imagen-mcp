# Contributing to Vertex AI Imagen MCP Server

First off, thank you for considering contributing to Vertex AI Imagen MCP Server! It's people like you that make this project great.

## 🤝 How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** with code snippets if applicable
- **Describe the behavior you observed** and what behavior you expected
- **Include screenshots** if they help explain the problem
- **Include environment details** (Python version, OS, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a step-by-step description** of the suggested enhancement
- **Provide specific examples** to demonstrate the enhancement
- **Describe the current behavior** and **explain the expected behavior**
- **Explain why this enhancement would be useful**

### Pull Requests

The process described here has several goals:

- Maintain the project's quality
- Fix problems that are important to users
- Engage the community in working toward the best possible version
- Enable a sustainable system for maintainers to review contributions

Please follow these steps to have your contribution considered by the maintainers:

1. **Follow the styleguides**
2. **After you submit your pull request**, verify that all status checks are passing

## 🏗️ Development Setup

### Prerequisites

- Python 3.8+
- Git
- Google Cloud account (for testing)

### Setting up the development environment

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/vertex-ai-imagen-mcp.git
   cd vertex-ai-imagen-mcp
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Set up pre-commit hooks** (optional but recommended)
   ```bash
   pre-commit install
   ```

5. **Set up environment variables for testing**
   ```bash
   export GOOGLE_CLOUD_PROJECT="your-test-project"
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/test-key.json"
   export VERTEX_AI_LOCATION="us-central1"
   ```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run tests with coverage
python -m pytest --cov=src

# Run specific test file
python -m pytest tests/test_api.py

# Run tests in verbose mode
python -m pytest -v
```

### Writing Tests

- Write tests for any new functionality
- Ensure tests cover both success and failure cases
- Use descriptive test names
- Mock external API calls to avoid charges during testing

Example test structure:
```python
def test_generate_image_success():
    """Test successful image generation."""
    # Test implementation
    pass

def test_generate_image_invalid_prompt():
    """Test error handling for invalid prompts."""
    # Test implementation
    pass
```

## 📝 Code Style

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line length**: 88 characters (Black default)
- **String quotes**: Use double quotes for strings
- **Import ordering**: Use `isort` for consistent import ordering

### Formatting Tools

```bash
# Format code with Black
black src/ tests/ examples/

# Sort imports with isort
isort src/ tests/ examples/

# Check code style with flake8
flake8 src/ tests/ examples/

# Type checking with mypy (optional)
mypy src/
```

### Code Quality Checklist

- [ ] Code is formatted with Black
- [ ] Imports are sorted with isort
- [ ] No flake8 violations
- [ ] Type hints are added where appropriate
- [ ] Docstrings follow Google style
- [ ] Tests are added for new functionality
- [ ] Tests pass locally

## 📚 Documentation

### Writing Documentation

- Use clear, concise language
- Include code examples for complex concepts
- Update both English and Korean versions when applicable
- Follow the existing documentation structure

### Documentation Structure

```
docs/
├── setup.md              # Setup instructions
├── api.md                # API reference
├── troubleshooting.md    # Common issues
├── ko/                   # Korean translations
│   ├── setup.md
│   ├── api.md
│   └── troubleshooting.md
└── images/               # Screenshots and diagrams
```

## 🔄 Git Workflow

### Branch Naming

- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Examples:
```
feat: add support for Imagen 3.0 fast model
fix: handle authentication timeout errors
docs: update setup guide with new requirements
test: add unit tests for image generation
```

### Pull Request Process

1. **Create a feature branch** from `main`
2. **Make your changes** following the style guide
3. **Add or update tests** as needed
4. **Update documentation** if necessary
5. **Ensure all tests pass** locally
6. **Create a pull request** with:
   - Clear title and description
   - Reference to related issues
   - Screenshots if UI changes
   - Checklist of changes made

## 🏷️ Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):

- `MAJOR.MINOR.PATCH`
- `1.0.0` - Major release
- `1.1.0` - Minor release (new features)
- `1.0.1` - Patch release (bug fixes)

### Release Checklist

- [ ] Update version in `setup.py`
- [ ] Update `CHANGELOG.md`
- [ ] Ensure all tests pass
- [ ] Create release notes
- [ ] Tag the release
- [ ] Publish to PyPI (if applicable)

## 🌍 Internationalization

### Adding Translations

We support multiple languages:

1. **Create language directory** in `docs/`
2. **Translate all documentation files**
3. **Update README links** to include new language
4. **Test all links and examples**

Currently supported languages:
- English (default)
- Korean (`docs/ko/`)

## 🚨 Security

### Reporting Security Vulnerabilities

Please do not report security vulnerabilities through public GitHub issues. Instead:

1. Email security concerns to the maintainers
2. Include as much detail as possible
3. Allow time for the issue to be addressed before public disclosure

### Security Best Practices

- Never commit API keys or credentials
- Use environment variables for sensitive data
- Keep dependencies up to date
- Follow Google Cloud security best practices

## 💬 Community

### Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code.

### Getting Help

- **GitHub Discussions** - For questions and community discussion
- **GitHub Issues** - For bug reports and feature requests
- **Documentation** - Check the docs first for common questions

## 🎉 Recognition

Contributors will be recognized in:

- `CONTRIBUTORS.md` file
- Release notes for significant contributions
- GitHub contributors page

Thank you for contributing to make this project better! 🚀

---

*This document is a living document and will be updated as the project evolves.*
