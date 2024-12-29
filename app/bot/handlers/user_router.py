from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from app.api.dao import UserDAO, OrderDAO
from app.bot.keyboards.kbs import app_keyboard
from app.bot.utils import *

user_router = Router()


@user_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """
    Обрабатывает команду /start.
    """
    user = await UserDAO.find_one_or_none(telegram_id=message.from_user.id)

    if not user:
        await UserDAO.add(
            telegram_id=message.from_user.id,
            first_name=message.from_user.first_name,
            username=message.from_user.username
        )

    await greet_user(message, is_new_user=not user)


@user_router.message(F.text == '🔙 Назад')
async def cmd_back_home(message: Message) -> None:
    """
    Обрабатывает нажатие кнопки "Назад".
    """
    await greet_user(message, is_new_user=False)


@user_router.message(F.text == "ℹ️ О нас")
async def about_us(message: Message):
    kb = app_keyboard(user_id=message.from_user.id, first_name=message.from_user.first_name)
    await message.answer(get_about_us_text(), reply_markup=kb)


@user_router.callback_query(F.data == "new_order")
async def about_us(callback: CallbackQuery):
    cart = await UserDAO.get_cart(callback.from_user.id)
    await OrderDAO.add(
        user_id=callback.from_user.id,
        completed=False,
        client_name=callback.from_user.first_name,
        products_list=cart,
    )
    await UserDAO.clear_cart(callback.from_user.id)
    await callback.message.edit_text(new_order())


@user_router.callback_query(F.data == "canc_order")
async def about_us(callback: CallbackQuery):
    await callback.message.edit_text(canc_order())