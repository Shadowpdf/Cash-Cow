from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import ServiceCall
from app.schemas.service_call import SERVICECALLRead

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db

router = APIRouter(prefix= "/service-call", tags= ["ServiceCalls"])

@router.get("/", response_model=list[SERVICECALLRead])
async def list_service_calls(db: AsyncSession = Depends(get_db)) -> list[ServiceCall]:
    statement = (
        select(ServiceCall).order_by(ServiceCall.id)
    )

    result = await db.execute(statement)

    return list(result.scalars().all())
    