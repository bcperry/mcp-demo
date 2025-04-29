from fastapi import FastAPI
from pydantic import Field
# import pyodbc, struct
# from azure import identity
from sse import create_sse_server
from mcp.server.fastmcp import FastMCP


# app = FastAPI()
mcp = FastMCP("AzureSQL")

from sqlite_db import SqliteDatabase
db = SqliteDatabase("test.db")
# def get_conn():
#     credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
#     token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
#     token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
#     SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
#     conn = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
#     return conn

# # Mount the Starlette SSE server onto the FastAPI app
# app.mount("/mcp/", create_sse_server(mcp), name="sse-mcp-server")


# @app.get("/")
# def read_root():
#     return {"MCP": "SQL", "description": "This is a simple SQL MCP server."}


@mcp.tool()
async def list_tables() -> str:
    """List all tables in the SQL database"""
    query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
    results = db._execute_query(query)
    return str(results)
@mcp.tool()
async def describe_table(table_name: str = Field(description="Name of the table to describe")) -> str:
    """Get the schema information for a specific table"""
    if table_name is None:
        raise ValueError("Missing table_name argument")
    results = db._execute_query(
        f"PRAGMA table_info({table_name})"
    )
    return str(results)

@mcp.tool()
async def create_table(query: str = Field(description="CREATE TABLE SQL statement")) -> str:
    """Create a table in the SQL database"""
    if not query.strip().upper().startswith("CREATE TABLE"):
        raise ValueError("Only CREATE TABLE statements are allowed")
    db._execute_query(query)
    return f"Table created successfully."

@mcp.tool()
async def write_query(query: str = Field(description="SQL query to execute")) -> str:
    """Execute an INSERT, UPDATE, or DELETE query on the SQL database"""
    if query.strip().upper().startswith("SELECT"):
        raise ValueError("SELECT queries are not allowed for write_query")
    results = db._execute_query(query)
    return str(results)

@mcp.tool()
async def read_query(query: str = Field(description="SELECT SQL query to execute")) -> str:
    """Execute a SELECT query on the SQL database"""
    if not query.strip().upper().startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed for read_query")
    results = db._execute_query(query)
    return str(results)

if __name__ == "__main__":
    mcp.run(transport="sse")