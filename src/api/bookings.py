from fastapi import APIRouter, HTTPException

from src.api.dependencies import UserIdDep, DBDep
from src.exeptions import ObjectNotFoundException, AllRoomsAreBookedException
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.schemas.hotels import Hotel

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def add_booking(user_id: UserIdDep, db: DBDep, booking_data: BookingAddRequest):
    # получить цену номера
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Номер не найден")
    # if not room:
    #     raise HTTPException(status_code=404, detail="Номер не найден")
    hotel: Hotel = await db.hotels.get_one(id=room.hotel_id)
    room_price: int = room.price
    # создать схему данных BookingAdd
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.dict(),
    )
    # добавить бронирование конкретному пользователю
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    except AllRoomsAreBookedException:
        raise HTTPException(status_code=409, detail="Не осталось свободных номеров")
    await db.commit()
    return {"status": "ok", "data": booking}
