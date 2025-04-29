"""
Script to clean up the database and start fresh
"""
import os
import sys

def clean_database():
    print("Cleaning up database...")
    
    # Path to the database file
    db_path = "./itinerary.db"
    
    # Check if file exists and remove it
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print(f"Database file {db_path} successfully removed.")
        except Exception as e:
            print(f"Error removing database file: {e}")
            return False
    else:
        print("No database file found. Nothing to clean.")
    
    return True

if __name__ == "__main__":
    if clean_database():
        print("Database cleaned successfully. Now you can reinitialize it.")
    else:
        print("Failed to clean database.")
