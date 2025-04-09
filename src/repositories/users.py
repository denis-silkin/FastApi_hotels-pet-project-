from pydantic import EmailStr
from sqlalchemy import select

from repositories.base import BaseRepository
from models.users import UsersOrm
from repositories.mappers.mappers import UserDataMapper
from schemas.users import User, UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPassword.model_validate(model)

