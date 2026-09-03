"""

"""
from sqlalchemy import case, func, select

from app.database import AsyncSessionLocal
from app.models import Branch
from app.schemas.branch import BranchMaintenanceRisk, BranchRead

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models.enums import AtmStatus
from app.models.atm import ATM
router = APIRouter(prefix = "/branches", tags=["Branches"])

@router.get("/", response_model=list[BranchRead])
async def list_branches(db: AsyncSession = Depends(get_db)) -> list[Branch]:
    statement = (
        select(Branch).order_by(Branch.id)
    )

    result = await db.execute(statement)
    return list(result.scalars().all())

@router.get("/maintenance-risk", response_model=list[BranchMaintenanceRisk])
async def maintenance_risk(db: AsyncSession = Depends(get_db)):
    total_atms = func.count(ATM.id)
    maintenance_atms = func.sum(case((ATM.status == AtmStatus.MAINTENANCE, 1), else_=0))
    maintenance_percentage = ( maintenance_atms * 100.0 / total_atms)
    
    statement = (
        select(
            Branch.id.label("branch_id"),
            Branch.name.label("branch_name"),
            total_atms.label("total_atms"),
            maintenance_atms.label("maintenance_atms"),
            maintenance_percentage.label("maintenance_percentage"),
        )
        .join(ATM, Branch.id == ATM.facility_id)
        .group_by(Branch.id, Branch.name)
        .having(maintenance_percentage > 30)
        .order_by(Branch.id)
    )
    result = await db.execute(statement)
    return [dict(row) for row in result.mappings().all()]

