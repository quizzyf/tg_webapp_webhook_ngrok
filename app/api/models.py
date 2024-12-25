from sqlalchemy import String, BigInteger, Integer, Date, Time, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class OrderProduct(Base):
    __tablename__ = 'order_products'

    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('orders.id'), primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'), primary_key=True)

    # Связь с Order и Product
    order: Mapped["Order"] = relationship("Order", back_populates="order_products")
    product: Mapped["Product"] = relationship("Product", back_populates="order_products")


class User(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)  # Уникальный идентификатор пользователя в Telegram
    first_name: Mapped[str] = mapped_column(String, nullable=False)  # Имя пользователя
    username: Mapped[str] = mapped_column(String, nullable=True)  # Telegram username
    basket: Mapped[str] = mapped_column(String, nullable=True)

    # Связь с заявками
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")


class Product(Base):
    __tablename__ = 'products'  # Название таблицы должно быть в нижнем регистре

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # Уникальный идентификатор продукта
    name: Mapped[str] = mapped_column(String, nullable=False)  # Название продукта
    cost: Mapped[int] = mapped_column(Integer, nullable=False)  # Цена
    description: Mapped[str] = mapped_column(String, nullable=False)  # Описание
    image: Mapped[str] = mapped_column(String, nullable=False)  # Путь к изображению
    type_product: Mapped[str] = mapped_column(String, nullable=True)  # Тип продукта

    # Связь с заказами через OrderProduct
    order_products: Mapped[list["OrderProduct"]] = relationship("OrderProduct", back_populates="product")


class Order(Base):
    __tablename__ = 'orders'  # Название таблицы должно быть в нижнем регистре

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # Уникальный идентификатор заявки
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.telegram_id'))  # Внешний ключ на пользователя
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    appointment_date: Mapped[Date] = mapped_column(Date, nullable=False)  # Дата заявки
    appointment_time: Mapped[Time] = mapped_column(Time, nullable=False)  # Время заявки
    client_name: Mapped[str] = mapped_column(String, nullable=False)  # Имя клиента

    # Связи с пользователем и продуктами через OrderProduct
    user: Mapped["User"] = relationship("User", back_populates="orders")
    order_products: Mapped[list["OrderProduct"]] = relationship("OrderProduct", back_populates="order")