"""
Simple script to test the MCP server functionality.
Run this script after starting the MCP server with:
    python -m app.mcp.server
"""
import requests
import json
import sys

def test_mcp_basic():
    """Test basic MCP functionality using HTTP requests"""
    print("Testing MCP server via HTTP...")
    
    base_url = "http://localhost:8000/api/v1"
    
    # Test getting all itineraries
    try:
        print("\nFetching all itineraries...")
        response = requests.get(f"{base_url}/itineraries/")
        if response.status_code == 200:
            itineraries = response.json()
            print(f"Success! Found {len(itineraries)} itineraries")
            for i in itineraries[:2]:  # Show just the first 2
                print(f" - {i['name']} ({i['nights']} nights): ${i['total_price']}")
                
            # If we found any itineraries, test getting details of the first one
            if itineraries:
                itinerary_id = itineraries[0]['id']
                print(f"\nFetching details for itinerary {itinerary_id}...")
                response = requests.get(f"{base_url}/itineraries/{itinerary_id}")
                if response.status_code == 200:
                    itinerary = response.json()
                    print(f"Success! Details for '{itinerary['name']}':")
                    print(f" - Description: {itinerary['description']}")
                    print(f" - Number of daily plans: {len(itinerary['daily_plans'])}")
                else:
                    print(f"Error: Status code {response.status_code}")
                    print(response.text)
        else:
            print(f"Error: Status code {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error testing API: {e}")
    
    print("\nTest complete!")

if __name__ == "__main__":
    try:
        test_mcp_basic()
    except Exception as e:
        print(f"Test failed with error: {e}")
