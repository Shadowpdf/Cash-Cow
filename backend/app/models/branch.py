"""


"""


from __future__ import annotations

from .base import Base

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Branch(Base):
    __tablename__ = "branches"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    location_region: Mapped[str] = mapped_column(String(50))
    capacity: Mapped[int] = mapped_column(Integer)
    supervisor_id: Mapped[int] = mapped_column(Integer)


    def __repr__(self) -> str:
        return (f"Branch-ID(id={self.id}, name={self.name!r}, "
                f"Location={self.location_region!r})")

