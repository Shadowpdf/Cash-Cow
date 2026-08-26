"""


"""
from .base import Base
from typing import TYPE_CHECKING
from datetime import datetime

from .enums import ServiceStatus, ServicePriority
from sqlalchemy import Enum as SqlEnum, Text, func
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class DiagnosticReport(Base):

    __tablename__ = "diagnostic_reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_call_id: Mapped[int] = mapped_column(Integer, ForeignKey("service_calls.id"))
    file_url: Mapped[str] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    
    def __repr__(self) -> str:
        return (f"DiagnosticReport(id={self.id}, service_call_id={self.service_call_id}, "
                f"file_url={self.file_url!r})")