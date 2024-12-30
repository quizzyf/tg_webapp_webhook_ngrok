import json
import logging
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from app.api.dao import *
from pydantic import BaseModel

from app.bot.create_bot import bot
from app.bot.keyboards.kbs import order_confirm
from app.config import settings


class UserData(BaseModel):
    telegram_id: int
    additional_number: int


class UserID(BaseModel):
    telegram_id: int


router = APIRouter(prefix='', tags=['Фронтенд'])
templates = Jinja2Templates(directory='app/templates')


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    products = await ProductDAO.find_all()
    return templates.TemplateResponse("index.html",
                                      {"request": request, "title": "Pizza Light", "products": products})


@router.get("/aboutus", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("about_us.html",
                                      {"request": request})


@router.get("/search", response_class=HTMLResponse)
async def read_root(request: Request, query: str = ""):
    products = await ProductDAO.find_all()
    results = [product for product in products if query.lower() in product.name.lower()]
    if not results or query == '':
        results = 'Ничего не найдено 🥲'
    return templates.TemplateResponse("search.html", {"request": request, "results": results, "query": query})


@router.get("/cart", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("basket.html", {"request": request})


@router.get("/order_history", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("orders_history.html", {"request": request})


@router.get("/admin", response_class=HTMLResponse)
async def read_root(request: Request, admin_id: int = None):
    data_page = {"request": request}
    if admin_id is None or admin_id != settings.ADMIN_ID:
        data_page['applications'] = []
        return templates.TemplateResponse("orders_admin.html", data_page)
    else:
        orders_not_completed = await OrderDAO.get_all_applications()
        orders_not_completed.sort(key=lambda x: x['appointment_date'])
        for order in orders_not_completed:
            order['appointment_date'] = order['appointment_date'].strftime('%d.%m.%Y, %H:%M')
            new_products = []
            for i in order['products_list'].split(','):
                prod_id, count = i.split('#')
                prod = await ProductDAO.find_one_or_none_by_id(int(prod_id))
                new_products.append([prod, int(count)])
            order['products_list'] = new_products

        data_page['applications'] = orders_not_completed
        return templates.TemplateResponse("orders_admin.html", data_page)


@router.post("/index/{prod_id}", response_class=HTMLResponse)
async def add_product_cart(user_data):
    telegram_id = user_data.telegram_id
    additional_number = user_data.additional_number
    logging.info(telegram_id, additional_number)
    # Обработайте полученные данные здесь


@router.post("/get_products")
async def get_products(telegram_id: int = Form(...)):
    products = await UserDAO.get_cart(telegram_id)
    new_products = []
    if products:
        for i in products.split(','):
            prod_id, count = i.split('#')
            prod = await ProductDAO.find_one_or_none_by_id(int(prod_id))
            new_products.append([prod, int(count)])
    return {"products": new_products}


@router.post("/get_orders")
async def get_products(telegram_id: int = Form(...)):
    orders = await UserDAO.get_orders(telegram_id)
    orders_ret = []
    for order in orders:
        new_products = []
        if order.products_list:
            for i in order.products_list.split(','):
                prod_id, count = i.split('#')
                prod = await ProductDAO.find_one_or_none_by_id(int(prod_id))
                new_products.append([prod, int(count)])
        orders_ret.append([new_products, order.created_at.strftime('%d.%m.%Y, %H:%M')])
    return {"orders": list(reversed(orders_ret))}


@router.post("/add_to_cart")
async def receive_telegram_id(telegram_id: int = Form(...), product_id: int = Form(...)):
    logging.info(f"Получен Telegram ID: {telegram_id}, Product ID: {product_id}")
    await UserDAO.add_product_basket(telegram_id, product_id)
    logging.info(f"Товар добавлен в корзину!")
    return JSONResponse(content={'re': 1})


@router.post("/del_from_cart")
async def receive_telegram_id(telegram_id: int = Form(...), product_id: int = Form(...)):
    logging.info(f"Получен Telegram ID: {telegram_id}, Product ID: {product_id}")
    await UserDAO.delete_product_basket(telegram_id, product_id)
    logging.info(f"Товар удален из корзины!")
    return JSONResponse(content={'re': 1})


@router.post("/new_order")
async def login(telegram_id: int = Form()):
    logging.info(f"Получен Telegram ID: {telegram_id} для нового заказа")
    message = 'Подтвердите ваш заказ, указанный в приложении:\n'
    products = await UserDAO.get_cart(telegram_id)
    new_products = []
    if products:
        l = products.split(',')
        for i in range(len(l)):
            prod_id, count = l[i].split('#')
            prod = await ProductDAO.find_one_or_none_by_id(int(prod_id))
            message += f'\t{i + 1}) {prod.name.capitalize()} ({prod.cost} ₽) * {int(count)} шт. = {prod.cost * int(count)} ₽\n'
            new_products.append([prod, int(count)])
    total_sum = 0
    for i in new_products:
        total_sum += (i[0].cost * i[1])
    message += f'Итого: {total_sum} ₽'
    await bot.send_message(telegram_id, message, reply_markup=order_confirm(telegram_id))
    return {"re": 1}


@router.post("/again_order")
async def login(telegram_id: int = Form(), products_ids: str = Form(...)):
    products = json.loads(products_ids)
    logging.info(f"Получен Telegram ID: {telegram_id, json.loads(products_ids)} для нового заказа")
    for item in products:
        for i in range(item['count']):
            await UserDAO.add_product_basket(telegram_id, item['id'])
    return {"re": 1}
