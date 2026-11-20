from datetime import timedelta
from typing import Any, Dict
from faker import Faker

fake = Faker()


def build_booking(**overrides) -> Dict[str, Any]:
    """Generate dynamic booking payload with sensible defaults and optional overrides."""
    checkin_date = fake.date_between(start_date="+10d", end_date="+60d")
    checkout_date = checkin_date + timedelta(days=fake.random_int(min=1, max=10))

    bookingdates = {
        "checkin": checkin_date.isoformat(),
        "checkout": checkout_date.isoformat(),
    }

    if "bookingdates" in overrides:
        bookingdates.update(overrides.pop("bookingdates"))

    data = {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": fake.random_int(min=50, max=1000),
        "depositpaid": fake.boolean(),
        "bookingdates": bookingdates,
        "additionalneeds": "Breakfast",
    }
    data.update(overrides)
    return data
