document.addEventListener('DOMContentLoaded', function() {
    // Получаем данные из Telegram Web App
    const initDataUnsafe = Telegram.WebApp.initDataUnsafe;

    // Получаем telegram_id
    const telegramId = initDataUnsafe.user.id;
    const formData = new FormData();
    formData.append('telegram_id', telegramId);

    // Отправляем telegram_id на сервер для получения продуктов
    fetch('/get_products', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        renderProducts(data.products);
    })
    .catch(error => console.error('Ошибка:', error));
});

function renderProducts(products) {
    const tableBody = document.getElementById('products-table-body');
    let totalSum = 0; // Переменная для хранения общей суммы

    products.forEach((item, index) => {
        const row = document.createElement('tr');

        const productCost = item[0].cost;
        const productQuantity = item[1];
        const productTotal = productCost * productQuantity;

        totalSum += productTotal; // Обновляем общую сумму

        row.innerHTML = `
            <th>
                <div class="block">
                    <div class="rasp_bas" data-popup-id="popup${item[1]}">
                        <div class="ff_bas">
                            <div class="container_pl_mi">
                                <div class="name_prod roboto-black">${item[0].name}:</div>
                                <div id="cost-${item[0].id}" class="price roboto-black">${productCost} ₽</div>
                            </div>
                            <div class="container_pl_mi">
                                <button class="but minus count_prod" onclick="decreaseQuantity('${item[0].id}')">-</button>
                                <span class="roboto-black count_prod" id="quantity-${item[0].id}">${productQuantity}</span>
                                <button class="but plus count_prod" onclick="increaseQuantity('${item[0].id}')">+</button>
                                <span class="roboto-black price itogo" id="itogo-${item[0].id}">Итого: ${productTotal} ₽</span>
                            </div>
                        </div>
                    </div>
                </div>
            </th>
        `;

        tableBody.appendChild(row);
    });

    // Добавляем итоговую сумму в конец таблицы
    const totalRow = document.createElement('tr');
    totalRow.innerHTML = `
        <th>
            <div class="block">
                <div class="rasp_bas">
                    <div class="ff_bas_zak">
                        <div class="container_pl_mi">
                            <div class="name_prod roboto-black">Итоговая сумма:</div>
                            <div class="price roboto-black">${totalSum} ₽</div>
                        </div>
                        <button class="zak_but count_prod roboto-bold" onclick="newOrder()">ЗАКАЗАТЬ</button>
                    </div>
                </div>
            </div>
        </th>
    `;
    tableBody.appendChild(totalRow);
}

function increaseQuantity(productId) {
    const quantityElement = document.getElementById(`quantity-${productId}`);
    const costElement = document.getElementById(`cost-${productId}`);
    const itogoElement = document.getElementById(`itogo-${productId}`);
    let quantity = parseInt(quantityElement.textContent);
    let cost = parseInt(costElement.textContent);
    quantityElement.textContent = quantity + 1;
    itogoElement.textContent = 'Итого: ' + cost * (quantity + 1) + ' ₽';

    updateTotalSum(); // Обновляем общую сумму

    const initDataUnsafe = window.Telegram.WebApp.initDataUnsafe;
    const userId = initDataUnsafe.user.id;

    const formData = new FormData();
    formData.append('telegram_id', userId);
    formData.append('product_id', productId);

    fetch('/add_to_cart', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}

function decreaseQuantity(productId) {
    const quantityElement = document.getElementById(`quantity-${productId}`);
    const costElement = document.getElementById(`cost-${productId}`);
    const itogoElement = document.getElementById(`itogo-${productId}`);

    let quantity = parseInt(quantityElement.textContent);
    if (quantity > 0) {
        let cost = parseInt(costElement.textContent);
        quantityElement.textContent = quantity - 1;
        itogoElement.textContent = 'Итого: ' + cost * (quantity - 1) + ' ₽';

        updateTotalSum(); // Обновляем общую сумму

        const initDataUnsafe = window.Telegram.WebApp.initDataUnsafe;
        const userId = initDataUnsafe.user.id;

        const formData = new FormData();
        formData.append('telegram_id', userId);
        formData.append('product_id', productId);

        fetch('/del_from_cart', {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
    }
    if (quantity == 1) {
        alert('Товар удален из корзины!');
        window.location.reload();
    }
}

function updateTotalSum() {
    const tableBody = document.getElementById('products-table-body');
    let totalSum = 0;

    // Суммируем все итоговые суммы продуктов
    const itogoElements = tableBody.querySelectorAll('.itogo');
    itogoElements.forEach(itogo => {
        const itogoValue = parseInt(itogo.textContent.replace('Итого: ', '').replace(' ₽', ''));
        totalSum += itogoValue;
    });

    // Обновляем отображение итоговой суммы
    const totalRow = tableBody.querySelector('tr:last-child');
    const totalPriceElement = totalRow.querySelector('.price.roboto-black');
    totalPriceElement.textContent = `${totalSum} ₽`;
}

function newOrder() {
    const initDataUnsafe = window.Telegram.WebApp.initDataUnsafe;
    const userId = initDataUnsafe.user.id;

    const formData = new FormData();
    formData.append('telegram_id', userId);

    fetch('/new_order', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        return response.json();
    })
    .then(data => {
        alert('Подтвердите ваш заказ в боте!');
        window.Telegram.WebApp.close();
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });

}
