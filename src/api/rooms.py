from fastapi import APIRouter, Query, Body

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import Rooms

router = APIRouter(prefix='/hotels', tags=['Номера'])


@router.get("")
async def get_rooms(
        hotel_id: str | None = Query(None, description='Отель'),
        title: str | None = Query(None, description='Номер'),
        description: str | None = Query(None, description='Описание номера'),
        price: int | None = Query(None, description='Цена'),
        quantity: int | None = Query(None, description='Количество'),
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            hotel_id=hotel_id,
            title=title,
            description=description,
            price=price,
            quantity=quantity,
        )


@router.get("/{rooms_id}", summary="получение одного номера")
async def get_rooms_one(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=hotel_id)


@router.post('')
async def create_rooms(
        hotel_data: Rooms = Body(openapi_examples={
            '1': {'summary': 'Сочи', 'value': {
                'title': "Отель Сочи 5 звезд у моря",
                'location': 'ул. Моря, 1',
                'description': 'Одноместный номер',
                'price': '3000 руб.',
                'quantity': '15'
                  }},
            '2': {'summary': 'Дубай', 'value': {
                'title': "Отель Дубай у фонтана",
                'location': 'ул. Шейха, 2',
                'description': 'Двухместный номер',
                'price': '5000 руб.',
                'quantity': '9'
            }},
        })):
    async with async_session_maker() as session:
        rooms = await RoomsRepository(session).add(hotel_data)
        # print(add_hotel_stnt.compile(engine, compile_kwargs={"literal_binds": True}))  # debug
        await session.commit()

        return {'status': 'ok', "data": rooms}


@router.delete('/{hotel_id}/')
async def delete_rooms(hotel_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete_by(id=hotel_id)
        await session.commit()
    return {'status': 'ok'}


@router.put('/{hotel_id}')
async def change_rooms(
        hotel_id: int,
        rooms_data: Rooms):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(rooms_data, id=hotel_id)
        await session.commit()
        return {'status': 'ok'}


# @router.patch('/{hotel_id}', summary='Частичное редактирование данных номера',
#               description='Описывает что делает функция в АПИ')
# def pat_rooms(
#         hotel_id: int,
#         rooms_data: HotelPATCH,
# ):
#     global hotels
#     for hotel in hotels:
#         if hotel['id'] == hotel_id:
#             if rooms_data.title is not None:
#                 hotel['title'] = hotel_data.title
#             if rooms_data.name is not None:
#                 hotel['name'] = hotel_data.name
#         return {'status': 'ok'}

