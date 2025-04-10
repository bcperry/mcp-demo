# MCP Demo Repository

This repository contains a demonstration of a minimal MCP (Model Context Protocol) client and server setup. The client leverages Azure OpenAI, while the server provides an SSE (Server-Sent Events) interface for communication.

## Repository Structure

```
mcp_client_aoai/
    app.py                # The main application file for the MCP client
    chainlit.md           # Documentation for running the MCP client
    README.md             # Additional documentation for the client
    requirements.txt      # Python dependencies for the client

mcp_sse_server/
    app.py                # The main application file for the MCP server
    requirements.txt      # Python dependencies for the server
    sse.py                # SSE implementation for the server
```

## Running the MCP Client

The MCP client is located in the `mcp_client_aoai` directory. To run the client, use the following command:

```bash
chainlit run app.py -p 8001
```

This will start the Chainlit application on port 8001. Ensure that the required dependencies are installed by running:

```bash
pip install -r mcp_client_aoai/requirements.txt
```

## Running the MCP Server

The MCP server is located in the `mcp_sse_server` directory. To run the server, use the following command:

```bash
python mcp_sse_server/app.py
```

The server will be hosted at `http://localhost:8000/sse/`. Ensure that the required dependencies are installed by running:

```bash
pip install -r mcp_sse_server/requirements.txt
```

## Creating an .env File

To configure the environment variables for this project, create a `.env` file in the root directory of the respective client or server folder. Use the provided `.env.example` file as a template. The `.env` file should contain the necessary environment variables required for the application to run.

For example:

```
AZURE_OPENAI_ENDPOINT="your_endpoint_here"
AZURE_OPENAI_API_KEY="your_api_key_here"
AZURE_OPENAI_MODEL="model_deployment_name_here"
OPENAI_API_VERSION=2024-02-15-preview
```

## Notes

- The MCP client communicates with the server via the SSE endpoint at `http://localhost:8000/sse/`.
- Make sure both the client and server are running simultaneously for proper functionality.

This repository serves as a minimal example to demonstrate the integration of MCP with Azure OpenAI and SSE communication.