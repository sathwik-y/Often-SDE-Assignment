# Integrating with Claude Desktop - Step by Step Guide

## Prerequisites

1. Install Claude Desktop from [Anthropic's website](https://www.anthropic.com/claude)
2. Ensure your Thailand Travel Itinerary system is fully set up and working
3. Make sure you have the MCP package installed: `pip install mcp`

## Step 1: Build the MCP Server File

We've created a dedicated MCP server file `claude_mcp_server.py` that provides tools for accessing your itinerary database.

## Step 2: Configure Claude Desktop (Windows)

Claude Desktop needs a configuration file to know about your MCP server:

1. Open or create the Claude Desktop configuration file:
   ```ivate your virtual environment:
   %AppData%\Claude\claude_desktop_config.json
   ```Grind\Itenary\venv\Scripts\activate
   You can use Notepad or VS Code to edit this file.
3. Run the database initialization script:
2. Add your Thailand Itinerary MCP server configuration:
   ```jsoninitialize_db.py
   {``
       "mcpServers": { was created successfully:
           "thailand-itinerary": {
               "command": "python",
               "args": [
                   "D:\\Grind\\Itenary\\claude_mcp_server.py"
               ] SQLite database with all necessary tables and seed data that the MCP server requires.
           }
       }3: Configure Claude Desktop (Windows)
   }
   ``` Desktop needs a configuration file to know about your MCP server:

   Make sure to use the correct absolute path to your MCP server file.
   ```
## Step 3: Restart Claude Desktopp_config.json
   ```
After saving the configuration file, completely close and restart Claude Desktop to load the new MCP server configuration.

## Step 4: Use the MCP Tools in Claudever configuration:
   ```json
1. Start a new conversation in Claude Desktop
2. Look for the hammer icon (🔨) in the bottom input area - this indicates MCP tools are available
3. Ask Claude questions about Thailand travel itineraries, such as:
   - "Can you recommend a 5-night itinerary for Thailand?"
   - "What are the available locations in Thailand's Phuket region?"
   - "Show me details of itineraries for Krabi"mcp_server.py"
               ]
Claude will use your MCP server to retrieve information from your database and provide responses based on your actual travel data.
       }
## Troubleshooting
   ```
If you encounter issues:
   Make sure to use the correct absolute path to your MCP server file.
1. **MCP icon not showing up**:
   - Check your `claude_desktop_config.json` for syntax errors
   - Ensure paths are absolute and use double backslashes in Windows paths
   - Make sure Claude Desktop is completely restarted and restart Claude Desktop to load the new MCP server configuration.

2. **Server connection issues**:Claude
   - Check Claude's log files in `%AppData%\Roaming\Claude\logs\` for errors
   - Look for files named `mcp-server-thailand-itinerary.log` for server-specific errors
2. Look for the hammer icon (🔨) in the bottom input area - this indicates MCP tools are available
3. **"No module named 'mcp'" error**:d travel itineraries, such as:
   - This means the Python environment that Claude Desktop is using can't find the MCP package
   - Update your `claude_desktop_config.json` to use the full path to the Python interpreter in your virtual environment:
     ```jsone details of itineraries for Krabi"
     {
         "mcpServers": { server to retrieve information from your database and provide responses based on your actual travel data.
             "thailand-itinerary": {
                 "command": "D:\\Grind\\Itenary\\venv\\Scripts\\python.exe",
                 "args": [
                     "D:\\Grind\\Itenary\\claude_mcp_server.py"
                 ]
             }not showing up**:
         } your `claude_desktop_config.json` for syntax errors
     }nsure paths are absolute and use double backslashes in Windows paths
     ```e sure Claude Desktop is completely restarted

4. **"No such table" database errors**:
   - This error occurs when the database hasn't been initializedClaude\logs\` for errors
   - Follow these steps to fix:y.log` for server-specific errors
     1. Open a terminal and navigate to your project directory
     2. Activate the virtual environment: `venv\Scripts\activate`3. **"No module named 'mcp'" error**:









   - Run `python verify_database.py` to check your database integrity   - Verify the database path in your config is correct   - Make sure your database is properly initialized5. **Database connection errors**:   - Make sure the database path in `claude_mcp_server.py` is correct and matches the path in your config     4. Verify with: `python verify_database.py`     3. Run: `python initialize_db.py`   - This means the Python environment that Claude Desktop is using can't find the MCP package
   - Update your `claude_desktop_config.json` to use the full path to the Python interpreter in your virtual environment:
     ```json
     {
         "mcpServers": {
             "thailand-itinerary": {
                 "command": "D:\\Grind\\Itenary\\venv\\Scripts\\python.exe",
                 "args": [
                     "D:\\Grind\\Itenary\\claude_mcp_server.py"
                 ]
             }
         }
     }
     ```

4. **Database connection errors**:
   - Make sure your database is properly initialized
   - Verify the database path in your config is correct
   - Run `python verify_database.py` to check your database integrity
