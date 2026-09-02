from pydantic import BaseModel, ConfigDict


class BranchRead(BaseModel):
    id: int
    name: str
    location_region: str
    capacity: int
    supervisor_id: int

    model_config = ConfigDict(from_attributes=True)