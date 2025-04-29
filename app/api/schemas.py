from pydantic import BaseModel, Field
from typing import List, Optional


class ActivityBase(BaseModel):
    name: str
    description: str
    duration: float
    price: float
    activity_type: str


class ActivityCreate(ActivityBase):
    location_id: int
    image_url: Optional[str] = None


class ActivityResponse(ActivityBase):
    id: int
    location_id: int
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class HotelBase(BaseModel):
    name: str
    description: str
    star_rating: float
    address: str
    price_per_night: float


class HotelCreate(HotelBase):
    location_id: int
    amenities: Optional[str] = None
    image_url: Optional[str] = None


class HotelResponse(HotelBase):
    id: int
    location_id: int
    amenities: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class TransferBase(BaseModel):
    transfer_type: str
    duration: float
    price: float
    description: str


class TransferCreate(TransferBase):
    origin_id: int
    destination_id: int


class TransferResponse(TransferBase):
    id: int
    origin_id: int
    destination_id: int

    class Config:
        from_attributes = True


class DailyPlanBase(BaseModel):
    day_number: int
    notes: Optional[str] = None


class DailyPlanCreate(DailyPlanBase):
    hotel_id: int
    transfer_id: Optional[int] = None
    activity_ids: List[int] = []


class DailyPlanResponse(DailyPlanBase):
    id: int
    hotel: HotelResponse
    transfer: Optional[TransferResponse] = None
    activities: List[ActivityResponse] = []

    class Config:
        from_attributes = True


class ItineraryBase(BaseModel):
    name: str
    description: str
    nights: int


class ItineraryCreate(ItineraryBase):
    daily_plans: List[DailyPlanCreate]


class ItineraryResponse(ItineraryBase):
    id: int
    total_price: float
    daily_plans: List[DailyPlanResponse]
    is_recommended: bool = False

    class Config:
        from_attributes = True


class LocationBase(BaseModel):
    name: str
    region: str
    description: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class LocationCreate(LocationBase):
    pass


class LocationResponse(LocationBase):
    id: int

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    detail: str
