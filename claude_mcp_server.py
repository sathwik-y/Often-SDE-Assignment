"""MCP Server for Claude Desktop integration with Thailand Travel Itinerary system"""
from typing import Dict, List, Optional
import json
import sys
import os

print(f"Starting MCP server with Python: {sys.executable}", file=sys.stderr)
print(f"Current working directory: {os.getcwd()}", file=sys.stderr)

try:
    from mcp.server.fastmcp import FastMCP
    print("MCP module imported successfully", file=sys.stderr)
except ImportError as e:
    print(f"Error importing MCP: {e}", file=sys.stderr)
    sys.exit(1)

DB_PATH = os.path.join("D:\\Grind\\Itenary", "itinerary.db")
print(f"Using absolute database path: {DB_PATH}", file=sys.stderr)

from app.database.db import engine, Base
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

abs_engine = create_engine(f"sqlite:///{DB_PATH}")

CustomSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=abs_engine)

from app.models.models import Itinerary, Location, Hotel, Activity, Transfer

try:
    inspector = sqlalchemy.inspect(abs_engine)
    tables = inspector.get_table_names()
    print(f"Tables in database: {tables}", file=sys.stderr)
    
    session = CustomSessionLocal()
    try:
        location_count = session.query(Location).count()
        print(f"Location count: {location_count}", file=sys.stderr)
        
        itinerary_count = session.query(Itinerary).count()
        print(f"Itinerary count: {itinerary_count}", file=sys.stderr)
        
        if itinerary_count > 0:
            sample = session.query(Itinerary).first()
            print(f"Sample itinerary: {sample.name} - {sample.nights} nights", file=sys.stderr)
    finally:
        session.close()
except Exception as e:
    print(f"Database error: {e}", file=sys.stderr)

mcp = FastMCP(name="ThailandItineraryServer")

@mcp.tool()
def find_itineraries(nights: Optional[int] = None) -> List[Dict]:
    """
    Find available travel itineraries based on number of nights.
    
    Args:
        nights: Optional number of nights to filter by (2-8)
    
    Returns:
        A list of matching itineraries with details
    """
    db = CustomSessionLocal()
    try:
        print(f"Searching for itineraries with nights={nights}", file=sys.stderr)
        query = db.query(Itinerary)
        
        if nights is not None:
            query = query.filter(Itinerary.nights == nights)
            print(f"Added filter: nights={nights}", file=sys.stderr)
        
        query = query.filter(Itinerary.is_recommended == True)
        print(f"Added filter: is_recommended=True", file=sys.stderr)
        
        print(f"SQL Query: {query.statement}", file=sys.stderr)
        
        items = query.all()
        print(f"Query returned {len(items)} results", file=sys.stderr)
        
        result = []
        for item in items:
            result.append({
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "nights": item.nights,
                "total_price": float(item.total_price),
                "num_daily_plans": len(item.daily_plans)
            })
        
        return result
    finally:
        db.close()

@mcp.tool()
def get_itinerary_details(itinerary_id: int) -> Dict:
    """
    Get detailed information about a specific itinerary.
    
    Args:
        itinerary_id: The ID of the itinerary to retrieve
    
    Returns:
        Detailed itinerary information including daily plans
    """
    # Use our custom session with absolute DB path
    db = CustomSessionLocal()
    try:
        print(f"Getting details for itinerary_id={itinerary_id}", file=sys.stderr)
        itinerary = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()
        
        if not itinerary:
            print(f"Itinerary with ID {itinerary_id} not found", file=sys.stderr)
            return {"error": f"Itinerary with ID {itinerary_id} not found"}
        
        print(f"Found itinerary: {itinerary.name}", file=sys.stderr)
        # Format the full itinerary with daily plans
        result = {
            "id": itinerary.id,
            "name": itinerary.name,
            "description": itinerary.description,
            "nights": itinerary.nights,
            "total_price": float(itinerary.total_price),
            "daily_plans": []
        }
        
        # Add daily plans sorted by day number
        for plan in sorted(itinerary.daily_plans, key=lambda x: x.day_number):
            daily_plan = {
                "day": plan.day_number,
                "notes": plan.notes,
                "hotel": {
                    "name": plan.hotel.name,
                    "location": plan.hotel.location.name,
                    "star_rating": plan.hotel.star_rating,
                    "price_per_night": float(plan.hotel.price_per_night)
                },
                "activities": []
            }
            
            # Add activities
            for activity in plan.activities:
                daily_plan["activities"].append({
                    "name": activity.name,
                    "duration": activity.duration,
                    "price": float(activity.price),
                    "type": activity.activity_type
                })
            
            # Add transfer if present
            if plan.transfer:
                daily_plan["transfer"] = {
                    "type": plan.transfer.transfer_type,
                    "origin": plan.transfer.origin.name,
                    "destination": plan.transfer.destination.name,
                    "duration": plan.transfer.duration,
                    "price": float(plan.transfer.price)
                }
            
            result["daily_plans"].append(daily_plan)
        
        return result
    finally:
        db.close()

@mcp.tool()
def get_available_locations() -> List[Dict]:
    """
    Get list of all available locations in Thailand.
    
    Returns:
        List of locations with region information
    """
    # Use our custom session with absolute DB path
    db = CustomSessionLocal()
    try:
        print("Getting available locations", file=sys.stderr)
        locations = db.query(Location).all()
        print(f"Found {len(locations)} locations", file=sys.stderr)
        
        if locations:
            for loc in locations[:3]:  # Print first 3 as sample
                print(f"Sample location: {loc.name} ({loc.region})", file=sys.stderr)
        
        return [
            {
                "id": loc.id,
                "name": loc.name,
                "region": loc.region,
                "description": loc.description
            }
            for loc in locations
        ]
    finally:
        db.close()

@mcp.prompt()
def recommend_thai_itinerary(nights: int, interests: str = "beaches, culture, food") -> str:
    """
    Create a prompt for recommending an itinerary based on interests.
    
    Args:
        nights: Number of nights for the trip (2-8)
        interests: Comma-separated list of travel interests
    """
    return f"""Please help me plan a {nights}-night trip to Thailand focusing on Phuket and Krabi regions.

My interests include: {interests}

I'd like recommendations on:
- Which itinerary would be best for me
- What activities I should prioritize
- Where I should stay
- How to get around
- Approximate budget

You can use the find_itineraries, get_itinerary_details, and get_available_locations tools to help create a personalized recommendation.

Please organize the response with clear headings and include specific details about accommodations, activities, and transfers.
"""

if __name__ == "__main__":
    print("Starting Claude Desktop MCP Server for Thailand Itinerary...")
    print("This server provides tools for Claude to access itinerary information.")
    print("Waiting for Claude Desktop to connect...")
    mcp.run()
