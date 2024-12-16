from fastapi import Query, APIRouter, Body
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from sqlalchemy import insert, select, or_
from src.models.hotels import HotelsOrm

router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get('')
async def get_hotels(
        pagination: PaginationDep,
        # id: int | None = Query(None, description='ID отеля'),
        location: int | None = Query(None, description='Отель'),
        title: str | None = Query(None, description='Название отеля'),
):
    per_page = pagination.page_size or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if location:
            query = query.filter(or_(location == 'Сочи', location == 'Дубай'))
        if title:
            query = query.filter(or_(title == 'Сочи', title == 'Дубай'))
        query = (
            query
            .limit(per_page)
            .offset(per_page * (per_page - 1))
                 )
        result = await session.execute(query)

        hotels = result.scalars().all()
        # print(type(hotels), hotels)
        return hotels

    # if pagination.page and pagination.page_size:
    #     return hotels_[pagination.page_size * (pagination.page-1):][:pagination.page_size]


# body, request body
@router.post('')
async def create_hotel(
        hotel_data: Hotel = Body(openapi_examples={
            '1': {'summary': 'Сочи', 'value': {
                'title': "Отель Сочи 5 звезд у моря",
                'location': 'ул. Моря, 1'}},
            '2': {'summary': 'Дубай', 'value': {
                'title': "Отель Дубай у фонтана",
                'location': 'ул. Моря, 2'}},
        })):
    async with async_session_maker() as session:
        add_hotel_stnt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stnt.compile(engine, compile_kwargs={"literal_binds": True}))  # debug
        await session.execute(add_hotel_stnt)
        await session.commit()

    return {'status': 'ok'}


@router.delete('/{hotel_id}/')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'ok'}


@router.put('/{hotel_id}')
def change_hotel(
        hotel_id: int,
        hotel_data: Hotel

):
    global hotels
    # hotel = [hotel for hotel in hotels if hotel['id'] == hotel_id][0]
    # hotel['title'] = title
    # hotel['name'] = name
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'] = hotel_data.title
            hotel['name'] = hotel_data.name
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
