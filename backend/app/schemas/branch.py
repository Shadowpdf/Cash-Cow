from pydantic import BaseModel, ConfigDict


class BranchRead(BaseModel):
    id: int
    name: str
    location_region: str
    capacity: int
    supervisor_id: int

    model_config = ConfigDict(from_attributes=True)

class BranchMaintenanceRisk(BaseModel):
    branch_id: int
    branch_name: str
    total_atms: int
    maintenance_atms: int
    maintenance_percentage: float

    model_config = ConfigDict(from_attributes=True)