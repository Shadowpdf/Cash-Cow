"""

"""
from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import Branch
from app.schemas.branch import BranchRead

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db

router = APIRouter(prefix = "/branches", tags=["Branches"])

@router.get("/", response_model=list[BranchRead])
async def list_branches(db: AsyncSession = Depends(get_db)) -> list[Branch]:
    statement = (
        select(Branch).order_by(Branch.id)
    )

    result = await db.execute(statement)
    return list(result.scalars().all())