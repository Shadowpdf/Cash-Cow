"""

"""


import asyncio

from sqlalchemy import select, text

from app.database import AsyncSessionLocal


# async def test_db(session):

#     statement = (
#         select(1)
#     )

#     results = await session.execute(statement)

    

async def main() -> None:
    async with AsyncSessionLocal() as session:

        test_stmt = select(text("1"))

        results = await session.execute(test_stmt)

        for result in results.scalars():
            print(f"Test-Output: {result!r}")




if __name__ == "__main__":
    asyncio.run(main())
