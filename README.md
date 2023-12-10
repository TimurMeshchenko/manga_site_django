<h3>В разделе "о проекте" указан демонстрационный сайт реализующий данный проект и технологии которые используются.
Хостинг бесплатный, поэтому бывают проблемы с прогрузкой css, тогда нужно обновить страницу.

Для презентабильности проекта взят готовый html, css (js написан с нуля) и данные для бд из <a href="https://remanga.org/">remanga.org</a>
</h3>
<h3>
Реализованный функционал: 
</h3>

Каталог тайтлов: 
    Infinity scroll (тайтлы загружаются при прокрутке вниз)
    Фильтрация тайтлов.

Страница с тайтлом: 
    Оценка тайтла (под названием тайтла нажать на звезду).
    Сохранение тайтла в закладки. (сделал без WebSocket, чтобы не увеличивать зависимости)
    Комментарии и их оценка, ещё переход по профилю.

Профиль:
    Изменение аватарки и пароля.

Поиск.
Закладки.
Регистрация, авторизация, выход. Основаны на сессиях.

Ajax, чтобы не обновлять страницу при GET, POST запросах.
Парсер, чтобы вручную не заполнять бд.

<h1> Установка </h1>

Активировать виртуальное окружение. КОД myenv/Scripts/activate

Или

Установить django и его зависимости. 
КОД pip install -r requirements.txt

Заменить данные для подключения бд на свои в файле remanga_site/settings.py 

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "remanga",
        "USER": "postgres",
        "PASSWORD": "Qewads",
        "HOST": "127.0.0.1",
        'PORT': '5432',
    }
}

Создать таблицы в базе данных. 
КОД python manage.py migrate

Для запуска с данными нужно импортировать PostgreSQL backup в директории database_backups. 
КОД psql -d remanga -f database_backups/PostgreSQL.sql

Запустить проект. python manage.py runserver

Также присутствует docker версия. 
Для запуска с данными, нужно разархивировать архив с бд в директории database_data
Запуск КОД docker compose up

Для заполнения базы данных можно использовать parser в одноименной директории. Он парсит https://remanga.org/ и заполняет базу данных.

<h1>Настройка парсера</h1>

КОД connect_to_database заменить на такой же как и в django settings

На каждой странице 30 тайтлов, в бд хранится 10 страниц, поэтому начать парсить нужно с 11 страницы.

Настройка диапозона парсинга страниц в этом коде

for titles_page in range(11, 12):

Где 11 - номер страницы, которую нужно начать парсить, 12 - закончить

