from fastapi import APIRouter, Body

from api.dependencies import DBDep
from schemas.facilities import FacilityAdd

router = APIRouter(prefix='/facilities', tags=['Удобства'])


@router.get("")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("")
async def create_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "ok", "data": facility}
