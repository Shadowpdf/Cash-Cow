"""
Creates all tables registered with Base metadata.

Importing app.models loads the ORM models that inherit from Base,
allowing SQLAlchemy to create their tables in the database.
"""

import asyncio

from app.database import engine
from app.models import Base

async def create_tables() -> None:
    async with engine.begin() as conn:

        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())