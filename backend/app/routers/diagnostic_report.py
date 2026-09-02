"""

"""

from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import DiagnosticReport
from app.schemas.diagnostic_report import DIAGNOSTICREPORTRead

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db

router = APIRouter(prefix = "/diagnostic_report", tags = ["Diagonostic Reports"])

@router.get("/", response_model=list[DIAGNOSTICREPORTRead])
async def list_atms(db: AsyncSession = Depends(get_db)) -> list[DiagnosticReport]:
    statement = (
        select(DiagnosticReport).order_by(DiagnosticReport.id)
    )

    result = await db.execute(statement)

    return list(result.scalars().all())