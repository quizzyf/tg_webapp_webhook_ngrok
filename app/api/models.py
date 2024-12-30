from sqlalchemy import String, BigInteger, Integer, Date, Time, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class User(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)  # Уникальный идентификатор пользователя в Telegram
    first_name: Mapped[str] = mapped_column(String, nullable=False)  # Имя пользователя
    username: Mapped[str] = mapped_column(String, nullable=True)  # Telegram username
    number: Mapped[int] = mapped_column(BigInteger, nullable=True)
    basket: Mapped[str] = mapped_column(String, nullable=True)
    orders_ids: Mapped[str] = mapped_column(String, nullable=True)



class Product(Base):
    __tablename__ = 'products'  # Название таблицы должно быть в нижнем регистре

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # Уникальный идентификатор продукта
    name: Mapped[str] = mapped_column(String, nullable=False)  # Название продукта
    cost: Mapped[int] = mapped_column(Integer, nullable=False)  # Цена
    description: Mapped[str] = mapped_column(String, nullable=False)  # Описание
    image: Mapped[str] = mapped_column(String, nullable=False)  # Путь к изображению
    type_product: Mapped[str] = mapped_column(String, nullable=True)  # Тип продукта


class Order(Base):
    __tablename__ = 'orders'  # Название таблицы должно быть в нижнем регистре

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # Уникальный идентификатор заявки
    user_id: Mapped[int] = mapped_column(BigInteger)  # Внешний ключ на пользователя
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    client_name: Mapped[str] = mapped_column(String, nullable=False)  # Имя клиента
    products_list: Mapped[str] = mapped_column(String, nullable=False)
