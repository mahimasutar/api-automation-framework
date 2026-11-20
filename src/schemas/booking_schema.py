from typing import Optional
from pydantic import BaseModel, ConfigDict


class BookingDates(BaseModel):
    model_config = ConfigDict(extra="ignore")

    checkin: str
    checkout: str


class BookingPayload(BaseModel):
    model_config = ConfigDict(extra="ignore")

    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: Optional[str] = None


class BookingResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    bookingid: int
    booking: BookingPayload
