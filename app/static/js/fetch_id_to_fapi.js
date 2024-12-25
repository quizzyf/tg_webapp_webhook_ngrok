const tg = window.Telegram.WebApp;
tg.expand();
const user = tg.initDataUnsafe.user;

const urlParams = new URLSearchParams(window.location.search);
const tgWebAppStartParam = urlParams.get('tgWebAppStartParam');

const fetchData = async (prod) => {
    let params;
    // Отправляем POST запрос
    if (tgWebAppStartParam) {
        params = new URLSearchParams({ tg_id: user.id.toString(), fat_id : tgWebAppStartParam });
    }
    else {
        params = new URLSearchParams({ tg_id: user.id });
    }

    const response = await fetch('/login', {
        method: 'POST',
        body: params
    });

    return await response.json();
};


const dataPromise = fetchData();