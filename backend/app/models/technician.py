"""

"""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .base import Base


class Technician(Base):

    __tablename__ = "technicians"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    facility_id: Mapped[int] = mapped_column(Integer, ForeignKey("branches.id"))
    supervisor_id: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
            return (f"Technician-ID(id={self.id}, name={self.name!r}, "
                    f"Branch-ID={self.facility_id}, Supervisor-ID={self.supervisor_id})")