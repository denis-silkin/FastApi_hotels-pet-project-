from datetime import date

from fastapi import Query, APIRouter, Body, HTTPException
from fastapi_cache.decorator import cache

from src.exeptions import check_date_to_after_date_from, ObjectNotFoundException
from src.schemas.hotels import Hotel, HotelPATCH, HotelAdd
from src.api.dependencies import PaginationDep, DBDep
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="Локация"),
    title: str | None = Query(None, description="Название отеля"),
    date_from: date = Query(examples=["2025-08-01"]),
    date_to: date = Query(examples=["2025-08-10"]),
):
    hotels = await HotelService(db).get_filtered_by_time(pagination, location, title, date_from, date_to)

    return {"status": "OK", "data": hotels}


@router.get("/{hotel_id}", summary="получение одного отеля")
@cache(expire=10)
async def get_hotels_one(hotel_id: int, db: DBDep):
    try:
        return HotelService(db).get_hotels_one(hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Отель не найден")


# body, request body
@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Сочи 5 звезд у моря",
                    "location": "ул. Моря, 1",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {"title": "Отель Дубай у фонтана", "location": "ул. Шейха, 2"},
            },
        }
    ),
):
    hotel = await HotelService(db).add_hotel(hotel_data)

    return {"status": "ok", "data": hotel}


@router.delete("/{hotel_id}/")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete_by(id=hotel_id)
    await db.commit()
    return {"status": "ok"}


@router.put("/{hotel_id}")
async def change_hotel(hotel_id: int, hotel_data: Hotel, db: DBDep):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "ok"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное редактирование данных отеля",
    description="Описывает что делает функция в АПИ",
)
async def pat_hotel(hotel_id: int, hotel_data: HotelPATCH, db: DBDep):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "ok"}
