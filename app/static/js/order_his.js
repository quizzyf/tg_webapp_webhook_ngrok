document.addEventListener('DOMContentLoaded', function() {
    // Получаем данные из Telegram Web App
    const initDataUnsafe = Telegram.WebApp.initDataUnsafe;

    // Получаем telegram_id
    const telegramId = initDataUnsafe.user.id;
    const formData = new FormData();
    formData.append('telegram_id', telegramId);

    // Отправляем telegram_id на сервер для получения продуктов
    fetch('/get_orders', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        renderOrders(data.orders);
    })
    .catch(error => console.error('Ошибка:', error));
});

function renderOrders(orders) {
    const tableBody = document.getElementById('orders-table-body');

    orders.forEach((prods, index) => {
        const row = document.createElement('tr');

        const products_list = prods[0]; // Предполагается, что это массив объектов продуктов
        const date_order = prods[1]; // Не используется в текущем коде, но вы можете его использовать позже

        // Создаем HTML для продуктов
        let productsHTML = '';
        products_list.forEach(prod => {
            productsHTML += `
                <div class="name_prod roboto-black">${prod[0].name}:</div>
                <div class="price roboto-black">${prod[0].cost} ₽ * ${prod[1]} шт.</div>
            `;
        });

        // Добавляем кнопку "Заказать снова"
        productsHTML += `
            <div class="container_pl_mi">
                <button class="zak_but count_prod roboto-bold" onclick='againOrder(${JSON.stringify(products_list)})'>В КОРЗИНУ</button>
            </div>
        `;

        // Заполняем строку таблицы
        row.innerHTML = `
            <th>
                <div class="block">
                    <div class="rasp_ord">
                        <div class="ff_ord">
                            <div class="ff_bas">
                                ${productsHTML}
                            </div>
                        </div>
                    </div>
                </div>
            </th>
        `;

        tableBody.appendChild(row);
    });
}

function againOrder(products_list) {
    const initDataUnsafe = window.Telegram.WebApp.initDataUnsafe;
    const userId = initDataUnsafe.user.id;

    const formData = new FormData();
    formData.append('telegram_id', userId);

    // products_list уже является массивом объектов
    const productsToSend = products_list.map(prod => ({
        id: prod[0].id, // Используйте id или любое другое свойство, необходимое для вашего сервера
        count: prod[1],
    }));

    // Добавляем массив объектов в FormData как строку JSON
    formData.append('products_ids', JSON.stringify(productsToSend));

    fetch('/again_order', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            alert('Ошибка при повторном заказе!');
            throw new Error('Network response was not ok');
        }

        return response.json();
    })
    .then(data => {
        alert('Этот заказ добавлен вам в текущую корзину!');
    })
    .catch(error => {
        alert('Ошибка при повторном заказе!');
        console.error('Ошибка:', error);
    });
}
