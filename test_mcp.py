import asyncio
from mcp.client import MCPClient
from app.mcp.server import mcp

async def test_mcp_server():
    # Start the server
    print("Starting MCP server...")
    server_task = asyncio.create_task(mcp.run())
    
    # Allow time for server to start
    await asyncio.sleep(2)
    
    # Create client
    print("Creating MCP client...")
    client = MCPClient()
    
    # Test get_recommended_itinerary
    print("\nTesting get_recommended_itinerary...")
    for nights in range(2, 9):
        result = await client.call_tool("get_recommended_itinerary", {"nights": nights})
        print(f"Result for {nights} nights: {'Success' if 'id' in result else 'Failed'}")
    
    # Test list_available_durations
    print("\nTesting list_available_durations...")
    durations = await client.call_tool("list_available_durations", {})
    print(f"Available durations: {durations}")
    
    # Test resources
    print("\nTesting itineraries resource...")
    for nights in range(2, 9):
        resource = await client.get_resource(f"itineraries://recommended/{nights}")
        print(f"Resource for {nights} nights: {'Success' if len(resource) > 100 else 'Failed'}")
    
    # Clean up
    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        pass
    
    print("\nMCP tests completed!")

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
