from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Table, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from app.database.db import Base

# Association table for many-to-many relationship between DailyPlan and Activity
daily_plan_activity = Table(
    "daily_plan_activity",
    Base.metadata,
    Column("daily_plan_id", Integer, ForeignKey("daily_plans.id")),
    Column("activity_id", Integer, ForeignKey("activities.id")),
)


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    region = Column(String(100), nullable=False)  # e.g., Phuket, Krabi
    description = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)

    # Relationships
    hotels = relationship("Hotel", back_populates="location")
    activities = relationship("Activity", back_populates="location")
    
    # Location as origin for transfers
    transfers_from = relationship("Transfer", foreign_keys="Transfer.origin_id", back_populates="origin")
    # Location as destination for transfers
    transfers_to = relationship("Transfer", foreign_keys="Transfer.destination_id", back_populates="destination")


class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    star_rating = Column(Float)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    address = Column(String(200))
    price_per_night = Column(Float)
    amenities = Column(Text)  # Comma-separated list of amenities
    image_url = Column(String(255))

    # Relationships
    location = relationship("Location", back_populates="hotels")
    daily_plans = relationship("DailyPlan", back_populates="hotel")


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    duration = Column(Float)  # in hours
    price = Column(Float)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    image_url = Column(String(255))
    activity_type = Column(String(50))  # e.g., "Excursion", "Tour", "Beach Activity"

    # Relationships
    location = relationship("Location", back_populates="activities")
    daily_plans = relationship("DailyPlan", secondary=daily_plan_activity, back_populates="activities")


class Transfer(Base):
    __tablename__ = "transfers"

    id = Column(Integer, primary_key=True, index=True)
    origin_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    destination_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    transfer_type = Column(String(50))  # e.g., "Car", "Boat", "Flight"
    duration = Column(Float)  # in hours
    price = Column(Float)
    description = Column(Text)

    # Relationships
    origin = relationship("Location", foreign_keys=[origin_id], back_populates="transfers_from")
    destination = relationship("Location", foreign_keys=[destination_id], back_populates="transfers_to")
    daily_plans = relationship("DailyPlan", back_populates="transfer")


class Itinerary(Base):
    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    nights = Column(Integer, nullable=False)
    total_price = Column(Float)
    is_recommended = Column(Boolean, default=False)  # Flag for recommended itineraries
    
    # Relationships
    daily_plans = relationship("DailyPlan", back_populates="itinerary", cascade="all, delete-orphan")


class DailyPlan(Base):
    __tablename__ = "daily_plans"

    id = Column(Integer, primary_key=True, index=True)
    day_number = Column(Integer, nullable=False)  # Day 1, Day 2, etc.
    itinerary_id = Column(Integer, ForeignKey("itineraries.id"), nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    transfer_id = Column(Integer, ForeignKey("transfers.id"), nullable=True)  # Optional transfer
    notes = Column(Text)

    # Relationships
    itinerary = relationship("Itinerary", back_populates="daily_plans")
    hotel = relationship("Hotel", back_populates="daily_plans")
    activities = relationship("Activity", secondary=daily_plan_activity, back_populates="daily_plans")
    transfer = relationship("Transfer", back_populates="daily_plans")
