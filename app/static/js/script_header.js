const menuBtn = document.querySelector('.menu-btn');
const menu = document.querySelector('.menu');
const content = document.querySelector('.main');
const br = document.querySelector('.brand_name');



// Обработчик события нажатия на кнопку
menuBtn.addEventListener('click', function(e) {
    e.preventDefault(); // Отмена стандартного поведения
    menu.classList.toggle('menu_active'); // Переключаем класс для меню
    content.classList.toggle('main_active');
    br.classList.toggle('brand_name_active');
    console.log('ttte')
});

