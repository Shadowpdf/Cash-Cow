from pydantic import BaseModel, ConfigDict

from app.models import ATM, Technician, ServiceCall
from app.models.enums import ServiceStatus


class TECHNICIANSRead(BaseModel):

    id: int
    name: str
    facility_id: int
    supervisor_id: int

    model_config = ConfigDict(from_attributes=True)

class ColocationDiscrepanciesRead(BaseModel):
    service_call_id: int
    atm_id: int
    technician_id: int
    technician_branch_id: int

    model_config = ConfigDict(from_attributes=True)

class ActiveCallTechnicianRead(BaseModel):
    technician_id: int
    technician_name: str
    supervisor_id: int
    service_call_id: int
    service_call_status: ServiceStatus

    model_config = ConfigDict(from_attributes=True)