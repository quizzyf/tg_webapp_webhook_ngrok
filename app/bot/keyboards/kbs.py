from aiogram.types import ReplyKeyboardMarkup, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from app.config import settings


def main_keyboard(user_id: int, first_name: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    url_applications = f"{settings.BASE_SITE}"

    kb.button(text="🌐 Открыть приложение", web_app=WebAppInfo(url=str(settings.BASE_SITE)))
    kb.button(text="ℹ️ О нас", callback_data='nnn')
    if user_id == settings.ADMIN_ID:
        kb.button(text="🔑 Админ панель", callback_data='bbb')
    kb.adjust(1)
    return kb.as_markup()


def back_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="🔙 Назад")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def admin_keyboard(user_id: int) -> InlineKeyboardMarkup:
    url_applications = f"{settings.BASE_SITE}/admin?admin_id={user_id}"
    kb = InlineKeyboardBuilder()
    kb.button(text="🏠 На главную", callback_data="back_home")
    kb.button(text="📝 Смотреть заявки", web_app=WebAppInfo(url=url_applications))
    kb.adjust(1)
    return kb.as_markup()


def app_keyboard(user_id: int, first_name: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    url_add_application = f'{settings.BASE_SITE}/'
    kb.button(text="📝 Cделать заказ", web_app=WebAppInfo(url=url_add_application))
    kb.adjust(1)
    return kb.as_markup()


def order_confirm(user_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Подтвердить ✅", callback_data="new_order")
    kb.button(text="Отклонить ❌", callback_data="canc_order")
    kb.adjust(1)
    return kb.as_markup()