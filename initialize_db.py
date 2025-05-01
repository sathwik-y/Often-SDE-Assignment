from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import random

from app.database.db import Base, engine, SessionLocal
from app.models.models import (
    Location, Hotel, Activity, Transfer, Itinerary, DailyPlan
)
from config import DATABASE_URL
from app.seed.seed_data import main as seed_main  # Import the main function correctly


def clean_database():
    """Remove existing database file if it exists"""
    print("Cleaning up database...")
    
    # Path to the database file - extract from DATABASE_URL if it's sqlite
    if DATABASE_URL.startswith("sqlite:///"):
        db_path = DATABASE_URL[10:]  # Remove sqlite:/// prefix
        
        # Check if file exists and remove it
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
                print(f"Database file {db_path} successfully removed.")
            except Exception as e:
                print(f"Error removing database file: {e}")
                return False
        else:
            print("No database file found. Creating fresh database.")
    else:
        print("Not a SQLite database, skipping file removal.")
    
    return True


def initialize_db():
    """Initialize the database and seed with data"""
    # Check if database exists and remove it
    db_path = "./itinerary.db"
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print(f"Existing database file {db_path} removed.")
        except Exception as e:
            print(f"Error removing existing database: {e}")
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    
    # Seed the database by calling the main function that handles db session internally
    seed_main()
    
    # Verify the database content
    print("\nVerifying database content...")
    db = SessionLocal()
    try:
        # Check itineraries
        itineraries = db.query(Itinerary).all()
        print(f"Created {len(itineraries)} itineraries:")
        
        for i in itineraries:
            daily_plans = db.query(DailyPlan).filter(DailyPlan.itinerary_id == i.id).count()
            print(f"- {i.name}: {i.nights} nights, {daily_plans} daily plans, ${i.total_price:.2f}")
    finally:
        db.close()


if __name__ == "__main__":
    initialize_db()
    print("\nDatabase initialization complete. Run 'uvicorn app.main:app --reload' to start the API.")
