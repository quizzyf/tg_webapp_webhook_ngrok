import logging
import re

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from app.api.dao import UserDAO, OrderDAO
from app.bot.keyboards.kbs import app_keyboard
from app.bot.utils import *
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext

user_router = Router()


def format_russian_phone_number(phone):
    # Удаляем все символы, кроме цифр
    cleaned = re.sub(r'\D', '', phone)

    # Проверяем, является ли номер российским
    if len(cleaned) == 10:
        # Если номер состоит из 10 цифр, добавляем код страны
        return f'+7{cleaned}'
    elif len(cleaned) == 11 and cleaned.startswith('7'):
        # Если номер состоит из 11 цифр и начинается с 7, добавляем код страны
        return f'+{cleaned}'
    elif len(cleaned) == 11 and cleaned.startswith('8'):
        # Если номер состоит из 11 цифр и начинается с 8, заменяем 8 на 7
        return f'+7{cleaned[1:]}'
    else:
        # Если номер не соответствует формату, возвращаем None или сообщение об ошибке
        return None


class Form(state.StatesGroup):
    number_user = state.State()
    number_user_not_ord = state.State()


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

    await greet_user(message)


@user_router.message(F.text == '📋 Главное меню')
async def cmd_main_menu(message: Message) -> None:
    """
    Обрабатывает нажатие кнопки "Назад".
    """
    await main_mail(message)


@user_router.message(F.text == '⚙️ Настройки профиля')
async def cmd_settings(message: Message) -> None:
    """
    Обрабатывает нажатие кнопки "Назад".
    """
    await settings(message)


@user_router.callback_query(F.data == "about_us")
async def about_us(callback: CallbackQuery):

    await get_about_us_text(callback)


@user_router.callback_query(F.data == "new_order")
async def make_order(callback: CallbackQuery, state: FSMContext):
    user = await UserDAO.find_one_or_none(telegram_id=callback.from_user.id)
    logging.info(user.number if user else 'Пользователь не найден')
    if user and user.number:
        cart = await UserDAO.get_cart(callback.from_user.id)
        await OrderDAO.add(
            user_id=callback.from_user.id,
            completed=False,
            client_name=callback.from_user.first_name,
            products_list=cart,
        )
        await UserDAO.clear_cart(callback.from_user.id)
        await callback.message.edit_text(new_order())
    else:
        await callback.answer("Пожалуйста, введите номер телефона. 🔢")
        await state.set_state(Form.number_user)
        await callback.message.answer("Введите ваш номер телефона, пожалуйста. 🔢")


@user_router.message(Form.number_user)
async def get_phone_number(message: Message, state: FSMContext):
    await state.update_data(number_user=message.text)
    data = await state.get_data()
    logging.info(data)
    number = format_russian_phone_number(data["number_user"])  # Пробуем преобразовать текст в число
    if number:
        await UserDAO.change_number(message.from_user.id, number)
        await message.answer("Номер сохранен! 📞 Подтвердите ваш заказ!")
        await state.clear()
    else:
        await message.answer("Некорректный номер телефона. ❌ Пожалуйста, попробуйте еще раз. 🔄")


@user_router.callback_query(F.data == "canc_order")
async def cancel_order(callback: CallbackQuery):
    await callback.edit_message_text(canc_order())


@user_router.callback_query(F.data == "change_number")
async def make_order(callback: CallbackQuery, state: FSMContext):
    user = await UserDAO.find_one_or_none(telegram_id=callback.from_user.id)
    logging.info(user.number if user else 'Пользователь не найден')
    await callback.answer("Пожалуйста, введите номер телефона. 🔢")
    await state.set_state(Form.number_user_not_ord)
    await callback.message.answer("Введите ваш номер телефона, пожалуйста. 🔢")


@user_router.message(Form.number_user_not_ord)
async def get_phone_number(message: Message, state: FSMContext):
    await state.update_data(number_user_not_ord=message.text)
    data = await state.get_data()

    number = format_russian_phone_number(data["number_user_not_ord"])  # Пробуем преобразовать текст в число
    if number:
        await UserDAO.change_number(message.from_user.id, number)
        await message.answer("Номер сохранен! 📞 ")
        await state.clear()
    else:
        await message.answer("Некорректный номер телефона. ❌ Пожалуйста, попробуйте еще раз. 🔄")