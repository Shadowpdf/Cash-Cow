from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.enums import AtmStatus


class ATMRead(BaseModel):

    id: int
    serial_number: str
    model: str
    status: AtmStatus
    cash_level: Decimal
    facility_id: int

    model_config = ConfigDict(from_attributes=True)