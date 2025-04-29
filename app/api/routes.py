from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.db import get_db
from app.models.models import Itinerary, DailyPlan, Hotel, Activity, Transfer, Location
from app.api.schemas import (
    ItineraryCreate,
    ItineraryResponse,
    ErrorResponse,
    LocationResponse
)

router = APIRouter()


@router.post(
    "/itineraries/", 
    response_model=ItineraryResponse, 
    responses={400: {"model": ErrorResponse}}
)
async def create_itinerary(itinerary: ItineraryCreate, db: Session = Depends(get_db)):
    """
    Create a new travel itinerary with daily plans.
    
    Example request body:
    ```json
    {
      "name": "Phuket Paradise",
      "description": "Experience the best of Phuket beaches and attractions",
      "nights": 5,
      "daily_plans": [
        {
          "day_number": 1,
          "hotel_id": 1,
          "transfer_id": 3,
          "activity_ids": [1, 5],
          "notes": "Arrival day with beach time"
        },
        {
          "day_number": 2,
          "hotel_id": 1,
          "activity_ids": [2, 3],
          "notes": "Island hopping tour"
        }
      ]
    }
    ``` 
    """
    total_price = 0
    
    # Validate that all referenced IDs exist
    hotel_ids = set()
    transfer_ids = set()
    activity_ids = set()
    
    for plan in itinerary.daily_plans:
        hotel_ids.add(plan.hotel_id)
        if plan.transfer_id:
            transfer_ids.add(plan.transfer_id)
        activity_ids.update(plan.activity_ids)
    
    hotels = db.query(Hotel).filter(Hotel.id.in_(hotel_ids)).all()
    if len(hotels) != len(hotel_ids):
        raise HTTPException(status_code=400, detail="One or more hotel IDs not found")
    
    if transfer_ids:
        transfers = db.query(Transfer).filter(Transfer.id.in_(transfer_ids)).all()
        if len(transfers) != len(transfer_ids):
            raise HTTPException(status_code=400, detail="One or more transfer IDs not found")
    
    if activity_ids:
        activities = db.query(Activity).filter(Activity.id.in_(activity_ids)).all()
        if len(activities) != len(activity_ids):
            raise HTTPException(status_code=400, detail="One or more activity IDs not found")
    
    #New Itinerary instance
    db_itinerary = Itinerary(
        name=itinerary.name,
        description=itinerary.description,
        nights=itinerary.nights,
        total_price=0,  
    )
    db.add(db_itinerary)
    db.flush()  
    
    # Create DailyPlans
    for plan_data in itinerary.daily_plans:
        plan = DailyPlan(
            day_number=plan_data.day_number,
            itinerary_id=db_itinerary.id,
            hotel_id=plan_data.hotel_id,
            transfer_id=plan_data.transfer_id,
            notes=plan_data.notes
        )
        db.add(plan)
        db.flush()
        
        # Add activities
        if plan_data.activity_ids:
            activities = db.query(Activity).filter(Activity.id.in_(plan_data.activity_ids)).all()
            plan.activities = activities
            
        # Calculate costs
        hotel = db.query(Hotel).filter(Hotel.id == plan.hotel_id).first()
        total_price += hotel.price_per_night
        
        if plan.transfer_id:
            transfer = db.query(Transfer).filter(Transfer.id == plan.transfer_id).first()
            total_price += transfer.price
            
        for activity in plan.activities:
            total_price += activity.price
    
    # Update total price
    db_itinerary.total_price = total_price
    db.commit()
    db.refresh(db_itinerary)
    
    return db_itinerary


@router.get(
    "/itineraries/", 
    response_model=List[ItineraryResponse]
)
async def get_itineraries(
    nights: Optional[int] = None,
    recommended_only: bool = False,
    skip: int = 0, 
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Retrieve travel itineraries with optional filtering by number of nights.
    
    Parameters:
    - nights: Filter by the exact number of nights
    - recommended_only: If true, return only recommended itineraries
    - skip: Number of records to skip (for pagination)
    - limit: Maximum number of records to return
    
    Example response:
    ```json
    [
      {
        "id": 1,
        "name": "Phuket Paradise",
        "description": "Experience the best of Phuket beaches",
        "nights": 5,
        "total_price": 1250.5,
        "is_recommended": true,
        "daily_plans": [...]
      }
    ]
    ``` 
    """
    query = db.query(Itinerary)
    
    if nights is not None:
        query = query.filter(Itinerary.nights == nights)
    
    if recommended_only:
        query = query.filter(Itinerary.is_recommended == True)
        
    itineraries = query.offset(skip).limit(limit).all()
    return itineraries


@router.get(
    "/itineraries/{itinerary_id}", 
    response_model=ItineraryResponse,
    responses={404: {"model": ErrorResponse}}
)
async def get_itinerary(itinerary_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific itinerary by its ID.
    
    Parameters:
    - itinerary_id: The ID of the itinerary to retrieve
    """
    itinerary = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()
    if not itinerary:
        raise HTTPException(status_code=404, detail=f"Itinerary with ID {itinerary_id} not found")
    return itinerary


@router.get("/locations/", response_model=List[LocationResponse])
async def get_locations(region: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Retrieve locations with optional filtering by region.
    
    Parameters:
    - region: Filter locations by region (e.g., "Phuket" or "Krabi")
    """
    query = db.query(Location)
    
    if region:
        query = query.filter(Location.region == region)
        
    locations = query.all()
    return locations
