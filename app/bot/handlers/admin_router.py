from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from app.bot.keyboards.kbs import main_keyboard, admin_keyboard
from app.bot.utils import *
from app.config import settings

admin_router = Router()


@admin_router.message(F.text == '🔑 Админ панель', F.from_user.id.in_([settings.ADMIN_ID]))
async def admin_panel(message: Message):
    await message.answer(
        f"Здравствуйте, <b>{message.from_user.full_name}</b>!\n\n"
        "Добро пожаловать в панель администратора. Здесь вы можете:\n"
        "• Просматривать все текущие заказы\n"
        "• Управлять статусами заказов\n"
        "Для доступа к полному функционалу, пожалуйста, перейдите по ссылке ниже.\n"
        "Мы постоянно работаем над улучшением и расширением возможностей панели.",
        reply_markup=admin_keyboard(user_id=message.from_user.id)
    )


@admin_router.callback_query(F.data == 'back_home')
async def cmd_back_home_admin(callback: CallbackQuery):
    await main_from_admin_mail(callback)