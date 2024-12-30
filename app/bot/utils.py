from aiogram.types import Message, CallbackQuery
from app.bot.keyboards.kbs import *


async def get_about_us_text(callback: CallbackQuery) -> None:
    kb = app_keyboard(user_id=callback.from_user.id)
    await callback.message.answer(
        f'Pizza Light — это место настоящей пиццы, приготовленной по традиционным рецептам из качественных ингредиентов.\n\n'
        f'Наша цель — предложить вам ароматную пиццу в уютной атмосфере с друзьями и семьей. 🍕\n\n'
        f'Закажите пиццу на нашем сайте! 🌐', reply_markup=kb)


async def greet_user(message: Message) -> None:
    await message.answer(
        f'👋 Привет! Добро пожаловать в наш бот Pizza Light! 🍕✨\n\n'
        f'Здесь ты можешь легко и быстро заказать вкусную пиццу на любой вкус!\n\n'
        f'📋 Выбери из нашего меню\n'
        f'🛒 Добавь свои любимые блюда в корзину, и через пару кликов твоя пицца будет готова!\n\n'
        f'🌐 Нажми на Главное меню и открывай приложение!',
        reply_markup=start_keyboard(user_id=message.from_user.id)
    )


async def main_mail(message) -> None:
    """
    Приветствует пользователя и отправляет соответствующее сообщение.
    """
    greeting = "С возвращением"
    status = "Рады видеть вас снова!"
    await message.answer(
        f"👋 {greeting}, <b>{message.from_user.full_name}</b>! {status}\n"
        "Что бы ты хотел заказать сегодня?",
        reply_markup=main_keyboard(user_id=message.from_user.id)
    )


async def main_from_admin_mail(callback) -> None:
    """
    Приветствует пользователя и отправляет соответствующее сообщение.
    """
    greeting = "С возвращением"
    status = "Рады видеть вас снова!"
    await callback.message.answer(
        f"👋 {greeting}, <b>{callback.from_user.full_name}</b>! {status}\n"
        "Что бы ты хотел заказать сегодня?",
        reply_markup=main_keyboard(user_id=callback.from_user.id)
    )


async def settings(message) -> None:
    """
    Приветствует пользователя и отправляет соответствующее сообщение.
    """
    greeting = "С возвращением"
    status = "Рады видеть вас снова!"
    await message.answer(
        f"⚙️ Это настройки вашего профиля. Здесь вы можете:\n"
        "  1) Изменить номер телефона",
        reply_markup=settings_keyboard(user_id=message.from_user.id)
    )


def new_order() -> str:
    return """Ваш заказ в обработке! 🛒\n\n Спасибо за использование нашего приложения!\n\n
    (ваш заказ никогда не приедет, это визуализация)"""


def canc_order() -> str:
    return """Ваш заказ в отменен! 🚫\n\n Если хотите подтвердить заказ, снова зайдите в приложение!\n\n Спасибо за использование нашего приложения!"""