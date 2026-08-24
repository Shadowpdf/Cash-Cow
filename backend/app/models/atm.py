from .base import Base
from typing import TYPE_CHECKING

from enums import ATMStatus
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ATM(Base):

    __tablename__ = "atms"

    id: Mapped[int] = mapped_column(primary_key=True)
    serial_number: Mapped[String] = mapped_column(String(100), unique=True)
    model: Mapped[String] = mapped_column(String(50))
    status: Mapped[ATMStatus] = mapped_column(
        SqlEnum(
            ATMStatus,
            name="atm_status",
            values_callable=lambda enum_cls: [member.value for member in enum_cls]
        ),

    )
    cash_level: Mapped[int] = mapped_column(Integer)
    facility_id: Mapped[int] = mapped_column(Integer, ForeignKey("branches.id"))