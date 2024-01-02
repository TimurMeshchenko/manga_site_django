# manga_site_django

![](https://lh3.googleusercontent.com/fife/AK0iWDxZYW5um9yXHTXYIpCDH4wN8BumOJEra9Xvl8Oqt5Vpxn40GYw-el49xr6zXofGSI2ax1Ajckcx59y3LbnKzyQsjJTkBAf6CZBykqEahBToWbrR9MZM6UinU74DkwgzGzCzO3Gt-6Owwu-tHycX3lPZ7paZ4s4lOrAI9J24_1fWjqwrQNFmLwQtCtiKyRf-P1jxjcvT70-I_cRjuUP-3hnsSgXvxzxBtcJLuGflni1aOulX4PW_YTrhSO7YPvPe7RPuUi3FjyiTG-tMv-wMtZyolzuTDSCQwZC3SPhQv5U1VD-TY9sP_SuXDwgl_82uf7AEGRKmVWYsesF0aNP9mJ4UjlEJHHhgekiSGXU70uOM6_g3ceDD8OUVQ-wIYnmG8qp5eWswa8MN2Y8bMriWhaKj7sdq40Yk47M-3s-3chibjIadMrkXspM0RqFahd7ucGfEW4An_yGsi6k8cl4Ys0mh-8n9gtM4PIp-6H5qrEyp-eIX7mu53Ost-DV5o-l-B-V4jcHSJBjxZfAlMKlm8sMl5NE-gcjMf_Lf_u5j2b3BPZe4tDkBvQVBF22XNZ2s5qR9blD9GxtnM_HQI-gBGxgxgtemVGIQdsUPdfouSb-CUPzQSyA0X7FqDUil0RROgUoHl3eG3zjXgj9s1sBP6HDYmpQ_BMV1jekxyPWhSPpVVaH1gejdIScwuJnL_wVo195oHWAJYUWe1wCfZ95VAtxvbkt6oA2m_013k6AWINknCdHa_j6Zu7SuGPNZp_WgRMts4ZjLCK8RPcp8ZElexIhrBgX_ukzN_d1mATYCSV6ROS97VoEm7y1DGAqQsXvmI5wKSkz4eCyxkYj_QwhF3Zu5AfgMePAiZ_wbwUKX83Gg-WH-wsZIafBgfHk6zkzPupQT0zWckRTSXT_6wy6ykpMV1X-cavxEH0j166Kdwv6KvHCRv_za_LRQlb-EYIRqKwvfSibmDH92bTrh-oHwBXqegwwii7XjBVJUkToshUWQ9p2zSBdsN0sxv839QA6-bhNZe2kWZS2wgMjWF7gjVeeKPvIiGmDBklTD_FBSXzdE9jZ3NNE8Wv0MtTvAB2vGvF4ujDPkPlCltW5iYVtNoighBY7HWht3aKJ0asavvdE6OamnQ4N-oqkbWcKp5dGDj_hWCDlB4EUdG4ZUqNPmvYv511Pl-VJwfWhnbC7rkWqBLpSkINwEP_m9nh6kFqDMaDRaBobcbhCiL5xTsIOg3uvTDpa07oFZHhJ5hX4ePVXEgAqdm_zDEEGnkLPrD5ne-gvvDA2MLWT3DYaqLh2-ZJtD-qawO3PbFT9jrdTWwB-5l3b6ADMBA-igM4sCZlbOE3u9ZBn4FQ3j7SKmJtmKixF1e_uRYP3mY20ROLfyKti0C7AllioptIe68ZtgkDViK3kaC495KCYLrSPzJ_y9ERRVRuifbhU-WexbSJZ1xKTqymaAx6UUOcugAEkHzd58PxrL1DnzxHQzPmlL_otjRbDjAausXL9w5bXV69lMYNIax2530o33RoXjsDlLKZGbPP0=w1284-h919)

**Есть версия на FastAPI без сайта [manga_site_fastapi](https://github.com/TimurMeshchenko/manga_site_fastapi)**

**Обзор всего функционала версии с FastAPI, только вместо RabbitMQ Celery** [https://www.youtube.com/watch?v=x2cIkt0P3XQ](https://www.youtube.com/watch?v=x2cIkt0P3XQ)

**Сайт, указанный в проекте, демонстрационный на бесплатном хостинге, поэтому там нет WebSockets, Redis, Celery, SMTP.**

**Сайт создан в учебных целях. Источник дизайна и данных для базы данных [remanga](https://remanga.org/), (JavaScript написан с нуля).**

**Основные отличия от FastAPI версии:**

* Redis используется только для Celery.
* Через Celery, а не RabbitMQ, отправляются письма для восстановления пароля.
* Регистрация, авторизация основаны на сессиях.
* Вместо Fetch Ajax.
 
## Реализованный функционал: 

**Каталог тайтлов:**
* Infinity scroll (тайтлы загружаются при прокрутке вниз). Когда пользователь скролит до последнего тайтла, отправляется Ajax запрос на получение новых тайтлов.
* Фильтрация тайтлов через параметры запроса.

**Страница с тайтлом:**

* Оценка тайтла (под названием тайтла нажать на звезду) Ajax.
* Сохранение тайтла в закладки. Реализовано с помощью **WebSockets**. 
При добавлении тайтла в закладки, он появляется в закладках и обновляется 
информация о тайтле у всех сессий пользователя.
* Комментарии. Реализовано с помощью **WebSockets**. При отправлении добавляется
у всех пользователей, которые сейчас находятся на той же странице.
* Оценка комментариев и переход по профилю автора Ajax.

**Профиль:**
Изменение аватарки и пароля Ajax.

**Поиск.** Infinity scroll.

**Закладки.** Обновляются в режиме реального времени с помощью WebSockets.

**Регистрация, авторизация, выход.** Основаны на сессиях, обновляются с помощью Ajax.

**Восстановление пароля.** Асинхронное отправление письма с помощью Celery.

**Парсер**, асинхронное с помощью asyncio получение данных с сайта remanga и автоматическое добавление в БД.

## Установка

### Docker версия. 

Запуск  
```bash 
docker compose up 
```
Для запуска с данными нужно восстановить БД

```bash 
docker exec -it postgresdb bash
psql -U postgres -d postgres -f /database_backups/release_plain.sql
Пароль postgres
```

### Без Docker

1. Активировать виртуальное окружение. 
```bash
myenv/Scripts/activate
```

Или

Установить Django и его зависимости. 
```bash
pip install -r requirements.txt
```

2. Заменить данные для подключения БД на свои в файле .env.dev

Для запуска с данными нужно импортировать PostgreSQL backup в директории database_backups для БД, указанной в .env.dev 
```bash
psql -U DB_USER -d DB_NAME -f database_backups/release_plain.sql

Ex. psql -U postgres -d remanga -f database_backups/release_plain.sql
```

3. Запустить проект. 
```bash
python -m uvicorn remanga_site.asgi:application --reload
```

## (Если нужно больше данных) Настройка парсера.
Для заполнения базы данных можно использовать parser в одноименной директории. 
Он асинхронно парсит [remanga](https://remanga.org/) и заполняет базу данных.

На каждой странице 30 тайтлов. В БД хранится 10 страниц, поэтому начать парсить нужно с 11 страницы.

Настройка диапозона парсинга страниц в этих строчках кода
```python
start_page_parsing = 11
end_page_parsing = 12 
```

**Запуск**

```bash
cd parser

python remanga_parser.py
```

## Тесты. 
Запускаются в github actions.

* Асинхронная проверка данных, полученых от парсера.

* Проверка исключений в параметрах запроса для фильтрации тайтлов.
* Проверка всех фильтров тайтлов.
* Проверка исключений всех POST запросов для тайтлов.
* Проверка оценки тайтла.
* Проверка оценки комментария тайтла.