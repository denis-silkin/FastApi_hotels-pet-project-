from models.bookings import BookingsOrm
from repositories.base import BaseRepository
from repositories.mappers.mappers import BookingDataMapper
from schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper
