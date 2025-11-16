# Blaxel MCP Python

<p align="center">
  <img src="https://blaxel.ai/logo.png" alt="Blaxel" width="200"/>
</p>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-enabled-brightgreen.svg)](https://modelcontextprotocol.io/)
[![UV](https://img.shields.io/badge/UV-package_manager-blue.svg)](https://github.com/astral-sh/uv)

</div>

A template implementation of a Model Context Protocol (MCP) server in Python.
This template demonstrates how to build MCP-compatible servers that can be integrated with MCP-enabled clients for enhanced AI interactions and tool integrations.

## 📑 Table of Contents

- [Blaxel MCP Python](#blaxel-mcp-python)
  - [📑 Table of Contents](#-table-of-contents)
  - [✨ Features](#-features)
  - [🚀 Quick Start](#-quick-start)
  - [📋 Prerequisites](#-prerequisites)
  - [💻 Installation](#-installation)
  - [🔧 Usage](#-usage)
    - [Running the Server Locally](#running-the-server-locally)
    - [Testing your server](#testing-your-server)
    - [Deploying to Blaxel](#deploying-to-blaxel)
  - [📁 Project Structure](#-project-structure)
  - [❓ Troubleshooting](#-troubleshooting)
    - [Common Issues](#common-issues)
  - [👥 Contributing](#-contributing)
  - [🆘 Support](#-support)
  - [📄 License](#-license)

## ✨ Features

- Model Context Protocol (MCP) server implementation
- Compatible with MCP-enabled clients and applications
- Tool registration and execution capabilities
- Resource management and context sharing
- Built with Python 3.12+ for modern language features
- Easy debugging with MCP Inspector
- Easy deployment and integration with Blaxel platform

## 🚀 Quick Start

For those who want to get up and running quickly:

```bash
# Clone the repository
git clone https://github.com/blaxel-ai/template-mcp-py.git

# Navigate to the project directory
cd template-mcp-py

# Install dependencies
uv sync

# Start the MCP server locally
bl serve --hotreload

# In another terminal, test with MCP Inspector
npx @modelcontextprotocol/inspector --transport http --server-url http://localhost:1338/mcp
```

## 📋 Prerequisites

- **Python:** 3.12 or later
- **[UV](https://github.com/astral-sh/uv):** An extremely fast Python package and project manager, written in Rust
- **Node.js** (Optional): 20.11.0 or later for hot reload features
- **Blaxel Platform Setup:** Complete Blaxel setup by following the [quickstart guide](https://docs.blaxel.ai/Get-started#quickstart)
  - **[Blaxel CLI](https://docs.blaxel.ai/Get-started):** Ensure you have the Blaxel CLI installed. If not, install it globally:
    ```bash
    curl -fsSL https://raw.githubusercontent.com/blaxel-ai/toolkit/main/install.sh | BINDIR=/usr/local/bin sudo -E sh
    ```
  - **Blaxel login:** Login to Blaxel platform
    ```bash
    bl login YOUR-WORKSPACE
    ```

## 💻 Installation

**Clone the repository and install dependencies:**

```bash
git clone https://github.com/blaxel-ai/template-mcp-py.git
cd template-mcp-py
uv sync
```

## 🔧 Usage

### Running the Server Locally

Start the development server with hot reloading:

```bash
bl serve --hotreload
```

_Note:_ This command starts the server and enables hot reload so that changes to the source code are automatically reflected.

### Testing your server

You can test your MCP server using the MCP Inspector for debugging:

```bash
npx @modelcontextprotocol/inspector --transport http --server-url http://localhost:1338/mcp
```

This launches the MCP Inspector UI which helps debug server functionality through a web interface.
You can connect to your MCP and test your Tools/Resources/Prompt

### Deploying to Blaxel

When you are ready to deploy your application:

```bash
bl deploy
```

This command uses your code and the configuration files under the `.blaxel` directory to deploy your application.

## 📁 Project Structure

- **src/server.py** - Main MCP server implementation
- **src/tools/** - Tool definitions and implementations
- **src/resources/** - Resource handlers and content
- **src/prompts/** - Prompt templates and management
- **pyproject.toml** - UV package manager configuration
- **blaxel.toml** - Blaxel deployment configuration

## ❓ Troubleshooting

### Common Issues

1. **Blaxel Platform Issues**:
   - Ensure you're logged in to your workspace: `bl login MY-WORKSPACE`
   - Verify models are available: `bl get models`
   - Check that functions exist: `bl get functions`

2. **MCP Protocol Errors**:
   - Check MCP client compatibility version
   - Verify message format compliance
   - Review server startup logs for initialization errors

3. **Tool Registration Problems**:
   - Ensure tool schemas are properly defined
   - Check tool argument validation
   - Verify tool decorators are correctly applied

4. **Connection Issues**:
   - Verify server is running on expected transport
   - Check stdio/socket configuration
   - Review client connection parameters

5. **Debugging with MCP Inspector**:
   - Ensure `BL_DEBUG=true` environment variable is set
   - Check that Node.js is installed for Inspector UI
   - Verify no port conflicts on Inspector interface

For more help, please [submit an issue](https://github.com/blaxel-templates/template-mcp-py/issues) on GitHub.

## 👥 Contributing

Contributions are welcome! Here's how you can contribute:

1. **Fork** the repository
2. **Create** a feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit** your changes:
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push** to the branch:
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Submit** a Pull Request

Please make sure to update tests as appropriate and follow the MCP protocol standards.

## 🆘 Support

If you need help with this template:

- [Submit an issue](https://github.com/blaxel-templates/template-mcp-py/issues) for bug reports or feature requests
- Visit the [Blaxel Documentation](https://docs.blaxel.ai) for platform guidance
- Check the [Model Context Protocol Documentation](https://modelcontextprotocol.io/) for protocol specifications
- Join our [Discord Community](https://discord.gg/G3NqzUPcHP) for real-time assistance

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
