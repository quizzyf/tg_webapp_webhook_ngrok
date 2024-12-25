import logging
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from app.api.dao import *
from pydantic import BaseModel


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


@router.get("/bobik", response_class=HTMLResponse)
async def read_root(request: Request):
    items = ['первое', "второе", "третье"]
    return templates.TemplateResponse("temp.html",
                                      {"request": request, "items": items})


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
    logging.info(new_products)
    return {"products": new_products}


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


@router.post("/login")
async def login(tg_id: int = Form(), fat_id: str | None = Form(None)):
    if fat_id and fat_id.isdigit():
        logging.info(f"Получен Telegram ID: {tg_id}")
        return {"re": 1}
    logging.info(f"Получен Telegram ID: {tg_id}")
    return {"re": 1}
