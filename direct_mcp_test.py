"""
Direct test of MCP server functionality without using the MCP client library.
Run this script with the MCP server running in another terminal:
    python -m app.mcp.server
"""
import subprocess
import sys
import time
import json

def test_mcp_direct():
    """Test MCP server by directly spawning it as a subprocess"""
    print("Testing MCP server directly...")
    
    # Start the MCP server as a subprocess
    print("Starting MCP server...")
    mcp_process = subprocess.Popen(
        [sys.executable, "-m", "app.mcp.server"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        text=True
    )
    
    try:
        # Give the server time to start
        print("Waiting for server to initialize...")
        time.sleep(2)
        
        # Send an initialization request
        print("Sending initialization request...")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "capabilities": {}
            }
        }
        mcp_process.stdin.write(json.dumps(init_request) + "\n")
        mcp_process.stdin.flush()
        
        # Read the response
        print("Reading response...")
        response_line = mcp_process.stdout.readline()
        try:
            response = json.loads(response_line)
            print("Server initialized successfully!")
            print(f"Server name: {response.get('result', {}).get('serverInfo', {}).get('name')}")
            print(f"Server version: {response.get('result', {}).get('serverInfo', {}).get('version')}")
        except json.JSONDecodeError:
            print(f"Failed to parse response: {response_line}")
        
        # Send a request to list tools
        print("\nSending request to list tools...")
        list_tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "listTools",
            "params": {}
        }
        mcp_process.stdin.write(json.dumps(list_tools_request) + "\n")
        mcp_process.stdin.flush()
        
        # Read the response
        print("Reading response...")
        response_line = mcp_process.stdout.readline()
        try:
            response = json.loads(response_line)
            tools = response.get('result', [])
            print(f"Found {len(tools)} tools:")
            for tool in tools:
                print(f" - {tool.get('name')}: {tool.get('description')}")
        except json.JSONDecodeError:
            print(f"Failed to parse response: {response_line}")
        
    finally:
        # Clean up
        print("\nShutting down MCP server...")
        mcp_process.terminate()
        try:
            mcp_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            mcp_process.kill()

if __name__ == "__main__":
    try:
        test_mcp_direct()
    except Exception as e:
        print(f"Test failed with error: {e}")
