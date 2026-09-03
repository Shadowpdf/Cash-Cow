from decimal import Decimal

from pydantic import BaseModel, ConfigDict
from app.models.enums import ServicePriority
from app.models.enums import ServiceStatus


class SERVICECALLRead(BaseModel):
    id: int
    title: str

    priority: ServicePriority

    status: ServiceStatus

    atm_id: int
    technician_id: int

    model_config = ConfigDict(from_attributes=True)

class ServiceReliabilityRead(BaseModel):
    model: str 
    total_calls: int
    completed_calls: int
    failed_calls: int 
    completion_ratio: Decimal

    model_config = ConfigDict(from_attributes=True)

