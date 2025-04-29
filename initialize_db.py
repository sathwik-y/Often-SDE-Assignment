from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import random

from app.database.db import Base
from app.models.models import (
    Location, Hotel, Activity, Transfer, Itinerary, DailyPlan
)
from config import DATABASE_URL


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


def initialize_database():
    """Initialize database with schema and seed data"""
    print("Creating database engine...")
    engine = create_engine(DATABASE_URL)
    
    print("Creating database tables...")
    Base.metadata.create_all(engine)
    
    print("Creating session...")
    Session = sessionmaker(bind=engine)
    db = Session()
    
    try:
        print("Seeding database with travel data...")
        # Seed locations
        print("Adding locations...")
        locations = seed_locations(db)
        
        # Seed hotels
        print("Adding hotels...")
        hotels = seed_hotels(db, locations)
        
        # Seed activities
        print("Adding activities...")
        activities = seed_activities(db, locations)
        
        # Seed transfers
        print("Adding transfers...")
        transfers = seed_transfers(db, locations)
        
        # Create itineraries
        print("Creating itineraries with daily plans...")
        itineraries = create_itineraries_with_plans(db, hotels, activities, transfers)
        
        # Create additional itineraries for remaining night durations
        print("Creating additional itineraries for all durations...")
        add_remaining_night_durations(db, itineraries, hotels, activities, transfers)
        
        print("Database seeding completed successfully!")
        return True
    
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        return False
    
    finally:
        db.close()


def seed_locations(db):
    """Seed location data for Phuket and Krabi regions"""
    locations = [
        Location(
            name="Patong Beach",
            region="Phuket",
            description="Phuket's most famous beach resort area, with a wide sandy beach and vibrant nightlife",
            latitude=7.8949,
            longitude=98.2963
        ),
        Location(
            name="Karon Beach",
            region="Phuket",
            description="A long stretch of white sand with crystal clear water, less crowded than Patong",
            latitude=7.8429,
            longitude=98.2946
        ),
        Location(
            name="Kata Beach",
            region="Phuket",
            description="A scenic bay with palm trees and soft white sand, popular with families",
            latitude=7.8206,
            longitude=98.2959
        ),
        Location(
            name="Phuket Town",
            region="Phuket",
            description="The capital of Phuket province with Sino-Portuguese architecture and local markets",
            latitude=7.8804,
            longitude=98.3923
        ),
        Location(
            name="Phi Phi Islands",
            region="Phuket",
            description="A group of stunning islands with limestone cliffs, clear waters and white sand beaches",
            latitude=7.7407,
            longitude=98.7784
        ),
        Location(
            name="Ao Nang",
            region="Krabi",
            description="A central beach town in Krabi with shops, restaurants, and access to nearby islands",
            latitude=8.0329,
            longitude=98.8268
        ),
        Location(
            name="Railay Beach",
            region="Krabi",
            description="A stunning peninsula accessible only by boat, famous for rock climbing and beautiful beaches",
            latitude=8.0055,
            longitude=98.8371
        ),
        Location(
            name="Koh Lanta",
            region="Krabi",
            description="A relaxed island with long beaches and a laid-back atmosphere",
            latitude=7.6521,
            longitude=99.0409
        ),
        Location(
            name="Krabi Town",
            region="Krabi",
            description="The main town in Krabi province with markets, temples and authentic Thai culture",
            latitude=8.0863,
            longitude=98.9063
        ),
    ]
    
    db.add_all(locations)
    db.commit()
    
    return locations


def seed_hotels(db, locations):
    """Seed hotel data for locations"""
    hotels = [
        Hotel(
            name="Patong Resort Hotel",
            description="Comfortable resort close to Patong's beach and nightlife",
            star_rating=4.0,
            location_id=1,  # Patong Beach
            address="208 Rat-Uthit 200 Pi Road, Patong, Kathu, Phuket",
            price_per_night=85.0,
            amenities="Swimming pool, Restaurant, Free WiFi, Spa, Fitness center",
            image_url="https://example.com/patong_resort.jpg"
        ),
        Hotel(
            name="Karon Sea Sands Resort & Spa",
            description="Relaxing resort just steps from Karon Beach",
            star_rating=4.0,
            location_id=2,  # Karon Beach
            address="24 Soi Karon Soi 2, Karon, Muang, Phuket",
            price_per_night=90.0,
            amenities="Swimming pool, Spa, Restaurant, Free WiFi, Tour desk",
            image_url="https://example.com/karon_sea_sands.jpg"
        ),
        Hotel(
            name="Kata Palm Resort & Spa",
            description="Tropical resort with large pools and easy beach access",
            star_rating=4.0,
            location_id=3,  # Kata Beach
            address="60 Kata Road, Kata Beach, Phuket",
            price_per_night=95.0,
            amenities="Swimming pools, Spa, 2 Restaurants, Pool bar, Free WiFi",
            image_url="https://example.com/kata_palm.jpg"
        ),
        Hotel(
            name="The Memory at On On Hotel",
            description="Historic Sino-Portuguese building in Phuket Old Town",
            star_rating=3.0,
            location_id=4,  # Phuket Town
            address="19 Phang Nga Road, Phuket Town",
            price_per_night=45.0,
            amenities="Free WiFi, 24-hour front desk, Tour desk",
            image_url="https://example.com/on_on_hotel.jpg"
        ),
        Hotel(
            name="Phi Phi Island Village Beach Resort",
            description="Luxury beachfront resort with bungalows on Phi Phi Island",
            star_rating=4.5,
            location_id=5,  # Phi Phi Islands
            address="49 Moo 8, Aonang, Muang, Krabi",
            price_per_night=210.0,
            amenities="Private beach, Infinity pool, Dive center, Spa, Multiple restaurants",
            image_url="https://example.com/phi_phi_village.jpg"
        ),
        Hotel(
            name="Aonang Cliff Beach Resort",
            description="Hillside resort with stunning views over Ao Nang Bay",
            star_rating=4.0,
            location_id=6,  # Ao Nang
            address="328 Moo 2, Ao Nang, Muang, Krabi",
            price_per_night=120.0,
            amenities="Infinity pools, Rooftop bar, Spa, Fitness center, Restaurants",
            image_url="https://example.com/aonang_cliff.jpg"
        ),
        Hotel(
            name="Rayavadee",
            description="Luxury resort set amidst tropical gardens surrounded by beaches",
            star_rating=5.0,
            location_id=7,  # Railay Beach
            address="214 Moo 2, Tambon Ao-Nang, Muang, Krabi",
            price_per_night=450.0,
            amenities="Multiple restaurants, Spa, Private beach areas, Free activities, Pavilion-style villas",
            image_url="https://example.com/rayavadee.jpg"
        ),
        Hotel(
            name="Lanta Sand Resort & Spa",
            description="Beachfront resort with beautiful sunset views",
            star_rating=4.0,
            location_id=8,  # Koh Lanta
            address="279 Moo 3, Saladan, Koh Lanta",
            price_per_night=105.0,
            amenities="Swimming pools, Spa, Restaurant, Beach bar, Free WiFi",
            image_url="https://example.com/lanta_sand.jpg"
        ),
        Hotel(
            name="The Brown Hotel",
            description="Modern hotel in central Krabi Town",
            star_rating=3.5,
            location_id=9,  # Krabi Town
            address="129 Uttarakit Road, Paknam, Muang, Krabi",
            price_per_night=55.0,
            amenities="Restaurant, Free WiFi, Tour desk, Airport shuttle",
            image_url="https://example.com/brown_hotel.jpg"
        ),
    ]
    
    db.add_all(hotels)
    db.commit()
    
    return hotels


def seed_activities(db, locations):
    """Seed activity data for locations"""
    activities = [
        Activity(
            name="Bangla Road Night Experience",
            description="Experience Patong's famous nightlife scene along Bangla Road",
            duration=4.0,
            price=30.0,
            location_id=1,  # Patong Beach
            image_url="https://example.com/bangla_road.jpg",
            activity_type="Nightlife"
        ),
        Activity(
            name="Patong Beach Day",
            description="Relax on Patong Beach with included sun loungers and umbrella",
            duration=6.0,
            price=15.0,
            location_id=1,  # Patong Beach
            image_url="https://example.com/patong_beach.jpg",
            activity_type="Beach"
        ),
        Activity(
            name="Karon Viewpoint Visit",
            description="Visit the famous Karon Viewpoint for spectacular views of three beaches",
            duration=2.0,
            price=25.0,
            location_id=2,  # Karon Beach
            image_url="https://example.com/karon_viewpoint.jpg",
            activity_type="Sightseeing"
        ),
        Activity(
            name="Surf Lesson at Kata Beach",
            description="Learn to surf with professional instructors at Kata Beach",
            duration=3.0,
            price=45.0,
            location_id=3,  # Kata Beach
            image_url="https://example.com/kata_surf.jpg",
            activity_type="Water Sport"
        ),
        Activity(
            name="Old Phuket Town Walking Tour",
            description="Guided tour of Phuket Town's historic center with Sino-Portuguese architecture",
            duration=3.0,
            price=35.0,
            location_id=4,  # Phuket Town
            image_url="https://example.com/phuket_town_tour.jpg",
            activity_type="Cultural Tour"
        ),
        Activity(
            name="Phi Phi Islands Boat Tour",
            description="Full-day speedboat tour of Phi Phi Islands including Maya Bay and snorkeling spots",
            duration=8.0,
            price=85.0,
            location_id=5,  # Phi Phi Islands
            image_url="https://example.com/phi_phi_tour.jpg",
            activity_type="Boat Tour"
        ),
        Activity(
            name="Kayaking at Ao Nang",
            description="Guided kayaking tour through the stunning limestone cliffs and lagoons",
            duration=4.0,
            price=40.0,
            location_id=6,  # Ao Nang
            image_url="https://example.com/ao_nang_kayak.jpg",
            activity_type="Water Sport"
        ),
        Activity(
            name="Rock Climbing at Railay",
            description="Rock climbing session on Railay's world-famous limestone cliffs for all levels",
            duration=5.0,
            price=65.0,
            location_id=7,  # Railay Beach
            image_url="https://example.com/railay_climbing.jpg",
            activity_type="Adventure"
        ),
        Activity(
            name="Four Islands Tour from Railay",
            description="Boat tour to four nearby islands with snorkeling and beach time",
            duration=7.0,
            price=55.0,
            location_id=7,  # Railay Beach
            image_url="https://example.com/four_islands.jpg",
            activity_type="Boat Tour"
        ),
        Activity(
            name="Koh Lanta National Park Trip",
            description="Visit to Koh Lanta National Park with hiking and beach time",
            duration=6.0,
            price=50.0,
            location_id=8,  # Koh Lanta
            image_url="https://example.com/lanta_national_park.jpg",
            activity_type="Nature"
        ),
        Activity(
            name="Krabi Night Market Tour",
            description="Evening tour of Krabi's vibrant night market with food tastings",
            duration=3.0,
            price=25.0,
            location_id=9,  # Krabi Town
            image_url="https://example.com/krabi_night_market.jpg",
            activity_type="Food & Culture"
        ),
        Activity(
            name="Tiger Cave Temple Tour",
            description="Visit the famous Tiger Cave Temple with 1,237 steps to panoramic views",
            duration=4.0,
            price=35.0,
            location_id=9,  # Krabi Town
            image_url="https://example.com/tiger_cave.jpg",
            activity_type="Cultural Tour"
        ),
        Activity(
            name="Elephant Sanctuary Visit",
            description="Ethical elephant sanctuary visit with feeding and bathing",
            duration=5.0,
            price=70.0,
            location_id=4,  # Phuket Town
            image_url="https://example.com/elephant_sanctuary.jpg",
            activity_type="Wildlife"
        ),
        Activity(
            name="Big Buddha Visit",
            description="Trip to Phuket's iconic 45-meter marble Buddha statue with island views",
            duration=3.0,
            price=30.0,
            location_id=4,  # Phuket Town
            image_url="https://example.com/big_buddha.jpg",
            activity_type="Cultural Tour"
        ),
        Activity(
            name="Thai Cooking Class",
            description="Learn to cook authentic Thai dishes with local ingredients",
            duration=4.0,
            price=55.0,
            location_id=9,  # Krabi Town
            image_url="https://example.com/thai_cooking.jpg",
            activity_type="Food & Culture"
        ),
    ]
    
    db.add_all(activities)
    db.commit()
    
    return activities


def seed_transfers(db, locations):
    """Seed transfer data between locations"""
    transfers = [
        # Phuket Airport to destinations
        Transfer(
            origin_id=4,  # Phuket Town (near airport)
            destination_id=1,  # Patong Beach
            transfer_type="Car",
            duration=1.0,
            price=20.0,
            description="Private car transfer from Phuket Airport to Patong Beach"
        ),
        Transfer(
            origin_id=4,  # Phuket Town
            destination_id=2,  # Karon Beach
            transfer_type="Car",
            duration=1.2,
            price=25.0,
            description="Private car transfer from Phuket Town to Karon Beach"
        ),
        Transfer(
            origin_id=4,  # Phuket Town
            destination_id=3,  # Kata Beach
            transfer_type="Car",
            duration=1.3,
            price=25.0,
            description="Private car transfer from Phuket Town to Kata Beach"
        ),
        
        # Between Phuket beaches
        Transfer(
            origin_id=1,  # Patong Beach
            destination_id=2,  # Karon Beach
            transfer_type="Car",
            duration=0.3,
            price=15.0,
            description="Private car transfer between Patong and Karon Beach"
        ),
        Transfer(
            origin_id=2,  # Karon Beach
            destination_id=3,  # Kata Beach
            transfer_type="Car",
            duration=0.2,
            price=12.0,
            description="Private car transfer between Karon and Kata Beach"
        ),
        Transfer(
            origin_id=1,  # Patong Beach
            destination_id=3,  # Kata Beach
            transfer_type="Car",
            duration=0.5,
            price=15.0,
            description="Private car transfer between Patong and Kata Beach"
        ),
        
        # To/From Phi Phi Island
        Transfer(
            origin_id=1,  # Patong Beach
            destination_id=5,  # Phi Phi Islands
            transfer_type="Speedboat",
            duration=1.0,
            price=40.0,
            description="Speedboat transfer from Patong to Phi Phi Islands"
        ),
        Transfer(
            origin_id=5,  # Phi Phi Islands
            destination_id=1,  # Patong Beach
            transfer_type="Speedboat",
            duration=1.0,
            price=40.0,
            description="Speedboat transfer from Phi Phi Islands to Patong"
        ),
        Transfer(
            origin_id=5,  # Phi Phi Islands
            destination_id=6,  # Ao Nang
            transfer_type="Ferry",
            duration=1.5,
            price=25.0,
            description="Ferry transfer from Phi Phi Islands to Ao Nang"
        ),
        
        # Krabi transfers
        Transfer(
            origin_id=9,  # Krabi Town
            destination_id=6,  # Ao Nang
            transfer_type="Car",
            duration=0.5,
            price=15.0,
            description="Private car transfer from Krabi Town to Ao Nang"
        ),
        Transfer(
            origin_id=6,  # Ao Nang
            destination_id=7,  # Railay Beach
            transfer_type="Longtail Boat",
            duration=0.3,
            price=10.0,
            description="Longtail boat transfer from Ao Nang to Railay Beach"
        ),
        Transfer(
            origin_id=7,  # Railay Beach
            destination_id=6,  # Ao Nang
            transfer_type="Longtail Boat",
            duration=0.3,
            price=10.0,
            description="Longtail boat transfer from Railay Beach to Ao Nang"
        ),
        Transfer(
            origin_id=6,  # Ao Nang
            destination_id=8,  # Koh Lanta
            transfer_type="Minivan + Ferry",
            duration=2.5,
            price=35.0,
            description="Combined minivan and ferry transfer from Ao Nang to Koh Lanta"
        ),
        
        # Between regions
        Transfer(
            origin_id=1,  # Patong Beach
            destination_id=6,  # Ao Nang
            transfer_type="Minivan",
            duration=3.0,
            price=55.0,
            description="Private minivan transfer from Patong Beach to Ao Nang"
        ),
        Transfer(
            origin_id=4,  # Phuket Town
            destination_id=9,  # Krabi Town
            transfer_type="Minivan",
            duration=2.5,
            price=45.0,
            description="Private minivan transfer from Phuket Town to Krabi Town"
        ),
    ]
    
    db.add_all(transfers)
    db.commit()
    
    return transfers


def create_itineraries_with_plans(db, hotels, activities, transfers):
    """Create itineraries with daily plans"""
    # Create 3-night Phuket itinerary
    phuket_3n = Itinerary(
        name="Phuket Getaway",
        description="A short trip to explore the beautiful beaches and vibrant nightlife of Phuket",
        nights=3,
        total_price=0,  # Will be calculated
        is_recommended=True
    )
    db.add(phuket_3n)
    db.flush()
    
    # Add daily plans
    # Day 1
    day1 = DailyPlan(
        day_number=1,
        itinerary_id=phuket_3n.id,
        hotel_id=1,  # Patong Resort
        transfer_id=1,  # Phuket Town to Patong
        notes="Arrive in Phuket and transfer to Patong Beach"
    )
    db.add(day1)
    db.flush()
    
    # Add Day 1 activity
    patong_beach_day = db.query(Activity).filter_by(name="Patong Beach Day").first()
    if patong_beach_day:
        day1.activities.append(patong_beach_day)
    
    # Day 2
    day2 = DailyPlan(
        day_number=2,
        itinerary_id=phuket_3n.id,
        hotel_id=1,  # Stay at same hotel
        transfer_id=None,
        notes="Full day exploring Patong area"
    )
    db.add(day2)
    db.flush()
    
    # Add Day 2 activities
    bangla_road = db.query(Activity).filter_by(name="Bangla Road Night Experience").first()
    if bangla_road:
        day2.activities.append(bangla_road)
    
    # Day 3
    day3 = DailyPlan(
        day_number=3,
        itinerary_id=phuket_3n.id,
        hotel_id=2,  # Move to Karon
        transfer_id=3,  # Patong to Karon
        notes="Change of scenery at Karon Beach"
    )
    db.add(day3)
    db.flush()
    
    # Add Day 3 activity
    karon_view = db.query(Activity).filter_by(name="Karon Viewpoint Visit").first()
    if karon_view:
        day3.activities.append(karon_view)
    
    # Create 5-night Krabi itinerary
    krabi_5n = Itinerary(
        name="Krabi Explorer",
        description="Discover the stunning islands and enjoy the water activities in Krabi",
        nights=5,
        total_price=0,  # Will be calculated
        is_recommended=True
    )
    db.add(krabi_5n)
    db.flush()
    
    # Add daily plans for Krabi
    # Day 1
    day1 = DailyPlan(
        day_number=1,
        itinerary_id=krabi_5n.id,
        hotel_id=6,  # Ao Nang Cliff
        transfer_id=10,  # Krabi Town to Ao Nang
        notes="Arrive in Krabi and transfer to Ao Nang beach"
    )
    db.add(day1)
    db.flush()
    
    # Day 2
    day2 = DailyPlan(
        day_number=2,
        itinerary_id=krabi_5n.id,
        hotel_id=6,  # Ao Nang Cliff
        transfer_id=None,
        notes="Water activities in Ao Nang"
    )
    db.add(day2)
    db.flush()
    
    kayaking = db.query(Activity).filter_by(name="Kayaking at Ao Nang").first()
    if kayaking:
        day2.activities.append(kayaking)
    
    # Days 3-5...
    # Add more daily plans for Krabi
    
    # Create 7-night Combined itinerary
    combined_7n = Itinerary(
        name="Phuket and Krabi Adventure",
        description="An exciting journey through the highlights of both Phuket and Krabi",
        nights=7,
        total_price=0,  # Will be calculated
        is_recommended=True
    )
    db.add(combined_7n)
    db.flush()
    
    # Add daily plans for combined itinerary...
    
    # Calculate total prices
    for itinerary in [phuket_3n, krabi_5n, combined_7n]:
        total_price = 0
        
        for plan in itinerary.daily_plans:
            # Hotel cost
            total_price += db.query(Hotel).get(plan.hotel_id).price_per_night
            
            # Transfer cost if any
            if plan.transfer_id:
                total_price += db.query(Transfer).get(plan.transfer_id).price
                
            # Activities costs
            for activity in plan.activities:
                total_price += activity.price
        
        itinerary.total_price = round(total_price, 2)
    
    db.commit()
    
    return [phuket_3n, krabi_5n, combined_7n]


def add_remaining_night_durations(db, existing_itineraries, hotels, activities, transfers):
    """Add itineraries for all required night durations from 2-8"""
    # Get the night durations of existing itineraries
    existing_nights = {i.nights for i in existing_itineraries}
    
    # Create itineraries for any missing duration
    for nights in range(2, 9):
        if nights not in existing_nights:
            print(f"Creating itinerary for {nights} nights...")
            region = "Phuket" if nights < 4 else "Krabi" if nights > 6 else "Phuket and Krabi"
            
            # Create new itinerary
            new_itinerary = Itinerary(
                name=f"{nights}-Night {region} Adventure",
                description=f"A {nights}-night journey through the best of {region}",
                nights=nights,
                total_price=0,  # Will be calculated
                is_recommended=True
            )
            db.add(new_itinerary)
            db.flush()
            
            # Add daily plans
            total_price = 0
            
            # Choose hotels based on region
            if region == "Phuket":
                hotel_ids = [1, 2, 3, 4]  # Phuket hotels
            elif region == "Krabi":
                hotel_ids = [6, 7, 8, 9]  # Krabi hotels
            else:
                hotel_ids = [1, 2, 3, 4, 6, 7, 8, 9]  # All hotels
            
            # Create daily plans for each day
            for day in range(1, nights + 1):
                hotel_id = random.choice(hotel_ids)
                hotel = db.query(Hotel).filter_by(id=hotel_id).one()
                
                # Add transfer on first day and occasionally
                transfer_id = None
                if day == 1:
                    if hotel.location.region == "Phuket":
                        transfer_id = 1  # To Patong
                    else:
                        transfer_id = 10  # To Ao Nang
                elif random.random() < 0.3:
                    transfer_id = random.choice([3, 4, 11, 12])
                
                # Create daily plan
                daily_plan = DailyPlan(
                    day_number=day,
                    itinerary_id=new_itinerary.id,
                    hotel_id=hotel_id,
                    transfer_id=transfer_id,
                    notes=f"Day {day} of your {nights}-night adventure"
                )
                db.add(daily_plan)
                db.flush()
                
                # Add hotel cost
                total_price += hotel.price_per_night
                
                # Add transfer cost if any
                if transfer_id:
                    transfer = db.query(Transfer).filter_by(id=transfer_id).one()
                    total_price += transfer.price
                
                # Add 1-2 activities
                location_id = hotel.location_id
                possible_activities = db.query(Activity).filter_by(location_id=location_id).all()
                if possible_activities:
                    num_activities = random.randint(1, min(2, len(possible_activities)))
                    selected_activities = random.sample(possible_activities, num_activities)
                    
                    for activity in selected_activities:
                        daily_plan.activities.append(activity)
                        total_price += activity.price
            
            # Update total price
            new_itinerary.total_price = round(total_price, 2)
            db.commit()


if __name__ == "__main__":
    # Clean existing database
    if clean_database():
        # Initialize fresh database
        if initialize_database():
            print("\nDatabase initialization completed successfully!")
            print("You can now run the API server with: uvicorn app.main:app --reload")
            print("And test the system with: python simple_mcp_test.py")
        else:
            print("\nDatabase initialization failed.")
    else:
        print("\nFailed to clean existing database.")
