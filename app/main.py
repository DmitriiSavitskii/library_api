# from database import async_engine, Base
# import asyncio
# from models.books import Book
# from models.readers import Reader
# from models.borrows import Borrow
# from models.users import User


# async def create_tables():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         # await conn.run_sync(Base.metadata.create_all)

# asyncio.run(create_tables())