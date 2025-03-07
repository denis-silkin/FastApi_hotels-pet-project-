from fastapi import Query, APIRouter, Body
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.hotels import HotelRepository

router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get('')
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description='Локация'),
        title: str | None = Query(None, description='Название отеля'),
):
    page_size = pagination.page_size or 5
    async with async_session_maker() as session:
        return await HotelRepository(session).get_all(
            location=location,
            title=title,
            limit=page_size,
            offset=page_size * (pagination.page - 1)
        )


@router.get('/{hotel_id}', summary="получение одного отеля")
async def get_hotels_one(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelRepository(session).get_one_or_none(id=hotel_id)


# body, request body
@router.post('')
async def create_hotel(
        hotel_data: Hotel = Body(openapi_examples={
            '1': {'summary': 'Сочи', 'value': {
                'title': "Отель Сочи 5 звезд у моря",
                'location': 'ул. Моря, 1'}},
            '2': {'summary': 'Дубай', 'value': {
                'title': "Отель Дубай у фонтана",
                'location': 'ул. Шейха, 2'}},
        })):
    async with async_session_maker() as session:
        hotel = await HotelRepository(session).add(hotel_data)
        # print(add_hotel_stnt.compile(engine, compile_kwargs={"literal_binds": True}))  # debug
        await session.commit()

        return {'status': 'ok', "data": hotel}


@router.delete('/{hotel_id}/')
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelRepository(session).delete_by(id=hotel_id)
        await session.commit()
    return {'status': 'ok'}


@router.put('/{hotel_id}')
async def change_hotel(
        hotel_id: int,
        hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
        return {'status': 'ok'}


@router.patch('/{hotel_id}', summary='Частичное редактирование данных отеля',
              description='Описывает что делает функция в АПИ')
def pat_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if hotel_data.title is not None:
                hotel['title'] = hotel_data.title
            if hotel_data.name is not None:
                hotel['name'] = hotel_data.name
        return {'status': 'ok'}
