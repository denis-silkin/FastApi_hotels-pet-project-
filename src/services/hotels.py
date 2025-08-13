from datetime import date

from src.exeptions import check_date_to_after_date_from, ObjectNotFoundException, HotelNotFoundException
from src.schemas.hotels import HotelAdd, Hotel
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_filtered_by_time(
            self,
            pagination,
            location: str | None,
            title: str | None,
            date_from: date,
            date_to: date,
    ):
        check_date_to_after_date_from(date_from, date_to)
        page_size = pagination.page_size or 5
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=page_size,
            offset=page_size * (pagination.page - 1),
        )

    async def get_hotels_one(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def add_hotel(self, data: HotelAdd):
        hotel = await self.db.hotels.add(data)
        await self.db.commit()
        return hotel

    async def get_hotel_with_check(self, hotel_id: int, ) -> Hotel:
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
