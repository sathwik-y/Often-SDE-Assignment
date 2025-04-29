# Thailand Travel Itinerary System - Documentation

## API Documentation

### Endpoints

#### GET `/api/v1/itineraries/`
Retrieves a list of all itineraries with optional filtering.

**Query Parameters:**
- `nights`: Filter by number of nights (optional)
- `recommended_only`: Boolean to filter only recommended itineraries (optional)
- `skip`: Number of records to skip for pagination (default: 0)
- `limit`: Maximum number of records to return (default: 10)

**Response:**
```json
[
  {
    "id": 1,
    "name": "Phuket Getaway",
    "description": "A short trip to explore the beautiful beaches and vibrant nightlife of Phuket",
    "nights": 3,
    "total_price": 375.0,
    "is_recommended": true,
    "daily_plans": [...]
  },
  {
    "id": 2,
    "name": "Krabi Explorer",
    "description": "Discover the stunning islands and enjoy the water activities in Krabi",
    "nights": 5,
    "total_price": 295.0,
    "is_recommended": true,
    "daily_plans": [...]
  }
]
```

#### GET `/api/v1/itineraries/{itinerary_id}`
Retrieves a specific itinerary by its ID.

**Parameters:**
- `itinerary_id`: The unique identifier of the itinerary

**Response:**
```json
{
  "id": 1,
  "name": "Phuket Getaway",
  "description": "A short trip to explore the beautiful beaches and vibrant nightlife of Phuket",
  "nights": 3,
  "total_price": 375.0,
  "is_recommended": true,
  "daily_plans": [
    {
      "id": 1,
      "day_number": 1,
      "notes": "Arrive in Phuket and transfer to Patong Beach",
      "hotel": {
        "id": 1,
        "name": "Patong Resort Hotel",
        "description": "Comfortable resort close to Patong's beach and nightlife",
        "star_rating": 4.0,
        "address": "208 Rat-Uthit 200 Pi Road, Patong, Kathu, Phuket",
        "price_per_night": 85.0,
        "amenities": "Swimming pool, Restaurant, Free WiFi, Spa, Fitness center",
        "image_url": "https://example.com/patong_resort.jpg",
        "location_id": 1
      },
      "transfer": {
        "id": 1,
        "origin_id": 4,
        "destination_id": 1,
        "transfer_type": "Car",
        "duration": 1.0,
        "price": 20.0,
        "description": "Private car transfer from Phuket Airport to Patong Beach"
      },
      "activities": [
        {
          "id": 2,
          "name": "Patong Beach Day",
          "description": "Relax on Patong Beach with included sun loungers and umbrella",
          "duration": 6.0,
          "price": 15.0,
          "location_id": 1,
          "image_url": "https://example.com/patong_beach.jpg",
          "activity_type": "Beach"
        }
      ]
    },
    // Additional daily plans...
  ]
}
```

#### POST `/api/v1/itineraries/`
Creates a new itinerary with daily plans.

**Request Body:**
```json
{
  "name": "Custom Phuket Trip",
  "description": "A personalized trip to Phuket",
  "nights": 4,
  "daily_plans": [
    {
      "day_number": 1,
      "hotel_id": 1,
      "transfer_id": 1,
      "activity_ids": [1, 2],
      "notes": "Arrival day"
    },
    {
      "day_number": 2,
      "hotel_id": 1,
      "activity_ids": [13, 14],
      "notes": "Cultural day"
    },
    // Additional daily plans...
  ]
}
```

**Response:**
Returns the created itinerary with the same format as the GET endpoint.

### Error Responses

**404 Not Found:**
```json
{
  "detail": "Itinerary with ID {id} not found"
}
```

**400 Bad Request:**
```json
{
  "detail": "One or more hotel IDs not found"
}
```

## MCP Server Documentation

The MCP server provides tools and resources for working with itineraries:

### Tools

#### `get_recommended_itinerary`
Returns a recommended itinerary for a specific number of nights.

**Parameters:**
- `nights`: Integer between 2-8

**Response:**
```json
{
  "id": 1,
  "name": "Phuket Getaway",
  "description": "A short trip to explore the beautiful beaches and vibrant nightlife of Phuket",
  "nights": 3,
  "total_price": 375.0,
  "daily_plans": [
    {
      "day": 1,
      "hotel": {
        "name": "Patong Resort Hotel",
        "star_rating": 4.0,
        "location": "Patong Beach"
      },
      "activities": [
        {
          "name": "Patong Beach Day",
          "duration": 6.0,
          "type": "Beach"
        }
      ],
      "notes": "Arrive in Phuket and transfer to Patong Beach"
    },
    // Additional daily plans...
  ]
}
```

#### `list_available_durations`
Returns a list of available night durations for recommended itineraries.

**Response:**
```json
[2, 3, 4, 5, 6, 7, 8]
```

### Resources

#### `itineraries://recommended/{nights}`
Returns detailed information about recommended itineraries for a specific number of nights.

**Parameters:**
- `nights`: Number of nights for the itinerary

**Response:**
Text description of recommended itineraries with details of daily plans.

### Prompts

#### `recommend_itinerary`
Creates a prompt for recommending an itinerary for a specific number of nights.

**Parameters:**
- `nights`: Number of nights for the trip

**Response:**
A prompt text that can be used with an AI assistant to generate itinerary recommendations.

## Database Schema

### Entities

#### Location
Represents destinations in Thailand.

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| name | String | Name of the location |
| region | String | Region (Phuket, Krabi) |
| description | Text | Description of the location |
| latitude | Float | Latitude coordinate |
| longitude | Float | Longitude coordinate |

#### Hotel
Represents accommodation options.

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| name | String | Hotel name |
| description | Text | Hotel description |
| star_rating | Float | Star rating (1-5) |
| location_id | Integer | Foreign key to Location |
| address | String | Physical address |
| price_per_night | Float | Cost per night |
| amenities | Text | Comma-separated list of amenities |
| image_url | String | URL to hotel image |

#### Activity
Represents excursions and things to do.

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| name | String | Activity name |
| description | Text | Activity description |
| duration | Float | Duration in hours |
| price | Float | Cost per person |
| location_id | Integer | Foreign key to Location |
| image_url | String | URL to activity image |
| activity_type | String | Type of activity |

#### Transfer
Represents transportation between locations.

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| origin_id | Integer | Foreign key to Location (from) |
| destination_id | Integer | Foreign key to Location (to) |
| transfer_type | String | Type of transport |
| duration | Float | Duration in hours |
| price | Float | Cost per transfer |
| description | Text | Transfer description |

#### Itinerary
Represents a complete trip plan.

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| name | String | Itinerary name |
| description | Text | Itinerary description |
| nights | Integer | Number of nights |
| total_price | Float | Total cost |
| is_recommended | Boolean | Recommended flag |

#### DailyPlan
Represents a single day within an itinerary.

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| day_number | Integer | Day sequence number |
| itinerary_id | Integer | Foreign key to Itinerary |
| hotel_id | Integer | Foreign key to Hotel |
| transfer_id | Integer | Foreign key to Transfer (optional) |
| notes | Text | Day notes |

### Relationships

- **Location** has many Hotels, Activities, and is related to Transfers (origin/destination)
- **Hotel** belongs to a Location and has many DailyPlans
- **Activity** belongs to a Location and has many-to-many relationship with DailyPlans
- **Transfer** has origin and destination Locations and may be related to DailyPlans
- **Itinerary** has many DailyPlans
- **DailyPlan** belongs to an Itinerary, has one Hotel, optional Transfer, and many Activities

## Example Data

### Sample Locations
- Patong Beach (Phuket)
- Karon Beach (Phuket)
- Phi Phi Islands (Phuket)
- Ao Nang (Krabi)
- Railay Beach (Krabi)

### Sample Activities
- Bangla Road Night Experience (Patong Beach)
- Phi Phi Islands Boat Tour (Phi Phi Islands)
- Rock Climbing at Railay (Railay Beach)

### Sample Itineraries
- 3-night Phuket Getaway
- 5-night Krabi Explorer
- 7-night Phuket and Krabi Adventure
