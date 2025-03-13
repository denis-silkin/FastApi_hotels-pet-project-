from pydantic import BaseModel


class Rooms(BaseModel):
    hotel_id: int
    title: str
    description: str
    price: int
    quantity: int
