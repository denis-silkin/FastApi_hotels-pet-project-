from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.database import engine


class RoomsRepository(BaseRepository):
    model = RoomsOrm

    async def get_all(self,
                      hotel_id,
                      title,
                      description,
                      price,
                      quantity,
                      ):
        query = select(RoomsOrm)
        if hotel_id:
            query = query.filter(func.lower(RoomsOrm.hotel_id).contains(hotel_id.strip().lower()))
        if title:
            query = query.filter(func.lower(RoomsOrm.title).contains(title.strip().lower()))
        if description:
            query = query.filter(func.lower(RoomsOrm.description).contains(title.strip().lower()))
        if price:
            query = query.filter(func.lower(RoomsOrm.price).contains(title.strip().lower()))
        if quantity:
            query = query.filter(func.lower(RoomsOrm.quantity).contains(title.strip().lower()))

        print(query.compile(engine, compile_kwargs={'literal_binds': True}))
        result = await self.session.execute(query)

        return result.scalars().all()
