Привет, это простой проект для создания телеграм бота который будет отображать сайт на FastAPI как мини приложение телеграма (WebApp)
Для того чтобы запустить проект, следуйте простым шагам:
  1) установите все библиотеки из reqirements.txt
  2) установите ngrok на ваш компьютер и войдите в аккаунт (сервис для вывода вашего сайта в интернет с помощью туннелей). Все инструкции по скачиванию можно найти на их сайте ngrok.com
  3) после установки ngrok`а, зайдите в консоль (Win + R -> cmd -> OK) и напишите "ngrok http n" n - порт на вашем компьютере (обычно от 8000 до 9000)
     ngrok запустится и выведет порт n в интернет, и выдаст вам бесплатный домен заканчивающийся на ...ngrok-free.app. Скопируйте эту ссылку и не закрывайте окно с ngrok
  4) далее вам нужно создать .env файл в корне проекта (там где находится requirements.txt) и вписать в него следущие строки
      BOT_TOKEN=токен вашего бота
      BASE_SITE=скопированная ссылка с ngrok`а
      ADMIN_ID=ваш Telegram_id (можно узнать написав боту @get_tg_ids_universeBOT)
  5) проект готов к запуску, запустите еще одну консоль и с помощью команды cd <путь до папки с проектом> зайдите в скачанный проект
     напишите uvicorn app.main:app --port n (n - порт, указанный при запуске ngrok)


