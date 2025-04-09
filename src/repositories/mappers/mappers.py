from models.bookings import BookingsOrm
from models.facilities import FacilitiesOrm
from models.hotels import HotelsOrm
from models.rooms import RoomsOrm
from models.users import UsersOrm
from repositories.mappers.base import DataMapper
from schemas.bookings import Booking
from schemas.facilities import Facility
from schemas.hotels import Hotel
from schemas.rooms import Room, RoomWithRels
from schemas.users import User


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Room


class RoomDataWithRelsMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomWithRels


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User


class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Booking


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facility
