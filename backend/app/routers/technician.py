
from app.database import AsyncSessionLocal
from app.models import Technician
from app.schemas.technician import TECHNICIANSRead

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