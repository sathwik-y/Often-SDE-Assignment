"""
Test script for the Thailand Itinerary MCP server.
This script demonstrates how to connect to and interact with the MCP server.
"""
import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_mcp_server():
    """Test the MCP server functionality."""
    print("Testing MCP server for Thailand Itineraries...")
    
    # Create server parameters for subprocess connection
    server_params = StdioServerParameters(
        command=sys.executable,  # Use the current Python interpreter
        args=["-m", "app.mcp.server"],  # Run the MCP server module
        env=None,  # Use current environment variables
    )
    
    print("Connecting to MCP server...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            print("Initializing MCP session...")
            await session.initialize()
            
            print("\n===== Testing available durations =====")
            # Test the list_available_durations tool
            try:
                durations = await session.call_tool("list_available_durations")
                print(f"Available durations: {durations}")
            except Exception as e:
                print(f"Error listing durations: {e}")
            
            print("\n===== Testing itinerary recommendation =====")
            # Test the get_recommended_itinerary tool with different night values
            for nights in [3, 5, 7]:
                try:
                    print(f"\nGetting recommended itinerary for {nights} nights:")
                    itinerary = await session.call_tool("get_recommended_itinerary", arguments={"nights": nights})
                    print(f"Recommended itinerary: {itinerary['name']}")
                    print(f"Description: {itinerary['description']}")
                    print(f"Total price: ${itinerary['total_price']}")
                    print(f"Number of daily plans: {len(itinerary['daily_plans'])}")
                except Exception as e:
                    print(f"Error getting itinerary for {nights} nights: {e}")
            
            print("\n===== Testing resource access =====")
            # Test the itinerary resource
            for nights in [3, 5]:
                try:
                    print(f"\nAccessing details for {nights}-night itineraries:")
                    content, mime_type = await session.read_resource(f"itineraries://recommended/{nights}")
                    print(f"Content type: {mime_type}")
                    # Print just the first few lines to avoid overwhelming output
                    content_preview = "\n".join(content.split("\n")[:10]) + "\n..."
                    print(f"Content preview:\n{content_preview}")
                except Exception as e:
                    print(f"Error accessing resource for {nights} nights: {e}")
            
            print("\n===== Testing itinerary prompt =====")
            # Test the recommend_itinerary prompt
            try:
                nights = 4
                print(f"Getting prompt for {nights}-night recommendation:")
                prompt = await session.get_prompt("recommend_itinerary", arguments={"nights": nights})
                print(f"Prompt messages: {prompt.messages}")
            except Exception as e:
                print(f"Error getting prompt: {e}")


def main():
    """Run the MCP server tests."""
    try:
        asyncio.run(test_mcp_server())
        print("\nMCP server test completed successfully!")
    except Exception as e:
        print(f"\nError testing MCP server: {e}")


if __name__ == "__main__":
    main()
