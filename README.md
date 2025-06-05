# Vertex AI Imagen MCP Server

🎨 **High-quality image generation from text prompts using Google Cloud Vertex AI Imagen API**

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Vertex%20AI-4285F4)](https://cloud.google.com/vertex-ai)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)

A Model Context Protocol (MCP) server that integrates Google Cloud's Vertex AI Imagen models for generating stunning images from text descriptions. Works seamlessly with Claude Desktop and supports both interactive CLI and MCP protocol modes.

## ✨ Features

- 🎨 **Latest AI Models**: Support for Imagen 3.0 and legacy models
- 🔧 **MCP Integration**: Full Model Context Protocol support for Claude Desktop
- 🖥️ **Standalone Mode**: Interactive CLI when MCP libraries aren't available  
- ⚙️ **Rich Options**: Aspect ratios, negative prompts, safety filters, and more
- 🔒 **Built-in Safety**: Automatic content filtering and watermarking
- 🚀 **Easy Setup**: Simple environment variable configuration
- 📚 **Comprehensive Docs**: Detailed guides in English and Korean

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Cloud account with Vertex AI API enabled
- Service account with `Vertex AI User` role

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/vertex-ai-imagen-mcp.git
cd vertex-ai-imagen-mcp
pip install -r requirements.txt
```

### Setup

1. **Create Google Cloud service account** and download JSON key
2. **Set environment variables**:
   ```bash
   export GOOGLE_CLOUD_PROJECT="your-project-id"
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
   export VERTEX_AI_LOCATION="us-central1"
   ```

### Usage

#### Standalone Mode (Recommended for testing)
```bash
python src/imagen_mcp_server.py
```

#### MCP Mode (Claude Desktop integration)
```bash
# Install MCP library
pip install mcp

# Add to Claude Desktop config:
{
  "mcpServers": {
    "vertex-ai-imagen": {
      "command": "python",
      "args": ["/path/to/vertex-ai-imagen-mcp/src/imagen_mcp_server.py"],
      "env": {
        "GOOGLE_CLOUD_PROJECT": "your-project-id",
        "VERTEX_AI_LOCATION": "us-central1",
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/service-account-key.json"
      }
    }
  }
}
```

## 🎨 Usage Examples

### Basic Generation
```python
# Simple prompt
"A serene mountain landscape at sunset"

# With options
{
  "prompt": "A futuristic cityscape with flying cars",
  "negative_prompt": "blurry, low quality",
  "aspect_ratio": "16:9",
  "image_count": 2
}
```

### Advanced Usage
```python
# High-quality generation with specific model
{
  "prompt": "A detailed oil painting of a cat wearing a crown",
  "model_version": "imagen-3.0-generate-002",
  "aspect_ratio": "3:4",
  "safety_setting": "block_medium_and_above",
  "seed": 12345
}
```

## 🛠️ API Reference

### Supported Tools

#### `generate_image`
Generate images from text prompts.

**Parameters:**
- `prompt` (required): Text description of the desired image
- `negative_prompt`: Content to avoid in the generated image
- `image_count`: Number of images to generate (1-4)
- `aspect_ratio`: Image dimensions (`1:1`, `3:4`, `4:3`, `16:9`, `9:16`)
- `model_version`: AI model to use (see supported models below)
- `safety_setting`: Content filter level
- `seed`: Random seed for reproducible results

#### `list_models`
List all available Imagen models and their capabilities.

### Supported Models

| Model | Description | Speed | Quality |
|-------|-------------|-------|---------|
| `imagen-3.0-generate-002` | Latest high-quality model | Medium | Excellent |
| `imagen-3.0-generate-001` | Previous Imagen 3.0 version | Medium | Excellent |
| `imagen-3.0-fast-generate-001` | Fast generation model | Fast | Good |
| `imagegeneration@006` | Stable legacy model | Medium | Good |
| `imagegeneration@005` | Previous legacy version | Medium | Good |

## 📁 Project Structure

```
vertex-ai-imagen-mcp/
├── src/
│   └── imagen_mcp_server.py      # Main MCP server implementation
├── examples/
│   ├── basic_usage.py            # Basic usage examples
│   └── advanced_usage.py         # Advanced features demo
├── docs/
│   ├── setup.md                  # Detailed setup guide
│   ├── api.md                    # API documentation
│   ├── troubleshooting.md        # Common issues and solutions
│   ├── ko/                       # Korean documentation
│   │   ├── README.md
│   │   ├── setup.md
│   │   └── api.md
│   └── images/                   # Documentation images
├── tests/
│   ├── test_api.py              # API tests
│   └── test_mcp.py              # MCP integration tests
├── requirements.txt              # Python dependencies
├── requirements-dev.txt          # Development dependencies
├── setup.py                      # Package configuration
├── .github/
│   └── workflows/
│       ├── test.yml             # Automated testing
│       └── release.yml          # Release automation
├── LICENSE                       # MIT License
└── README.md                     # This file
```

## 🌐 Documentation

- **English**: [Setup Guide](docs/setup.md) | [API Reference](docs/api.md) | [Troubleshooting](docs/troubleshooting.md)
- **한국어**: [설정 가이드](docs/ko/setup.md) | [API 참조](docs/ko/api.md) | [문제 해결](docs/ko/troubleshooting.md)

## 🧪 Development

### Local Development Setup

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/vertex-ai-imagen-mcp.git
cd vertex-ai-imagen-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Run linting
black src/ tests/
flake8 src/ tests/
```

### Running Examples

```bash
# Basic usage
python examples/basic_usage.py

# Advanced features
python examples/advanced_usage.py
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`python -m pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Code Style

- Use [Black](https://black.readthedocs.io/) for code formatting
- Follow [PEP 8](https://pep8.org/) style guidelines
- Add type hints where appropriate
- Write descriptive commit messages

## 📋 Requirements

### System Requirements
- Python 3.8 or higher
- Internet connection for API calls
- Google Cloud account with billing enabled

### Python Dependencies
- `requests>=2.31.0` - HTTP client for API calls
- `google-auth>=2.23.0` - Google Cloud authentication
- `google-auth-oauthlib>=1.1.0` - OAuth2 support
- `google-auth-httplib2>=0.1.1` - HTTP transport
- `mcp>=0.1.0` - Model Context Protocol (optional)

### Google Cloud Requirements
- Project with Vertex AI API enabled
- Service account with `Vertex AI User` role
- Billing account linked to the project

## 💰 Pricing

This tool uses Google Cloud Vertex AI Imagen API, which has usage-based pricing:

- **Pay per image generated**
- **Pricing varies by model and resolution**
- **Free tier available for new users**

For detailed pricing information, visit the [Google Cloud Pricing page](https://cloud.google.com/vertex-ai/pricing).

### Cost Optimization Tips

- Use `imagen-3.0-fast-generate-001` for faster, cheaper generation
- Generate multiple images in a single request when possible
- Set up billing alerts to monitor usage
- Use lower resolution for prototyping

## 🔒 Security & Privacy

- **Service Account Keys**: Store securely and rotate regularly
- **Content Filtering**: Built-in safety filters prevent harmful content
- **Data Privacy**: Images are not stored by Google after generation
- **Network Security**: All API calls use HTTPS/TLS encryption

## ❓ Troubleshooting

### Common Issues

**Authentication Error (403 Forbidden)**
```bash
# Solution: Check service account permissions
# Ensure "Vertex AI User" role is assigned
```

**API Not Enabled Error**
```bash
# Solution: Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com
```

**Project Not Found**
```bash
# Solution: Verify environment variables
echo $GOOGLE_CLOUD_PROJECT
echo $GOOGLE_APPLICATION_CREDENTIALS
```

For more detailed troubleshooting, see our [Troubleshooting Guide](docs/troubleshooting.md).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Cloud Vertex AI** - For providing powerful AI image generation capabilities
- **Model Context Protocol** - For enabling seamless AI tool integration
- **Anthropic Claude** - For inspiring better human-AI collaboration
- **Open Source Community** - For making this project possible

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/vertex-ai-imagen-mcp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/vertex-ai-imagen-mcp/discussions)
- **Documentation**: [Full Documentation](docs/)

## 🌟 Show Your Support

If this project helps you, please consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 📝 Contributing to documentation
- 🔗 Sharing with others

---

**Made with ❤️ by the community for the community**

*Happy image generating! 🎨*
