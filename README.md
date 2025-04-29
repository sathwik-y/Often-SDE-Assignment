# Thailand Travel Itinerary System

A backend system for managing travel itineraries for Thailand's Phuket and Krabi regions, featuring a database for trip itineraries, RESTful API endpoints, and an MCP server for recommended itineraries.

## Features

- **Database Architecture**: SQLAlchemy models for accommodations, transfers, activities, and itineraries
- **RESTful API**: FastAPI endpoints for creating and viewing itineraries
- **MCP Server**: Model Context Protocol server for recommended itineraries
- **Seed Data**: Realistic data for Thailand's Phuket and Krabi regions
- **Itineraries**: Pre-built plans ranging from 2-8 nights

## Prerequisites

- Python 3.8+
- pip or uv (Python package manager)

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd Itenary
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   ```
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Initialize the database:
   ```
   python initialize_db.py
   ```

## Running the Application

### Start the FastAPI Server

```
uvicorn app.main:app --reload
```

This will start the API server at http://127.0.0.1:8000

### Access API Documentation

Open your browser and navigate to:
- http://127.0.0.1:8000/docs - Interactive API documentation (Swagger UI)
- http://127.0.0.1:8000/redoc - Alternative documentation (ReDoc)

### Run the MCP Server

```
python -m app.mcp.server
```

### Testing

1. Test the API endpoints:
   ```
   python simple_mcp_test.py
   ```

2. Test the MCP server directly:
   ```
   python direct_mcp_test.py
   ```

## API Endpoints

### GET `/api/v1/itineraries/`
Retrieve all itineraries with optional filtering by number of nights and recommended status.

Query parameters:
- `nights`: Filter by number of nights
- `recommended_only`: Filter only recommended itineraries
- `skip`: Number of records to skip (pagination)
- `limit`: Maximum number of records to return (pagination)

### GET `/api/v1/itineraries/{itinerary_id}`
Retrieve a specific itinerary by its ID.

### POST `/api/v1/itineraries/`
Create a new itinerary with daily plans.

## MCP Server

The MCP server provides tools and resources for working with itineraries:

### Tools

- `get_recommended_itinerary`: Get a recommended itinerary for a specific number of nights
- `list_available_durations`: List all available durations for recommended itineraries

### Resources

- `itineraries://recommended/{nights}`: Get information about recommended itineraries

### Prompts

- `recommend_itinerary`: Create a prompt for itinerary recommendations

## Project Structure

```
Itenary/
│
├── app/                      # Main application package
│   ├── api/                  # API endpoints and schemas
│   │   ├── __init__.py
│   │   ├── routes.py         # API route handlers
│   │   └── schemas.py        # Pydantic models for validation
│   │
│   ├── database/             # Database configuration
│   │   ├── __init__.py
│   │   └── db.py             # Database connection setup
│   │
│   ├── mcp/                  # MCP server components
│   │   ├── __init__.py
│   │   └── server.py         # MCP server implementation
│   │
│   ├── models/               # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── models.py         # Database entity models
│   │
│   ├── seed/                 # Database seeding
│   │   ├── __init__.py
│   │   └── seed_data.py      # Seed data implementation
│   │
│   ├── __init__.py
│   └── main.py               # FastAPI application setup
│
├── venv/                     # Virtual environment (not in repo)
│
├── config.py                 # Configuration settings
├── initialize_db.py          # Database initialization script
├── requirements.txt          # Project dependencies
├── simple_mcp_test.py        # Simple test script
└── README.md                 # This file
```

## Commands Reference

### Database Management

- Initialize database with seed data:
  ```
  python initialize_db.py
  ```

- Clean database (remove existing database file):
  ```
  python clean_db.py
  ```

### Server Commands

- Start FastAPI server:
  ```
  uvicorn app.main:app --reload
  ```

- Start MCP server:
  ```
  python -m app.mcp.server
  ```

### Testing

- Test API endpoints:
  ```
  python simple_mcp_test.py
  ```

- Test MCP server directly:
  ```
  python direct_mcp_test.py
  ```

- Test with MCP CLI tools (if available):
  ```
  mcp dev mcp_server_wrapper.py
  ```

## License

[Specify License]

## Author

[Your Name]
