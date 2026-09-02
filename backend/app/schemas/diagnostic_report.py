from pydantic import BaseModel, ConfigDict
from datetime import datetime


class DIAGNOSTICREPORTRead(BaseModel):

    id: int
    service_call_id: int
    file_url: str
    notes: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
