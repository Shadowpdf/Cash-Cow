
from app.database import AsyncSessionLocal
from app.models import Technician, ServiceCall, ATM
from app.schemas.technician import ActiveCallTechnicianRead, ColocationDiscrepanciesRead, TECHNICIANSRead

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db

router = APIRouter(prefix= "/technicians", tags = ["Technicians"])

@router.get("/", response_model=list[TECHNICIANSRead])
async def list_technicians(db: AsyncSession = Depends(get_db)) -> list[Technician]:
    statement = (
        select(Technician).order_by(Technician.id)
    )

    results = await db.execute(statement)

    return list(results.scalars().all())

@router.get("/co-location-discrepancies", response_model=list[ColocationDiscrepanciesRead])
async def list_colocation_discrepancies(db: AsyncSession = Depends(get_db)):
    statement = (
        select(
            ServiceCall.id.label("service_call_id"),
            ATM.id.label("atm_id"),
            Technician.id.label("technician_id"),
            Technician.facility_id.label("technician_branch_id")
        )
        .join(ATM, ServiceCall.atm_id == ATM.id)
        .join(Technician, ServiceCall.technician_id == Technician.id)
        .where(Technician.facility_id != ATM.facility_id)
        .order_by(ServiceCall.id)
    )

    result = await db.execute(statement)
    return [dict(row) for row in result.mappings().all()]

@router.get("/active-call-technician/{supervisor_id}", response_model=list[ActiveCallTechnicianRead])
async def list_active_call_technician(supervisor_id: int ,db: AsyncSession = Depends(get_db)):
    statement = (
        select(
            Technician.id.label("technician_id"),
            Technician.name.label("technician_name"),
            Technician.supervisor_id.label("supervisor_id"),
            ServiceCall.id.label("service_call_id"),
            ServiceCall.status.label("service_call_status")
        )
        .join(ServiceCall, Technician.id == ServiceCall.technician_id)
        .where((ServiceCall.status.in_(["In-Progress", "Pending"])))
        .where(Technician.supervisor_id == supervisor_id)
    )

    result = await db.execute(statement)
    return [dict(row) for row in result.mappings().all()]
