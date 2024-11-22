from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from bot.src.database.models import User


async def orm_add_user(session:AsyncSession, data:dict):
    obj = User(
        id=data['id'],
        name=data["name"],
        isAdmin=data['isAdmin']
    )
    session.add(obj)
    await session.commit()
    return obj


async def orm_get_users(session: AsyncSession):
    query = select(User)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_delete_user(session: AsyncSession, user_id: int):
    query = delete(User).where(User.id == user_id)
    await session.execute(query)
    await session.commit()


# async def orm_get_product(session: AsyncSession, product_id: int):
#     query = select(Product).where(Product.id == product_id)
#     result = await session.execute(query)
#     return result.scalar()


# async def orm_update_product(session: AsyncSession, product_id: int, data):
#     query = update(Product).where(Product.id == product_id).values(
#         name=data["name"],
#         description=data["description"],
#         price=float(data["price"]),
#         image=data["image"],)
#     await session.execute(query)
#     await session.commit()


