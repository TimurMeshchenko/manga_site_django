# manga_site_django

![](https://lh3.googleusercontent.com/fife/AK0iWDxZYW5um9yXHTXYIpCDH4wN8BumOJEra9Xvl8Oqt5Vpxn40GYw-el49xr6zXofGSI2ax1Ajckcx59y3LbnKzyQsjJTkBAf6CZBykqEahBToWbrR9MZM6UinU74DkwgzGzCzO3Gt-6Owwu-tHycX3lPZ7paZ4s4lOrAI9J24_1fWjqwrQNFmLwQtCtiKyRf-P1jxjcvT70-I_cRjuUP-3hnsSgXvxzxBtcJLuGflni1aOulX4PW_YTrhSO7YPvPe7RPuUi3FjyiTG-tMv-wMtZyolzuTDSCQwZC3SPhQv5U1VD-TY9sP_SuXDwgl_82uf7AEGRKmVWYsesF0aNP9mJ4UjlEJHHhgekiSGXU70uOM6_g3ceDD8OUVQ-wIYnmG8qp5eWswa8MN2Y8bMriWhaKj7sdq40Yk47M-3s-3chibjIadMrkXspM0RqFahd7ucGfEW4An_yGsi6k8cl4Ys0mh-8n9gtM4PIp-6H5qrEyp-eIX7mu53Ost-DV5o-l-B-V4jcHSJBjxZfAlMKlm8sMl5NE-gcjMf_Lf_u5j2b3BPZe4tDkBvQVBF22XNZ2s5qR9blD9GxtnM_HQI-gBGxgxgtemVGIQdsUPdfouSb-CUPzQSyA0X7FqDUil0RROgUoHl3eG3zjXgj9s1sBP6HDYmpQ_BMV1jekxyPWhSPpVVaH1gejdIScwuJnL_wVo195oHWAJYUWe1wCfZ95VAtxvbkt6oA2m_013k6AWINknCdHa_j6Zu7SuGPNZp_WgRMts4ZjLCK8RPcp8ZElexIhrBgX_ukzN_d1mATYCSV6ROS97VoEm7y1DGAqQsXvmI5wKSkz4eCyxkYj_QwhF3Zu5AfgMePAiZ_wbwUKX83Gg-WH-wsZIafBgfHk6zkzPupQT0zWckRTSXT_6wy6ykpMV1X-cavxEH0j166Kdwv6KvHCRv_za_LRQlb-EYIRqKwvfSibmDH92bTrh-oHwBXqegwwii7XjBVJUkToshUWQ9p2zSBdsN0sxv839QA6-bhNZe2kWZS2wgMjWF7gjVeeKPvIiGmDBklTD_FBSXzdE9jZ3NNE8Wv0MtTvAB2vGvF4ujDPkPlCltW5iYVtNoighBY7HWht3aKJ0asavvdE6OamnQ4N-oqkbWcKp5dGDj_hWCDlB4EUdG4ZUqNPmvYv511Pl-VJwfWhnbC7rkWqBLpSkINwEP_m9nh6kFqDMaDRaBobcbhCiL5xTsIOg3uvTDpa07oFZHhJ5hX4ePVXEgAqdm_zDEEGnkLPrD5ne-gvvDA2MLWT3DYaqLh2-ZJtD-qawO3PbFT9jrdTWwB-5l3b6ADMBA-igM4sCZlbOE3u9ZBn4FQ3j7SKmJtmKixF1e_uRYP3mY20ROLfyKti0C7AllioptIe68ZtgkDViK3kaC495KCYLrSPzJ_y9ERRVRuifbhU-WexbSJZ1xKTqymaAx6UUOcugAEkHzd58PxrL1DnzxHQzPmlL_otjRbDjAausXL9w5bXV69lMYNIax2530o33RoXjsDlLKZGbPP0=w1284-h919)


В разделе "о проекте" указан демонстрационный сайт реализующий данный проект и технологии которые используются.

Хостинг бесплатный, поэтому бывают проблемы с прогрузкой css, тогда нужно обновить страницу.

Сайт создан в учебных целях, источник дизайна и данных для базы данных [remanga](https://remanga.org/),  
(js написан с нуля).  

## Реализованный функционал: 

**Каталог тайтлов:**
    Infinity scroll (тайтлы загружаются при прокрутке вниз)
    Фильтрация тайтлов.

**Страница с тайтлом:**
    Оценка тайтла (под названием тайтла нажать на звезду).
    Сохранение тайтла в закладки. (сделал без WebSocket, чтобы не увеличивать зависимости)
    Комментарии и их оценка, ещё переход по профилю.

**Профиль:**
    Изменение аватарки и пароля.

**Поиск.** Infinity scroll
**Закладки.**
**Регистрация, авторизация, выход.** Основаны на сессиях, обновляются с помощью ajax.

**Парсер**, чтобы вручную не заполнять бд.

## Установка

Активировать виртуальное окружение. 
```bash
myenv/Scripts/activate
```

Или

Установить django и его зависимости. 
```bash
pip install -r requirements.txt
```

Заменить данные для подключения бд на свои в файле remanga_site/settings.py 

```python
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
```

Создать таблицы в базе данных. 
```bash
python manage.py migrate
```

Для запуска с данными нужно импортировать PostgreSQL backup в директории database_backups. 
```bash
psql -d remanga -f database_backups/PostgreSQL.sql
```

Запустить проект. 
```bash
python manage.py runserver
```

### Также присутствует docker версия. 

Для запуска с данными, нужно разархивировать архив с бд в директории **database_data** и там оставить 

Запуск  
```bash 
docker compose up 
```

## (Если нужно больше данных) Настройка парсера
Для заполнения базы данных можно использовать parser в одноименной директории. 
Он парсит [remanga](https://remanga.org/) и заполняет базу данных.

Подключение к бд заменить на такой же, как и в remanga_site/settings.py 

```python
def connect_to_database(self) -> None:
    self.db_connection = psycopg2.connect(
        database="remanga",
        user="postgres",
        password="Qewads",
        host="127.0.0.1",
        port='5432'
    )
```

На каждой странице 30 тайтлов, в бд хранится 10 страниц, поэтому начать парсить нужно с 11 страницы.

Настройка диапозона парсинга страниц в этом коде
```python
for titles_page in range(11, 12):
```

Где 11 - номер страницы, которую нужно начать парсить, 12 - закончить

