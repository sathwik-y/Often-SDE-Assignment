from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from mcp.server.fastmcp import FastMCP, Context

from app.database.db import SessionLocal
from app.models.models import Itinerary
from config import MCP_SERVER_NAME


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[Dict[str, Any]]:
    """Initialize database connection for MCP server"""
    db = SessionLocal()
    try:
        yield {"db": db}
    finally:
        db.close()


# Create MCP server
mcp = FastMCP(
    MCP_SERVER_NAME,
    lifespan=app_lifespan,
    dependencies=["fastapi", "sqlalchemy"]
)


@mcp.tool()
def get_recommended_itinerary(nights: int, ctx: Context) -> dict:
    """
    Get a recommended itinerary for the specified number of nights.
    
    Args:
        nights: Number of nights for the trip (2-8)
    
    Returns:
        A recommended itinerary with daily plans.
    """
    if nights < 2 or nights > 8:
        return {"error": f"Nights must be between 2 and 8, got {nights}"}
    
    db: Session = ctx.request_context.lifespan_context["db"]
    
    # Find recommended itinerary with exact match for nights
    itinerary = db.query(Itinerary).filter(
        Itinerary.nights == nights,
        Itinerary.is_recommended == True
    ).first()
    
    if not itinerary:
        # If no exact match, try to find any recommended itinerary
        itinerary = db.query(Itinerary).filter(
            Itinerary.is_recommended == True
        ).first()
    
    if not itinerary:
        return {"error": "No recommended itineraries found"}
    
    # Format response
    result = {
        "id": itinerary.id,
        "name": itinerary.name,
        "description": itinerary.description,
        "nights": itinerary.nights,
        "total_price": itinerary.total_price,
        "daily_plans": []
    }
    
    # Add daily plans with details
    for plan in sorted(itinerary.daily_plans, key=lambda x: x.day_number):
        daily_plan = {
            "day": plan.day_number,
            "hotel": {
                "name": plan.hotel.name,
                "star_rating": plan.hotel.star_rating,
                "location": plan.hotel.location.name
            },
            "activities": [],
            "notes": plan.notes
        }
        
        # Add activities
        for activity in plan.activities:
            daily_plan["activities"].append({
                "name": activity.name,
                "duration": activity.duration,
                "type": activity.activity_type
            })
        
        # Add transfer if exists
        if plan.transfer:
            daily_plan["transfer"] = {
                "type": plan.transfer.transfer_type,
                "origin": plan.transfer.origin.name,
                "destination": plan.transfer.destination.name,
                "duration": plan.transfer.duration
            }
        
        result["daily_plans"].append(daily_plan)
    
    return result


@mcp.tool()
def list_available_durations(ctx: Context) -> List[int]:
    """
    List all available durations (nights) for recommended itineraries.
    
    Returns:
        A list of available night durations for recommended itineraries.
    """
    db: Session = ctx.request_context.lifespan_context["db"]
    
    # Query distinct night values for recommended itineraries
    nights = db.query(Itinerary.nights).filter(
        Itinerary.is_recommended == True
    ).distinct().all()
    
    return [n[0] for n in nights]


@mcp.resource("itineraries://recommended/{nights}")
def get_recommended_itinerary_resource(nights: str) -> str:
    """
    Get details about recommended itineraries for the specified number of nights.
    
    Args:
        nights: Number of nights for the itinerary
    
    Returns:
        A text description of recommended itineraries
    """
    try:
        nights_int = int(nights)
    except ValueError:
        return "Invalid input: nights must be a number between 2-8"
    
    if nights_int < 2 or nights_int > 8:
        return f"No recommended itineraries available for {nights_int} nights. Please choose between 2-8 nights."
    
    # Get the database session from a singleton or global instance
    db = SessionLocal()
    try:
        # Find recommended itineraries with the specified number of nights
        itineraries = db.query(Itinerary).filter(
            Itinerary.nights == nights_int,
            Itinerary.is_recommended == True
        ).all()
        
        if not itineraries:
            return f"No recommended itineraries found for {nights_int} nights."
        
        # Format response
        result = f"Found {len(itineraries)} recommended itineraries for {nights_int} nights:\n\n"
        
        for idx, itinerary in enumerate(itineraries, 1):
            result += f"Itinerary {idx}: {itinerary.name}\n"
            result += f"Description: {itinerary.description}\n"
            result += f"Total Price: ${itinerary.total_price:.2f}\n"
            result += f"Number of daily plans: {len(itinerary.daily_plans)}\n\n"
            
            for plan in sorted(itinerary.daily_plans, key=lambda x: x.day_number):
                result += f"Day {plan.day_number}:\n"
                result += f"  Stay at {plan.hotel.name} ({plan.hotel.star_rating} stars) in {plan.hotel.location.name}\n"
                
                if plan.transfer:
                    result += f"  Transfer: {plan.transfer.transfer_type} from {plan.transfer.origin.name} to {plan.transfer.destination.name} ({plan.transfer.duration} hours)\n"
                
                if plan.activities:
                    result += "  Activities:\n"
                    for activity in plan.activities:
                        result += f"    - {activity.name} ({activity.duration} hours)\n"
                
                if plan.notes:
                    result += f"  Notes: {plan.notes}\n"
                
                result += "\n"
        
        return result
    finally:
        db.close()


@mcp.prompt()
def recommend_itinerary(nights: int) -> str:
    """Create a prompt for recommending an itinerary for the specified number of nights"""
    return f"""Please recommend an itinerary for a {nights}-night trip to Thailand, focusing on the Phuket and Krabi regions.
    
Include suggestions for:
- Hotels to stay in 
- Activities and excursions
- Transfers between locations
- Approximate budget

Base your recommendations on realistic trip plans for Thailand, highlighting the best experiences while keeping a reasonable pace.
"""

# Add this code at the end of the file to make it runnable as a script
if __name__ == "__main__":
    print(f"Starting {MCP_SERVER_NAME}...")
    print("Press Ctrl+C to exit")
    mcp.run()
