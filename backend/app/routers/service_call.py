from sqlalchemy import case, func, select

from app.database import AsyncSessionLocal
from app.models import ServiceCall
from app.schemas.service_call import SERVICECALLRead, ServiceReliabilityRead

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models.atm import ATM

router = APIRouter(prefix= "/service-call", tags= ["ServiceCalls"])

@router.get("/", response_model=list[SERVICECALLRead])
async def list_service_calls(db: AsyncSession = Depends(get_db)) -> list[ServiceCall]:
    statement = (
        select(ServiceCall).order_by(ServiceCall.id)
    )

    result = await db.execute(statement)

    return list(result.scalars().all())

@router.get("/service-reliability", response_model=list[ServiceReliabilityRead])
async def service_calls_reliability(db: AsyncSession = Depends(get_db)):

    completed_calls = func.sum(case((ServiceCall.status == "Completed", 1), else_=0))
    failed_calls = func.sum(case((ServiceCall.status == "Failed", 1), else_=0))
    total_calls = completed_calls + failed_calls
    completion_ratio = (completed_calls * 100.0 / total_calls)
    statement = (
        select(
            ATM.model.label("model"),
            total_calls.label("total_calls"),
            completed_calls.label("completed_calls"),
            failed_calls.label("failed_calls"),
            completion_ratio.label("completion_ratio")
        )
        .join(ServiceCall, ATM.id == ServiceCall.atm_id)
        .group_by(ATM.model)
    )

    result = await db.execute(statement)
    return [dict(row) for row in result.mappings().all()]



    