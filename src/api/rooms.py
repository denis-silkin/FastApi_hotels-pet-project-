from datetime import date

from fastapi import APIRouter, Body, Query

from api.dependencies import DBDep
from schemas.facilities import RoomFacilityAdd
from schemas.rooms import RoomAdd, RoomPatchRequest, RoomPatch, RoomAddRequest

router = APIRouter(prefix='/hotels', tags=['Номера'])


@router.get("{hotel_id}/rooms")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2025-08-01"),
        date_to: date = Query(example="2025-08-10"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}", summary="получение одного номера")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none_with_rels(hotel_id=hotel_id, id=room_id)


@router.post('/{hotel_id}/rooms')
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    # print(add_hotel_stnt.compile(engine, compile_kwargs={"literal_binds": True}))  # debug

    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()

    return {'status': 'ok', "data": room}


@router.delete('/{hotel_id}/rooms{room_id}')
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete_by(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {'status': 'ok'}


@router.put('/{hotel_id}/rooms/{room_id}')
async def change_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest,
        db: DBDep):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.rooms_facilities.set_room_facility(room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()

    return {'status': 'ok'}


@router.patch('/{hotel_id}/rooms{room_id}', summary='Частичное редактирование данных номера',
              description='Описывает что делает функция в АПИ')
async def pat_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
        db: DBDep
):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.edit(_room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facility(room_id, facilities_ids=_room_data_dict["facilities_ids"])
    await db.commit()

    return {'status': 'ok'}
