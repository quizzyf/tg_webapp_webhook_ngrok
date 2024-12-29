document.addEventListener('DOMContentLoaded', function () {
    // Добавляем обработчик для элемента, который открывает popup
    document.querySelectorAll('.rasp').forEach(function (element) {
        element.addEventListener('click', function () {
            const popupId = this.getAttribute('data-popup-id');
            if (popupId) {
                const popup = document.getElementById(popupId);
                if (popup) {
                    // Переключаем видимость popup
                    popup.classList.toggle('hidden');
                }
            }
        });
    });

    // Добавляем обработчик для закрытия popup при клике за пределами его содержимого
    document.querySelectorAll('.b-popup').forEach(function (popup) {
        popup.addEventListener('click', function (event) {
            // Если клик произошел вне области содержимого popup, то закрываем его
            if (event.target.closest('.b-popup-content')) {
                this.classList.add('hidden');
            }
        });
    });
});
function addToCart(productId) {
    const initDataUnsafe = window.Telegram.WebApp.initDataUnsafe;
    const uid = initDataUnsafe.user.id;

    const formData = new FormData();
    formData.append('telegram_id', uid);
    formData.append('product_id', productId);// Убедитесь, что это соответствует вашим ожиданиям на стороне сервера

    fetch('/add_to_cart', {
        method: 'POST',
        body: formData,  // Передаем formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        alert('Товар добавлен в корзину!');
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}