import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./itinerary.db")

# API Configuration
API_PREFIX = "/api/v1"

# MCP Server Configuration
MCP_SERVER_NAME = "ThailandItineraryServer"
MCP_SERVER_VERSION = "1.0.0"

# Seed data configuration
MIN_NIGHTS = 2
MAX_NIGHTS = 8
