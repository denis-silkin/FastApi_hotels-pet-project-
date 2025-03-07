from pydantic import BaseModel, ConfigDict, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str


class UsersAdd(BaseModel):
    email: EmailStr
    hashed_password: str


class User(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
