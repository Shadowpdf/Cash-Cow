"""

English translation

Import Python's environment-variable tools.

Import SQLAlchemy's async database tools.

Find DATABASE_URL from the computer's environment.
If it isn't there, use our local development database URL.

Using that URL, create one async SQLAlchemy engine.
Print generated SQL while we're learning.

Create a reusable factory that produces async sessions
connected through that engine.

Don't wipe ORM object values after committing changes.

"""


import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

#Setting the DB URL with the cashcow database
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/cashcow_dev",

)

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)