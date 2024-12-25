from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.functions import current_user

from app.dao.base import BaseDAO
from app.api.models import User, Product, Order
from app.database import async_session_maker


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def add_product_basket(cls, id_user: int, id_product: int):
        async with async_session_maker() as session:
            try:
                user = await UserDAO.find_one_or_none(telegram_id=id_user)
                if user is None:
                    raise SQLAlchemyError
                bask = user.basket
                if bask is None:
                    current_basket = []
                else:
                    current_basket = bask.split(',')
                if current_basket:
                    for i in range(len(current_basket)):
                        pr = current_basket[i].split('#')
                        if int(pr[0]) == id_product:
                            current_basket[i] = pr[0] + '#' + str(int(pr[1]) + 1)
                            break
                    else:
                        current_basket.append(f'{str(id_product)}#1')
                user.basket = ','.join(current_basket)
                session.add(user)
                await session.commit()

            except SQLAlchemyError as e:
                await session.rollback()
                raise e

    @classmethod
    async def delete_product_basket(cls, id_user: int, id_product: int):
        async with async_session_maker() as session:
            try:
                user = await UserDAO.find_one_or_none(telegram_id=id_user)
                if user is None:
                    raise SQLAlchemyError
                bask = user.basket
                current_basket = bask.split(',')
                for i in range(len(current_basket)):
                    pr = current_basket[i].split('#')
                    if int(pr[0]) == id_product and int(pr[1]) > 1:
                        current_basket[i] = pr[0] + '#' + str(int(pr[1]) - 1)
                        break
                    elif int(pr[0]) == id_product and int(pr[1]) == 1:
                        current_basket.pop(i)
                        break
                user.basket = ','.join(current_basket)
                session.add(user)
                await session.commit()

            except SQLAlchemyError as e:
                await session.rollback()
                raise e

    @classmethod
    async def get_cart(cls, id_user: int):
        async with async_session_maker() as session:
            try:
                user = await UserDAO.find_one_or_none(telegram_id=id_user)
                if user is None:
                    raise SQLAlchemyError
                bask = user.basket
                if bask is None:
                    return []
                else:
                    return bask
            except SQLAlchemyError as e:
                await session.rollback()
                raise e


class ProductDAO(BaseDAO):
    model = Product


class OrderDAO(BaseDAO):
    model = Order

    @classmethod
    async def get_applications_by_user(cls, user_id: int):
        """
        Возвращает все заявки пользователя по user_id с дополнительной информацией
        о мастере и услуге.

        Аргументы:
            user_id: Идентификатор пользователя.

        Возвращает:
            Список заявок пользователя с именами мастеров и услуг.
        """
        async with async_session_maker() as session:
            try:
                # Используем joinedload для ленивой загрузки связанных объектов
                query = (
                    select(cls.model)
                    .options(joinedload(cls.model.completed), joinedload(cls.model.client_name))
                    .filter_by(user_id=user_id)
                )
                result = await session.execute(query)
                applications = result.scalars().all()

                # Возвращаем список словарей с нужными полями
                return [
                    {
                        "application_id": app.id,
                        "user_id": app.user_id,
                        "completed": app.completed,
                        "appointment_date": app.appointment_date,
                        "appointment_time": app.appointment_time,
                        "client_name": app.client_name,
                    }
                    for app in applications
                ]
            except SQLAlchemyError as e:
                print(f"Error while fetching applications for user {user_id}: {e}")
                return None

    @classmethod
    async def get_all_applications(cls):
        """
        Возвращает все заявки в базе данных с дополнительной информацией о мастере и услуге.

        Возвращает:
            Список всех заявок с именами мастеров и услуг.
        """
        async with async_session_maker() as session:
            try:
                # Используем joinedload для загрузки связанных данных
                query = (
                    select(cls.model)
                    .options(joinedload(cls.model.completed), joinedload(cls.model.client_name))
                )
                result = await session.execute(query)
                applications = result.scalars().all()

                # Возвращаем список словарей с нужными полями
                return [
                    {
                        "application_id": app.id,
                        "user_id": app.user_id,
                        "completed": app.completed,  # Имя мастера
                        "appointment_date": app.appointment_date,
                        "appointment_time": app.appointment_time,
                        "client_name": app.client_name,  # Имя клиента
                    }
                    for app in applications
                ]
            except SQLAlchemyError as e:
                print(f"Error while fetching all applications: {e}")
                return None