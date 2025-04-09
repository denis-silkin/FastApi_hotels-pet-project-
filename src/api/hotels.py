from datetime import date

from fastapi import Query, APIRouter, Body

from schemas.hotels import Hotel, HotelPATCH
from api.dependencies import PaginationDep, DBDep

router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get('')
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description='Локация'),
        title: str | None = Query(None, description='Название отеля'),
        date_from: date = Query(example="2025-08-01"),
        date_to: date = Query(example="2025-08-10"),
):
    page_size = pagination.page_size or 5
    return await db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=page_size,
            offset=page_size * (pagination.page - 1)
        )


@router.get('/{hotel_id}', summary="получение одного отеля")
async def get_hotels_one(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


# body, request body
@router.post('')
async def create_hotel(
        db: DBDep,
        hotel_data: Hotel = Body(openapi_examples={
            '1': {'summary': 'Сочи', 'value': {
                'title': "Отель Сочи 5 звезд у моря",
                'location': 'ул. Моря, 1'}},
            '2': {'summary': 'Дубай', 'value': {
                'title': "Отель Дубай у фонтана",
                'location': 'ул. Шейха, 2'}},
        })):
    hotel = await db.hotels.add(hotel_data)
    # print(add_hotel_stnt.compile(engine, compile_kwargs={"literal_binds": True}))  # debug
    await db.commit()

    return {'status': 'ok', "data": hotel}


@router.delete('/{hotel_id}/')
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete_by(id=hotel_id)
    await db.commit()
    return {'status': 'ok'}


@router.put('/{hotel_id}')
async def change_hotel(
        hotel_id: int,
        hotel_data: Hotel,
        db: DBDep):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {'status': 'ok'}


@router.patch('/{hotel_id}', summary='Частичное редактирование данных отеля',
              description='Описывает что делает функция в АПИ')
async def pat_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
        db: DBDep
):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {'status': 'ok'}
