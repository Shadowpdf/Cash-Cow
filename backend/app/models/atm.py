from decimal import Decimal

from .base import Base
from typing import TYPE_CHECKING

from .enums import AtmStatus
from sqlalchemy import Enum as SqlEnum, Numeric
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ATM(Base):

    __tablename__ = "atms"

    id: Mapped[int] = mapped_column(primary_key=True)
    serial_number: Mapped[str] = mapped_column(String(100), unique=True)
    model: Mapped[str] = mapped_column(String(50))
    status: Mapped[AtmStatus] = mapped_column(
        SqlEnum(
            AtmStatus,
            name="atm_status",
            values_callable=lambda enum_cls: [member.value for member in enum_cls]
        ),

    )
    cash_level: Mapped[Decimal] = mapped_column(Numeric(5,2))
    facility_id: Mapped[int] = mapped_column(Integer, ForeignKey("branches.id"))


    def __repr__(self) -> str:
            return (f"ATM-ID(id={self.id}, serial-number={self.serial_number!r}, "
                    f"ATM-Status={self.status.value}, cash_level={self.cash_level}%, branch-id={self.facility_id})")