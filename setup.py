#!/usr/bin/env python3
"""
Setup script for Vertex AI Imagen MCP Server
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

# Get version from environment or default
version = os.getenv("VERSION", "1.0.0")

setup(
    name="vertex-ai-imagen-mcp",
    version=version,
    author="Kevin Park & Claude",
    author_email="your-email@example.com",
    description="Google Cloud Vertex AI Imagen MCP Server for high-quality image generation",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/vertex-ai-imagen-mcp",
    project_urls={
        "Bug Reports": "https://github.com/YOUR_USERNAME/vertex-ai-imagen-mcp/issues",
        "Source": "https://github.com/YOUR_USERNAME/vertex-ai-imagen-mcp",
        "Documentation": "https://github.com/YOUR_USERNAME/vertex-ai-imagen-mcp/blob/main/docs/",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Multimedia :: Graphics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Framework :: AsyncIO",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "mcp": ["mcp>=0.1.0"],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "docs": [
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "imagen-mcp-server=imagen_mcp_server:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    keywords=[
        "vertex-ai",
        "imagen",
        "google-cloud",
        "mcp",
        "model-context-protocol",
        "image-generation",
        "ai",
        "machine-learning",
        "claude",
        "anthropic",
    ],
    zip_safe=False,
)
