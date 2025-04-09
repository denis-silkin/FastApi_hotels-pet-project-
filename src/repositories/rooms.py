from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from repositories.base import BaseRepository
from models.rooms import RoomsOrm
from repositories.mappers.mappers import RoomDataMapper, RoomDataWithRelsMapper
from repositories.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date,
    ):
        """
        with rooms_count as (
	        select room_id, count(*) as rooms_booked from bookings
	        where date_from <= '2025-03-19' and date_to >= '2025-03-05'
	        group by room_id
        ),
        rooms_left_table as (
	        select rooms.id as room_id, quantity - coalesce(rooms_booked, 0) as rooms_left
	        from rooms
	        left join rooms_count on rooms.id = rooms_count.room_id
        )
        select * from rooms_left_table
        where rooms_left > 0;
        """
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)

        # print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        return [RoomDataWithRelsMapper.map_to_domain_entity(model) for model in result.unique().scalars().all()]

    async def get_one_or_none_with_rels(self, **filter_by):

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by))
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return RoomDataWithRelsMapper.map_to_domain_entity(model)
