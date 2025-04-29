import random
from sqlalchemy.orm import Session

from app.models.models import (
    Location, Hotel, Activity, Transfer, Itinerary, DailyPlan
)
from config import MIN_NIGHTS, MAX_NIGHTS


def seed_locations(db: Session):
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


def seed_hotels(db: Session, locations):
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


def seed_activities(db: Session, locations):
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


def seed_transfers(db: Session, locations):
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


def create_itineraries(db: Session, hotels, activities, transfers):
    """Create itineraries with daily plans"""
    # 3-night Phuket itinerary
    phuket_3n = Itinerary(
        name="Phuket Getaway",
        description="A short trip to explore the beautiful beaches and vibrant nightlife of Phuket",
        nights=3,
        total_price=0,  # Will be calculated
        is_recommended=True
    )
    db.add(phuket_3n)
    db.flush()
    
    # Day 1: Arrival in Patong
    day1 = DailyPlan(
        day_number=1,
        itinerary_id=phuket_3n.id,
        hotel_id=1,  # Patong Resort Hotel
        transfer_id=1,  # Phuket Town to Patong
        notes="Arrival day with afternoon free time at Patong Beach"
    )
    db.add(day1)
    db.flush()
    day1.activities.append(activities[1])  # Patong Beach Day
    
    # Day 2: Patong and surroundings
    day2 = DailyPlan(
        day_number=2,
        itinerary_id=phuket_3n.id,
        hotel_id=1,  # Patong Resort Hotel
        notes="Full day in Patong area with nightlife experience"
    )
    db.add(day2)
    db.flush()
    day2.activities.append(activities[0])  # Bangla Road Night Experience
    
    # Day 3: Visit Kata Beach
    day3 = DailyPlan(
        day_number=3,
        itinerary_id=phuket_3n.id,
        hotel_id=3,  # Kata Palm Resort
        transfer_id=5,  # Patong to Kata
        notes="Change of scenery at beautiful Kata Beach"
    )
    db.add(day3)
    db.flush()
    day3.activities.append(activities[3])  # Surf Lesson at Kata Beach
    
    # 5-night Krabi itinerary
    krabi_5n = Itinerary(
        name="Krabi Explorer",
        description="Discover the stunning islands and enjoy the water activities in Krabi",
        nights=5,
        total_price=0,  # Will be calculated
        is_recommended=True
    )
    db.add(krabi_5n)
    db.flush()
    
    # Day 1: Arrival in Ao Nang
    day1 = DailyPlan(
        day_number=1,
        itinerary_id=krabi_5n.id,
        hotel_id=6,  # Aonang Cliff Beach Resort
        transfer_id=10,  # Krabi Town to Ao Nang
        notes="Arrival day with evening exploration of Ao Nang"
    )
    db.add(day1)
    db.flush()
    
    # Day 2: Kayaking Day
    day2 = DailyPlan(
        day_number=2,
        itinerary_id=krabi_5n.id,
        hotel_id=6,  # Aonang Cliff Beach Resort
        notes="Full day of water activities in the stunning limestone landscapes"
    )
    db.add(day2)
    db.flush()
    day2.activities.append(activities[6])  # Kayaking at Ao Nang
    
    # Day 3: Railay Beach Day
    day3 = DailyPlan(
        day_number=3,
        itinerary_id=krabi_5n.id,
        hotel_id=7,  # Rayavadee
        transfer_id=11,  # Ao Nang to Railay
        notes="Luxury stay at the stunning Railay Peninsula"
    )
    db.add(day3)
    db.flush()
    day3.activities.append(activities[7])  # Rock Climbing at Railay
    
    # Day 4: Island Hopping
    day4 = DailyPlan(
        day_number=4,
        itinerary_id=krabi_5n.id,
        hotel_id=7,  # Rayavadee
        notes="Exploring the stunning islands around Railay"
    )
    db.add(day4)
    db.flush()
    day4.activities.append(activities[8])  # Four Islands Tour from Railay
    
    # Day 5: Return to Krabi Town
    day5 = DailyPlan(
        day_number=5,
        itinerary_id=krabi_5n.id,
        hotel_id=9,  # The Brown Hotel
        transfer_id=12,  # Railay to Ao Nang
        notes="Final night in Krabi Town with cultural experiences"
    )
    db.add(day5)
    db.flush()
    day5.activities.append(activities[10])  # Krabi Night Market Tour
    day5.activities.append(activities[14])  # Thai Cooking Class
    
    # 7-night Phuket-Krabi combined itinerary
    combined_7n = Itinerary(
        name="Phuket and Krabi Adventure",
        description="An exciting journey through the highlights of both Phuket and Krabi",
        nights=7,
        total_price=0,  # Will be calculated
        is_recommended=True
    )
    db.add(combined_7n)
    db.flush()
    
    # Day 1-2: Patong Beach, Phuket
    day1 = DailyPlan(
        day_number=1,
        itinerary_id=combined_7n.id,
        hotel_id=1,  # Patong Resort Hotel
        transfer_id=1,  # Phuket Town to Patong
        notes="Arrival day in Phuket's most popular beach area"
    )
    db.add(day1)
    db.flush()
    day1.activities.append(activities[1])  # Patong Beach Day
    
    day2 = DailyPlan(
        day_number=2,
        itinerary_id=combined_7n.id,
        hotel_id=1,  # Patong Resort Hotel
        notes="Cultural day in Phuket"
    )
    db.add(day2)
    db.flush()
    day2.activities.append(activities[13])  # Big Buddha Visit
    day2.activities.append(activities[4])  # Old Phuket Town Walking Tour
    
    # Day 3-4: Phi Phi Islands
    day3 = DailyPlan(
        day_number=3,
        itinerary_id=combined_7n.id,
        hotel_id=5,  # Phi Phi Island Village
        transfer_id=6,  # Patong to Phi Phi
        notes="Journey to the stunning Phi Phi Islands"
    )
    db.add(day3)
    db.flush()
    day3.activities.append(activities[5])  # Phi Phi Islands Boat Tour
    
    day4 = DailyPlan(
        day_number=4,
        itinerary_id=combined_7n.id,
        hotel_id=5,  # Phi Phi Island Village
        notes="Free day to explore Phi Phi Islands at your own pace"
    )
    db.add(day4)
    db.flush()
    
    # Day 5-7: Krabi
    day5 = DailyPlan(
        day_number=5,
        itinerary_id=combined_7n.id,
        hotel_id=6,  # Aonang Cliff Beach Resort
        transfer_id=8,  # Phi Phi to Ao Nang
        notes="Transfer to Krabi's beautiful Ao Nang beach area"
    )
    db.add(day5)
    db.flush()
    day5.activities.append(activities[6])  # Kayaking at Ao Nang
    
    day6 = DailyPlan(
        day_number=6,
        itinerary_id=combined_7n.id,
        hotel_id=7,  # Rayavadee
        transfer_id=11,  # Ao Nang to Railay
        notes="Experience the exclusive Railay Peninsula"
    )
    db.add(day6)
    db.flush()
    day6.activities.append(activities[7])  # Rock Climbing at Railay
    
    day7 = DailyPlan(
        day_number=7,
        itinerary_id=combined_7n.id,
        hotel_id=9,  # The Brown Hotel
        transfer_id=12,  # Railay to Ao Nang
        notes="Final day exploring Krabi Town's culture and cuisine"
    )
    db.add(day7)
    db.flush()
    day7.activities.append(activities[10])  # Krabi Night Market Tour
    day7.activities.append(activities[11])  # Tiger Cave Temple Tour
    
    # Create itineraries list
    itineraries = [phuket_3n, krabi_5n, combined_7n]
    
    # Calculate and update total prices for all itineraries
    for itinerary in itineraries:
        total_price = 0
        
        for plan in itinerary.daily_plans:
            # Add hotel cost
            hotel = db.query(Hotel).filter(Hotel.id == plan.hotel_id).first()
            total_price += hotel.price_per_night
            
            # Add transfer cost if any
            if plan.transfer_id:
                transfer = db.query(Transfer).filter(Transfer.id == plan.transfer_id).first()
                total_price += transfer.price
            
            # Add activities cost
            for activity in plan.activities:
                total_price += activity.price
        
        # Update the itinerary with the calculated total price
        itinerary.total_price = round(total_price, 2)
    
    db.commit()
    
    return itineraries


def create_additional_itinerary(db: Session, nights: int, hotels, activities, transfers):
    """Create an additional itinerary for a specific number of nights if missing"""
    
    region = "Phuket" if nights < 4 else "Krabi" if nights > 6 else "Phuket and Krabi"
    
    itinerary = Itinerary(
        name=f"{nights}-Night {region} Adventure",
        description=f"A {nights}-night journey through the best of {region}",
        nights=nights,
        total_price=0,  # Will be calculated
        is_recommended=True
    )
    
    db.add(itinerary)
    db.flush()
    
    # Choose appropriate hotels based on region and duration
    if region == "Phuket":
        hotel_ids = [1, 2, 3, 4]  # Phuket hotels
    elif region == "Krabi":
        hotel_ids = [6, 7, 8, 9]  # Krabi hotels
    else:
        hotel_ids = [1, 2, 3, 4, 6, 7, 8, 9]  # All hotels
    
    # Create daily plans
    total_price = 0
    
    for day in range(1, nights + 1):
        # Select a random hotel
        hotel_id = random.choice(hotel_ids)
        hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
        
        # Add transfer on first day and every other day with 30% chance
        transfer_id = None
        if day == 1:
            # First day arrival transfer
            if hotel.location.region == "Phuket":
                transfer_id = 1  # Phuket Town to Patong
            else:
                transfer_id = 10  # Krabi Town to Ao Nang
        elif random.random() < 0.3:
            possible_transfers = db.query(Transfer).all()
            if possible_transfers:
                transfer = random.choice(possible_transfers)
                transfer_id = transfer.id
        
        # Create the daily plan
        plan = DailyPlan(
            day_number=day,
            itinerary_id=itinerary.id,
            hotel_id=hotel_id,
            transfer_id=transfer_id,
            notes=f"Day {day} of your {nights}-night adventure"
        )
        db.add(plan)
        db.flush()
        
        # Add hotel cost
        total_price += hotel.price_per_night
        
        # Add transfer cost if any
        if transfer_id:
            transfer = db.query(Transfer).filter(Transfer.id == transfer_id).first()
            total_price += transfer.price
        
        # Add 1-2 activities per day
        location_id = hotel.location_id
        possible_activities = db.query(Activity).filter(
            Activity.location_id == location_id
        ).all()
        
        if possible_activities:
            # Select 1-2 activities
            num_activities = random.randint(1, min(2, len(possible_activities)))
            selected_activities = random.sample(possible_activities, num_activities)
            
            for activity in selected_activities:
                plan.activities.append(activity)
                total_price += activity.price
    
    # Update the total price
    itinerary.total_price = round(total_price, 2)
    db.commit()
    
    return itinerary


def seed_database(db: Session):
    """Seed the database with all required data"""
    print("Seeding locations...")
    locations = seed_locations(db)
    
    print("Seeding hotels...")
    hotels = seed_hotels(db, locations)
    
    print("Seeding activities...")
    activities = seed_activities(db, locations)
    
    print("Seeding transfers...")
    transfers = seed_transfers(db, locations)
    
    print("Creating itineraries...")
    itineraries = create_itineraries(db, hotels, activities, transfers)
    
    print(f"Database seeded with:")
    print(f"- {len(locations)} locations")
    print(f"- {len(hotels)} hotels")
    print(f"- {len(activities)} activities")
    print(f"- {len(transfers)} transfers")
    print(f"- {len(itineraries)} itineraries")
    
    # Create itineraries for each night duration if not already present
    existing_nights = {i.nights for i in itineraries}
    
    for nights in range(MIN_NIGHTS, MAX_NIGHTS + 1):
        if nights not in existing_nights:
            print(f"Creating additional {nights}-night itinerary...")
            create_additional_itinerary(db, nights, hotels, activities, transfers)


def main():
    """Main function to seed the database"""
    from app.database.db import SessionLocal, engine
    from app.models.models import Base

    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        seed_database(db)
        print("Database seeding completed successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
