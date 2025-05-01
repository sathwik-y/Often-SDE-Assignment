"""
Claude MCP Integration for Thailand Itinerary System

This script demonstrates how to set up an MCP server that
Claude can connect to for retrieving itinerary data.

Instructions:
1. Make sure Claude Desktop is installed
2. Run this script
3. In Claude Desktop, connect to the MCP server at localhost:8080
"""
import asyncio
import json
import os
from typing import Dict, List, Optional

from app.database.db import SessionLocal
from app.models.models import Itinerary
from mcp.server.fastmcp import FastMCP, Context

# Create MCP server for Claude integration
claude_mcp = FastMCP(
    "ThailandItineraryClaudeServer",
    port=8080,  # Choose a port that doesn't conflict with your other services
)

@claude_mcp.tool()
def find_itineraries(nights: Optional[int] = None, ctx: Context = None) -> List[Dict]:
    """
    Find travel itineraries based on the number of nights.
    
    Args:
        nights: Optional number of nights to filter by (2-8)
    
    Returns:
        A list of matching itineraries with basic info
    """
    db = SessionLocal()
    try:
        query = db.query(Itinerary)
        
        if nights is not None:
            query = query.filter(Itinerary.nights == nights)
        
        # Limit to recommended itineraries
        query = query.filter(Itinerary.is_recommended == True)
        
        # Get basic info for each itinerary
        itineraries = []
        for item in query.all():
            itineraries.append({
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "nights": item.nights,
                "total_price": float(item.total_price),
            })
        
        return itineraries
    finally:
        db.close()

@claude_mcp.tool()
def get_itinerary_details(itinerary_id: int, ctx: Context = None) -> Dict:
    """
    Get detailed information about a specific itinerary.
    
    Args:
        itinerary_id: The ID of the itinerary to retrieve
    
    Returns:
        Detailed itinerary information including daily plans
    """
    db = SessionLocal()
    try:
        itinerary = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()
        
        if not itinerary:
            return {"error": f"Itinerary with ID {itinerary_id} not found"}
        
        # Format basic itinerary info
        result = {
            "id": itinerary.id,
            "name": itinerary.name,
            "description": itinerary.description,
            "nights": itinerary.nights,
            "total_price": float(itinerary.total_price),
            "daily_plans": []
        }
        
        # Add detailed daily plans
        for plan in sorted(itinerary.daily_plans, key=lambda x: x.day_number):
            daily_plan = {
                "day": plan.day_number,
                "notes": plan.notes,
                "hotel": {
                    "name": plan.hotel.name,
                    "star_rating": plan.hotel.star_rating,
                    "location": plan.hotel.location.name,
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
            
            # Add transfer if available
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

@claude_mcp.prompt()
def create_itinerary_recommendation(nights: int) -> str:
    """Create a prompt for generating an itinerary recommendation"""
    return f"""Please recommend a {nights}-night itinerary for Thailand focusing on Phuket and Krabi.
    
You can use the find_itineraries tool to find suitable itineraries, and the get_itinerary_details tool to get more information.

When presenting the itinerary to the user:
1. Start with an engaging overview of what makes this itinerary special
2. Organize the information by day, highlighting accommodations, activities, and transfers
3. Include estimated prices for transparency
4. Add your own insights about the locations and experiences

Remember to be conversational and enthusiastic about the beautiful destinations in Thailand!
"""

if __name__ == "__main__":
    print("Starting Claude MCP Server for Thailand Itineraries...")
    print("Connect Claude Desktop to localhost:8080")
    print("Press Ctrl+C to exit")
    
    try:
        # Run the MCP server
        claude_mcp.run()
    except KeyboardInterrupt:
        print("Claude MCP Server stopped.")
