from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from config import API_PREFIX

# Initialize FastAPI app
app = FastAPI(
    title="Thailand Travel Itinerary API",
    description="API for managing travel itineraries in Thailand",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=API_PREFIX)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Thailand Travel Itinerary API",
        "docs": "/docs",
        "api_version": "1.0.0"
    }
