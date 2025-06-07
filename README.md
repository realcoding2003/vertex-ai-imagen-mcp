# 🎨 Vertex AI Imagen MCP Server

**Languages**: [🇰🇷 한국어](README_KR.md)

---

**Model Context Protocol (MCP) Server for Google Cloud Vertex AI Imagen**

This MCP server enables direct generation of high-quality AI images in Claude Desktop using the [vertex-ai-imagen](https://github.com/realcoding2003/vertex-ai-imagen) package.

## ✨ Key Features

- 🎯 **Simple Setup**: Streamlined architecture based on the `vertex-ai-imagen` package
- 🚀 **Claude Desktop Integration**: Seamless image generation through MCP
- 🎨 **Multiple Model Support**: Imagen 3.0, imagegeneration@006, and more
- 🔧 **Flexible Options**: Aspect ratios, image count, safety settings, etc.
- 🔒 **Secure Authentication**: Google Cloud Service Account based

## 🚀 Quick Start (5-minute Setup)

### 1️⃣ Project Installation

```bash
git clone https://github.com/realcoding2003/vertex-ai-imagen-mcp.git
cd vertex-ai-imagen-mcp
pip install -r requirements.txt
```

### 2️⃣ Google Cloud Authentication Setup

1. Create/select a project in [Google Cloud Console](https://console.cloud.google.com/)
2. [Enable Vertex AI API](https://console.cloud.google.com/marketplace/product/google/aiplatform.googleapis.com)
3. Create a service account and download key file (see detailed guide below)

### 3️⃣ Claude Desktop Configuration

1. **Configuration file location**:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. **Add configuration content**:

```json
{
  "mcpServers": {
    "vertex-ai-imagen": {
      "command": "python",
      "args": ["/absolute/path/to/vertex-ai-imagen-mcp/mcp_server.py"],
      "env": {
        "GOOGLE_CLOUD_PROJECT": "your-actual-project-id",
        "GOOGLE_APPLICATION_CREDENTIALS": "/absolute/path/to/your-key-file.json"
      }
    }
  }
}
```

3. **Restart Claude Desktop**

### 4️⃣ First Image Generation Test

After restarting Claude Desktop: *"Generate a beautiful sunset landscape image"*

---

## 🛠️ Detailed Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/realcoding2003/vertex-ai-imagen-mcp.git
cd vertex-ai-imagen-mcp
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Google Cloud Setup

#### 3.1 Google Cloud Project and API Activation

1. **Access Google Cloud Console**
   - Log in to [Google Cloud Console](https://console.cloud.google.com/)
   - Select an existing project or create a new one

2. **Enable Vertex AI API**
   - Navigate to "APIs & Services" → "Library" from the left menu
   - Search for "Vertex AI API" and click on it
   - Click the "Enable" button to activate the API

   Or enable directly via [this link](https://console.cloud.google.com/marketplace/product/google/aiplatform.googleapis.com)

#### 3.2 Service Account Creation and Key File Download

1. **Create Service Account**
   - Go to "IAM & Admin" → "Service Accounts" in Google Cloud Console
   - Click "Create Service Account"
   - Enter service account details:
     - **Service account name**: `imagen-mcp` (or your preferred name)
     - **Service account ID**: Auto-generated
     - **Description**: `Service account for Imagen MCP Server`
   - Click "Create and Continue"

2. **Grant Permissions**
   - In the "Grant this service account access to project" section
   - Select `Vertex AI User` role from the "Select a role" dropdown
   - Click "Continue"

3. **Generate and Download Key File**
   - Skip the "Grant users access to this service account" section and click "Done"
   - Click on the email address of the newly created service account
   - Go to the "Keys" tab
   - Click "Add Key" → "Create new key"
   - Select key type: **JSON**
   - Click "Create" and the JSON key file will be automatically downloaded

4. **Store Key File in Safe Location**

   ```bash
   # Example: macOS/Linux
   mkdir -p ~/.config/gcloud
   mv ~/Downloads/your-project-id-xxxxxx.json ~/.config/gcloud/imagen-mcp-key.json
   
   # Example: Windows
   mkdir %USERPROFILE%\.config\gcloud
   move %USERPROFILE%\Downloads\your-project-id-xxxxxx.json %USERPROFILE%\.config\gcloud\imagen-mcp-key.json
   ```

### 4. Environment Variable Setup

Set environment variables with the downloaded key file and project information:

**macOS/Linux:**

```bash
export GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.config/gcloud/imagen-mcp-key.json"
```

**Windows (PowerShell):**

```powershell
$env:GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"
$env:GOOGLE_APPLICATION_CREDENTIALS="$HOME\.config\gcloud\imagen-mcp-key.json"
```

> 💡 **How to find Project ID**: Use the ID displayed next to the project name at the top of Google Cloud Console.

## 🔧 Claude Desktop Configuration

### Check Configuration File Location

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### Edit Configuration File

Create/edit the `claude_desktop_config.json` file to register the MCP server:

```json
{
  "mcpServers": {
    "vertex-ai-imagen": {
      "command": "python",
      "args": [
        "/absolute/path/to/vertex-ai-imagen-mcp/mcp_server.py"
      ],
      "env": {
        "GOOGLE_CLOUD_PROJECT": "your-actual-project-id",
        "GOOGLE_APPLICATION_CREDENTIALS": "/absolute/path/to/your-key-file.json"
      }
    }
  }
}
```

> ⚠️ **Important**:
>
> - All paths must be absolute paths
> - Replace `your-actual-project-id` with your actual Google Cloud project ID
> - Replace the key file path with the actual path to your downloaded JSON file

### After Configuration

1. Completely close Claude Desktop
2. Restart Claude Desktop
3. If a 🔧 icon appears in the bottom left, the MCP server has been successfully connected

## 🚀 Usage

### Using in Claude Desktop

After restarting Claude Desktop, you can generate images like this:

```text
Ask Claude: "Generate a beautiful sunset landscape image"
```

### Using Advanced Options

```text
Ask Claude: "Generate an image of a cat traveling through space in 16:9 aspect ratio, 
create 2 images, use the imagen-3.0-fast-generate-001 model, 
and add 'blurry, low quality' as negative prompt"
```

### Specifying Image Save Path

```text
Ask Claude: "Generate a beautiful landscape image and save it in 
/Users/username/Pictures/AI_Images folder with the name 'landscape.png'"
```

### Saving with Exact Filename

```text
Ask Claude: "Generate a website hero image. Make it 16:9 aspect ratio, 
use the imagen-3.0-generate-001 model, and save it as 'hero.png' in 
/Users/kevinpark/Documents/projects/realcoding.github.io/assets/images/posts/ai-tutorial/ 
directory"
```

### Interactive Mode (Without MCP)

```bash
python mcp_server.py
```

## 🎯 Available Tools

### `generate_image`

Generate images from text prompts

**Required Parameters:**

- `prompt` (string): Text prompt for image generation

**Optional Parameters:**

- `negative_prompt` (string): Content to avoid
- `count` (integer, 1-4): Number of images to generate
- `aspect_ratio` (string): Aspect ratio ("1:1", "3:4", "4:3", "16:9", "9:16")
- `model` (string): Model to use (default: "imagegeneration@006")
- `seed` (integer): Seed value for reproducible results
- `safety_setting` (string): Safety filter level (default: "block_some")
- `save_path` (string): Directory path to save images (if not specified, images are only displayed in Claude)
- `filename` (string): Exact filename (with or without extension). **Using this option saves with the specified name without timestamp.**
- `filename_prefix` (string): Filename prefix (default: "generated_image"). **Only used when filename is not specified.**

> 💡 **Filename Behavior**:
>
> - When `filename` is specified: Saves with exact filename (adds _1,_2 etc. for multiple images)
> - When `filename` is not specified: Saves as `{filename_prefix}_{timestamp}_{number}.png` format

### `list_models`

List available Imagen models

## 🤖 Supported Models

| Model Name | Speed | Quality | Use Case |
|------------|-------|---------|----------|
| `imagegeneration@006` | 🟡 Medium | 🟣 Excellent | General purpose |
| `imagen-3.0-generate-001` | 🟡 Medium | 🟣 Excellent | High-quality work |
| `imagen-3.0-generate-002` | 🟡 Medium | 🟣 Excellent | Latest high-quality |
| `imagen-3.0-fast-generate-001` | ⚡ Fast | 🟢 Good | Fast prototyping |

## 🔍 Troubleshooting

### Common Issues

#### 1. Authentication Error

```bash
❌ Authentication failed: could not find default credentials
```

**Solution:**

- Check if `GOOGLE_APPLICATION_CREDENTIALS` environment variable is set correctly
- Verify that the service account key file exists and is readable

#### 2. Permission Error

```bash
❌ 403 Forbidden: The caller does not have permission
```

**Solution:**

- Verify that the service account has the `roles/aiplatform.user` role
- Check if Vertex AI API is enabled

#### 3. Project ID Error

```bash
❌ Project ID is not set
```

**Solution:**

- Set the `GOOGLE_CLOUD_PROJECT` environment variable
- Check the project ID in Claude Desktop configuration

## 📁 Project Structure

```bash
vertex-ai-imagen-mcp/
├── mcp_server.py              # Main MCP server
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore file
├── README.md                 # Korean version
├── README_EN.md              # This file (English version)
├── LICENSE                   # MIT License
├── claude_desktop_config.json # Claude Desktop configuration example
└── examples/                 # Usage examples
    └── basic_usage.py        # Basic usage example
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🔗 Related Links

- [vertex-ai-imagen package](https://github.com/realcoding2003/vertex-ai-imagen) - Core AI image generation library
- [Google Cloud Vertex AI](https://cloud.google.com/vertex-ai) - Official Vertex AI documentation
- [Model Context Protocol](https://modelcontextprotocol.io/) - Official MCP website
- [Claude Desktop](https://claude.ai/desktop) - Claude Desktop application

## ❓ Questions & Support

If you encounter any issues or have questions, please create an issue on [GitHub Issues](https://github.com/realcoding2003/vertex-ai-imagen-mcp/issues).

---

**Made with ❤️ by [Kevin Park](https://github.com/realcoding2003)**
