from pydantic import BaseModel, ConfigDict


class TECHNICIANSRead(BaseModel):

    id: int
    name: str
    facility_id: int
    supervisor_id: int

    model_config = ConfigDict(from_attributes=True)