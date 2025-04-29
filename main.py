import uvicorn
from fastapi import FastAPI
from app.api.routes import router
from config import API_PREFIX

app = FastAPI(title="Thailand Itinerary Planner")

# Include the API router with prefix
app.include_router(router, prefix=API_PREFIX)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
