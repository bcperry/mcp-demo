# Welcome to the Minimal MCP Client using Azure OpenAI! 🚀🤖

Hi there, Developer! 👋 This project is a minimal implementation of an MCP (Model Context Protocol) client that leverages Azure OpenAI for the Large Language Model. It is designed to demonstrate how to integrate MCP with Azure OpenAI in a lightweight and efficient manner.

We can't wait to see what you create with this MCP client! Happy coding! 💻😊

## Running the Project

To run this project, use the following command:

```bash
chainlit run app.py --port 8001
```

This will start the Chainlit application on port 8001.

## Hosting the MCP Server

If you are hosting the MCP server, ensure it is added as an SSE (Server-Sent Events) server at the following URL:

```
http://localhost:8000/sse/
```

This setup is essential for the MCP client to communicate effectively with the server.
