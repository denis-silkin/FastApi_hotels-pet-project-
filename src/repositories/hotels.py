from datetime import date

from models.rooms import RoomsOrm
from repositories.base import BaseRepository
from models.hotels import HotelsOrm
from sqlalchemy import select, func
from database import engine
from repositories.mappers.mappers import HotelDataMapper
from repositories.utils import rooms_ids_for_booking
from schemas.hotels import Hotel


class HotelRepository(BaseRepository):
    model = HotelsOrm
    mapper = HotelDataMapper

        # print(query.compile(engine, compile_kwargs={'literal_binds': True}))

    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            location,
            title,
            limit,
            offset,
    ) -> list[Hotel]:
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotels_ids_to_get))
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()]
