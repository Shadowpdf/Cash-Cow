"""

"""


from .base import Base
from typing import TYPE_CHECKING

from .enums import ServiceStatus, ServicePriority
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ServiceCall(Base):

    __tablename__ = "service_calls"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    priority: Mapped[ServicePriority] = mapped_column(
        SqlEnum(
            ServicePriority,
            name="service_priority",
            values_callable=lambda enum_cls: [member.value for member in enum_cls]
        ),
    ) 

    status: Mapped[ServiceStatus] = mapped_column(
        SqlEnum(
            ServiceStatus,
            name="service_status",
            values_callable=lambda enum_cls: [member.value for member in enum_cls]
        ),
    )

    atm_id: Mapped[int] = mapped_column(Integer, ForeignKey("atms.id"))
    technician_id: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
            return (f"ServiceCall-ID(id={self.id}, name={self.title!r}, "
                    f"Priority={self.priority.value}, ServiceCallStatus={self.status.value}, ATM-ID={self.atm_id},"
                    f"Technician_id={self.technician_id})")