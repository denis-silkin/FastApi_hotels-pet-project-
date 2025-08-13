from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.exeptions import RoomNotFoundException, HotelNotFoundException, HotelNotFoundHTTPException
from src.schemas.rooms import  RoomPatchRequest, RoomAddRequest
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("{hotel_id}/rooms")
@cache(expire=10)
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(examples=["2025-08-01"]),
    date_to: date = Query(examples=["2025-08-10"]),
):
    return await RoomService(db).get_filtered_by_time(hotel_id, date_from, date_to)


@router.get("/{hotel_id}/rooms/{room_id}", summary="получение одного номера")
@cache(expire=10)
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        return await db.rooms.get_one_with_rels(hotel_id=hotel_id, id=room_id)
    except RoomNotFoundException:
        raise RoomNotHTTPException


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body()):
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "ok", "data": room}


@router.delete("/{hotel_id}/rooms{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await RoomService(db).delete_room(hotel_id, room_id)
    return {"status": "ok"}


@router.put("/{hotel_id}/rooms/{room_id}")
async def change_room(
    hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep
):
    await RoomService(db).change_room(hotel_id, room_id, room_data)

    return {"status": "ok"}


@router.patch(
    "/{hotel_id}/rooms{room_id}",
    summary="Частичное редактирование данных номера",
    description="Описывает что делает функция в АПИ",
)
async def pat_room(hotel_id: int, room_id: int, room_data: RoomPatchRequest, db: DBDep):
    await RoomService(db).pat_room(hotel_id, room_id, room_data)

    return {"status": "ok"}
