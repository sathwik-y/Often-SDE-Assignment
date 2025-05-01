import streamlit as st
import requests
import subprocess
import time
import os
import threading
import json
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Thailand Itinerary MCP Demo",
    page_icon="🏝️",
    layout="wide"
)

# Global variables
MCP_SERVER_PROCESS = None
API_SERVER_PROCESS = None
MCP_SERVER_RUNNING = False
API_SERVER_RUNNING = False
API_BASE_URL = "http://127.0.0.1:8000/api/v1"

def start_mcp_server():
    """Start the MCP server in a separate process"""
    global MCP_SERVER_PROCESS, MCP_SERVER_RUNNING
    if not MCP_SERVER_RUNNING:
        # Use Python executable from the current environment
        python_exe = Path(os.path.dirname(os.__file__)).parent / "python.exe"
        
        # Start the MCP server
        MCP_SERVER_PROCESS = subprocess.Popen(
            [str(python_exe), "-m", "app.mcp.server"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        MCP_SERVER_RUNNING = True
        st.toast("MCP Server started successfully!", icon="✅")
        return "MCP Server started successfully!"
    return "MCP Server is already running."

def start_api_server():
    """Start the FastAPI server in a separate process"""
    global API_SERVER_PROCESS, API_SERVER_RUNNING
    if not API_SERVER_RUNNING:
        # Use Python executable from the current environment
        python_exe = Path(os.path.dirname(os.__file__)).parent / "python.exe"
        
        # Start the API server
        API_SERVER_PROCESS = subprocess.Popen(
            [str(python_exe), "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        API_SERVER_RUNNING = True
        st.toast("API Server started successfully!", icon="✅")
        return "API Server started successfully!"
    return "API Server is already running."

def stop_servers():
    """Stop all running servers"""
    global MCP_SERVER_PROCESS, API_SERVER_PROCESS, MCP_SERVER_RUNNING, API_SERVER_RUNNING
    
    if MCP_SERVER_PROCESS:
        MCP_SERVER_PROCESS.terminate()
        MCP_SERVER_PROCESS = None
        MCP_SERVER_RUNNING = False
    
    if API_SERVER_PROCESS:
        API_SERVER_PROCESS.terminate()
        API_SERVER_PROCESS = None
        API_SERVER_RUNNING = False
    
    st.toast("All servers stopped", icon="🛑")
    return "All servers stopped."

def fetch_itineraries(nights=None, recommended_only=False):
    """Fetch itineraries from the API"""
    params = {}
    if nights:
        params["nights"] = nights
    if recommended_only:
        params["recommended_only"] = "true"
    
    try:
        response = requests.get(f"{API_BASE_URL}/itineraries/", params=params)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"Error fetching itineraries: {str(e)}")
        return None

def fetch_itinerary_details(itinerary_id):
    """Fetch details of a specific itinerary"""
    try:
        response = requests.get(f"{API_BASE_URL}/itineraries/{itinerary_id}")
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"Error fetching itinerary details: {str(e)}")
        return None

def simulate_mcp_request(nights):
    """Simulate an MCP request for a recommended itinerary"""
    try:
        # First, find itineraries with the specified number of nights
        params = {"nights": nights, "recommended_only": True}
        response = requests.get(f"{API_BASE_URL}/itineraries/", params=params)
        
        if response.status_code != 200 or not response.json():
            st.warning(f"No itineraries found for {nights} nights")
            return None
        
        # Get the ID of the first matching itinerary
        itinerary_id = response.json()[0]["id"]
        
        # Now fetch the complete details of this itinerary
        detail_response = requests.get(f"{API_BASE_URL}/itineraries/{itinerary_id}")
        
        if detail_response.status_code != 200:
            st.warning(f"Failed to get details for itinerary {itinerary_id}")
            return response.json()[0]  # Return basic info as fallback
        
        full_data = detail_response.json()
        
        # Debug information
        st.sidebar.info(f"Debug: Found {len(full_data.get('daily_plans', []))} daily plans")
        
        return full_data
    except Exception as e:
        st.error(f"Error with MCP request: {str(e)}")
        return None

# Main app UI
st.title("🏝️ Thailand Travel Itinerary MCP Demo")
st.write("This demo showcases the MCP server implementation for Thailand travel itineraries.")

# Sidebar controls
with st.sidebar:
    st.header("Server Controls")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start API Server", key="start_api", type="primary"):
            st.write(start_api_server())
    
    with col2:
        if st.button("Start MCP Server", key="start_mcp", type="primary"):
            st.write(start_mcp_server())
    
    if st.button("Stop All Servers", key="stop_servers", type="secondary"):
        st.write(stop_servers())
    
    st.divider()
    st.subheader("Demo Options")
    demo_nights = st.slider("Number of Nights", min_value=2, max_value=8, value=5, step=1)
    recommended_only = st.checkbox("Recommended Itineraries Only", value=True)

# Main content
tabs = st.tabs(["MCP Demo", "API Endpoints"])

# MCP Demo Tab
with tabs[0]:
    st.header("MCP Server Demo")
    st.write("Demonstrates the MCP server recommending itineraries based on number of nights.")
    
    if st.button("Get Recommended Itinerary", key="get_recommended", type="primary"):
        with st.spinner("Fetching recommended itinerary..."):
            itinerary = simulate_mcp_request(demo_nights)
            
            if itinerary:
                st.success(f"Found recommended {demo_nights}-night itinerary!")
                
                st.subheader(itinerary['name'])
                st.write(itinerary['description'])
                st.metric("Total Price", f"${itinerary['total_price']:.2f}")
                
                # Check and display the number of daily plans
                num_plans = len(itinerary.get('daily_plans', []))
                st.info(f"This itinerary includes {num_plans} daily plans")
                
                st.divider()
                st.subheader("Daily Plans")
                
                # If no daily plans, show a warning
                if not itinerary.get('daily_plans'):
                    st.warning("No daily plans found for this itinerary")
                    st.write("Please verify the database by running 'python verify_database.py'")
                
                for plan in sorted(itinerary.get('daily_plans', []), 
                                  key=lambda x: x.get('day_number', x.get('day', 0))):
                    day_num = plan.get('day_number', plan.get('day', 'Unknown'))
                    with st.expander(f"Day {day_num} - {plan.get('notes', 'No notes')}"):
                        if 'hotel' in plan and plan['hotel']:
                            st.write(f"**Hotel:** {plan['hotel']['name']} ({plan['hotel']['star_rating']} stars)")
                        else:
                            st.write("**Hotel information not available**")
                        
                        if 'transfer' in plan and plan['transfer']:
                            try:
                                origin = plan['transfer'].get('origin', {}).get('name', 'Unknown')
                                destination = plan['transfer'].get('destination', {}).get('name', 'Unknown')
                                st.write(f"**Transfer:** {plan['transfer'].get('transfer_type', 'Unknown')} from {origin} to {destination}")
                            except (KeyError, TypeError):
                                st.write(f"**Transfer:** {plan['transfer'].get('transfer_type', 'Available')}")
                        
                        if 'activities' in plan and plan['activities']:
                            st.write("**Activities:**")
                            for activity in plan['activities']:
                                st.write(f"- {activity['name']} ({activity.get('duration', 'Unknown')} hours)")
                        else:
                            st.write("**No scheduled activities**")
            else:
                st.error(f"No recommended itineraries found for {demo_nights} nights.")

# API Endpoints Tab
with tabs[1]:
    st.header("API Endpoints Documentation")
    st.write("Complete documentation of all available REST API endpoints.")
    
    # Create tabs for different endpoint categories
    api_tabs = st.tabs(["Itineraries", "Locations", "Testing"])
    
    # ITINERARIES ENDPOINTS
    with api_tabs[0]:
        st.subheader("Itinerary Endpoints")
        
        endpoints = [
            {
                "method": "GET",
                "path": "/api/v1/itineraries/",
                "description": "Get all itineraries with optional filtering",
                "params": "nights (optional), recommended_only (optional), skip (optional), limit (optional)",
                "example": "GET /api/v1/itineraries/?nights=5&recommended_only=true",
                "response_key": "List of itinerary objects with basic info"
            },
            {
                "method": "GET", 
                "path": "/api/v1/itineraries/{itinerary_id}",
                "description": "Get detailed information about a specific itinerary",
                "params": "itinerary_id (path parameter)",
                "example": "GET /api/v1/itineraries/1",
                "response_key": "Complete itinerary object with all daily plans"
            },
            {
                "method": "POST",
                "path": "/api/v1/itineraries/",
                "description": "Create a new itinerary",
                "params": "Request body with itinerary details",
                "example": "POST /api/v1/itineraries/ with JSON body",
                "response_key": "Created itinerary object"
            }
        ]
        
        for endpoint in endpoints:
            with st.expander(f"{endpoint['method']} {endpoint['path']}"):
                st.write(f"**Description:** {endpoint['description']}")
                st.write(f"**Parameters:** {endpoint['params']}")
                st.write(f"**Example Request:** `{endpoint['example']}`")
                st.write(f"**Response Type:** {endpoint['response_key']}")
                
                if endpoint['method'] == "GET" and "itinerary_id" not in endpoint['path']:
                    # Add button to test GET all itineraries
                    nights = st.number_input("Nights filter (optional)", min_value=0, max_value=10, value=0, key=f"nights_{endpoint['path']}")
                    recommended = st.checkbox("Recommended only", key=f"recommended_{endpoint['path']}")
                    if st.button("Try it", key=f"try_{endpoint['path']}"):
                        params = {}
                        if nights > 0:
                            params["nights"] = nights
                        if recommended:
                            params["recommended_only"] = "true"
                        
                        response = requests.get(f"{API_BASE_URL}/itineraries/", params=params)
                        if response.status_code == 200:
                            st.success(f"Success! Found {len(response.json())} itineraries")
                            st.json(response.json()[:2])  # Show first 2 for brevity
                            if len(response.json()) > 2:
                                st.caption("(Showing first 2 results)")
                        else:
                            st.error(f"Error: {response.status_code}")
                            st.text(response.text)
                
                elif endpoint['method'] == "GET" and "itinerary_id" in endpoint['path']:
                    # Add button to test GET single itinerary
                    itinerary_id = st.number_input("Itinerary ID", min_value=1, max_value=10, value=1, key=f"id_{endpoint['path']}")
                    if st.button("Try it", key=f"try_{endpoint['path']}"):
                        response = requests.get(f"{API_BASE_URL}/itineraries/{itinerary_id}")
                        if response.status_code == 200:
                            st.success(f"Success! Got details for itinerary {itinerary_id}")
                            with st.expander("View response"):
                                st.json(response.json())
                        else:
                            st.error(f"Error: {response.status_code}")
                            st.text(response.text)
    
    # LOCATIONS ENDPOINTS
    with api_tabs[1]:
        st.subheader("Location Endpoints")
        
        endpoints = [
            {
                "method": "GET",
                "path": "/api/v1/locations/",
                "description": "Get all locations with optional filtering by region",
                "params": "region (optional)",
                "example": "GET /api/v1/locations/?region=Phuket",
                "response_key": "List of location objects"
            }
        ]
        
        for endpoint in endpoints:
            with st.expander(f"{endpoint['method']} {endpoint['path']}"):
                st.write(f"**Description:** {endpoint['description']}")
                st.write(f"**Parameters:** {endpoint['params']}")
                st.write(f"**Example Request:** `{endpoint['example']}`")
                st.write(f"**Response Type:** {endpoint['response_key']}")
                
                # Add button to test GET locations
                region = st.radio("Region filter", ["All", "Phuket", "Krabi"], key=f"region_{endpoint['path']}")
                if st.button("Try it", key=f"try_{endpoint['path']}"):
                    params = {}
                    if region != "All":
                        params["region"] = region
                    
                    response = requests.get(f"{API_BASE_URL}/locations/", params=params)
                    if response.status_code == 200:
                        locations = response.json()
                        st.success(f"Success! Found {len(locations)} locations")
                        st.json(locations)
                    else:
                        st.error(f"Error: {response.status_code}")
                        st.text(response.text)
    
    # TESTING ENDPOINTS
    with api_tabs[2]:
        st.subheader("Testing Endpoints")
        st.write("These endpoints can be used for testing the API.")
        
        # Root endpoint
        with st.expander("GET /"):
            st.write("**Description:** Root endpoint that returns basic API info")
            st.write("**Parameters:** None")
            st.write("**Example Request:** `GET /`")
            
            if st.button("Try it", key="try_root"):
                response = requests.get("http://127.0.0.1:8000/")
                if response.status_code == 200:
                    st.success("Success!")
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
                    st.text(response.text)
        
        # Docs
        st.write("**API Documentation:**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Open Swagger UI", key="open_swagger"):
                st.markdown("[Swagger UI](http://127.0.0.1:8000/docs){target='_blank'}")
        with col2:
            if st.button("Open ReDoc", key="open_redoc"):
                st.markdown("[ReDoc](http://127.0.0.1:8000/redoc){target='_blank'}")

# Footer
st.divider()
st.caption("Thailand Travel Itinerary MCP Demo | Created for demonstration purposes")
