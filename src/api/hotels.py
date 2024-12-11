from fastapi import Query, APIRouter, Body
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep


router = APIRouter(prefix='/hotels', tags=['Отели'])


hotels = [
    {'id': 1, 'title': 'Sochi', 'name': 'sochi'},
    {'id': 2, 'title': 'Dubai', 'name': 'dubai'},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get('')
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description='ID отеля'),
        title: str | None = Query(None, description='Название отеля'),
        name: str | None = Query(None, description='Имя отеля'),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        if name and hotel['name'] != name:
            continue
        hotels_.append(hotel)

    if pagination.page and pagination.page_size:
        return hotels_[pagination.page_size * (pagination.page-1):][:pagination.page_size]
    return hotels_


# body, request body
@router.post('')
def create_hotel(
        hotel_data: Hotel = Body(openapi_examples={
            '1': {'summary': 'Сочи', 'value':{
                'title': "Отель Сочи 5 звезд у моря",
                'name': 'sochi_u_morya'}},
            '2': {'summary': 'Дубай', 'value':{
                'title': "Отель Дубай у фонтана",
                'name': 'dubai_fountain'}},
        })):
    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': hotel_data.title,
        'name': hotel_data.name,
    })
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
