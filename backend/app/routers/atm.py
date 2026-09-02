"""

"""
from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import ATM
from app.schemas.atm import ATMRead

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db


router = APIRouter(prefix = "/atms", tags = ["ATMs"])

@router.get("/", response_model=list[ATMRead])
async def list_atms(db: AsyncSession = Depends(get_db)) -> list[ATM]:
    statement = (
        select(ATM).order_by(ATM.id)
    )

    result = await db.execute(statement)

    return list(result.scalars().all())

@router.get("/low-cash", response_model=list[ATMRead])
async def low_cash_atms(db: AsyncSession = Depends(get_db)) -> list[ATM]:
    statement = (
        select(ATM).where(ATM.cash_level < 20.0).order_by(ATM.id)
    )

    result = await db.execute(statement)

    return list(result.scalars().all())