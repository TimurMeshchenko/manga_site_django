# manga_site_django

![](https://lh3.googleusercontent.com/fife/AK0iWDxff1KbtkQ5LyOjqm--fSltOWxGbsAorjp1ZUgTH_xy1igbTuFPVFatoxxOemsGPBVPqhaJsY5Gj7qbznyaJ1NSoaVfVK9FfulCTMTu4C0rpxkXIObAIWY3kozSEFdCOjdlto6ehA3EDM3OCvQ2ritC82iZbvhbAuvbb1fEy2kE6Xu-HmW7FU5fnqTnSn5kW7GA-4gTv5yhhhaEx2IaStouL1o2BZ1G5sKd0ihJ4X6ZViAsbUyWv2_CYBsBK7aegsAAYwiN41zxXVr7J_yzxqnpU8Uj6SUW-iZpaY5i_UGcZGmn4fDzNTXb1FboXmqAPGC617KI3STz2VuvE13Xmc4SNsZaKkYFeYRY4HWm88n53C5h7J7UKrAY7h8vRmuRG7VMrSkJIAG3pSeMBXtS3fLxOpSdkYwTCklXdyoyu8KdeVaAsxZEA5Qzp_NdlZ3ce6RCFt3J-H8NsLgb8JUGajNpIViGhTyPh4sOEi5_5-xh6vpKtLdoatmVnzZIRtTKJwP5x5JyJocqgP4fq2eOghECzjeJUZY7-fXQX1eX0cYrRWKAmWMBjlBJnwhjEkOxdYrfIfbnON6AVrwml8UqxCJuJOZYEjVhbuk4m_xyPlUpKsMcZeyBZhnhwflt90mEBtX_JdrqpebZ5NDnaXVdYWRdzTlmyhOx4TwYxCkTkPAPRUELQJr36XJJKLmtgSAtUQuue1u8gKfihhKA0oU-VrHfZ063NWmV9LkBMYGxFmVA3BLS9K7ZV0XaFnGYLYKC_OI1WnlpaW19SzldlK3v32tXsiMYgZZlyjT-LBjVNPHs3Oq3i73T2Feo4aMlGUMBg1WvaQZqllM8x0gEJdle4FALL8HNEqJ1pqVXxzuPIuj1a_ePt603pGQpUXLI4qS5Kt7boTuDMbqVHGa8cQ5plgq_c4b_9Vtsc0zYKblsM_prbkaaDgYWY5aqUOnQp0klmc9ItuIdTCmm047E6ox1feOdT7S0-dQKPn6GMu_uKl1tTidyI-eglJAk3mHrXPOcdH0lnDpV_1nxw7eCA8a0oYReZxNSEnkCjPBhV4m9TL50hMHo0rhPlzcPINFUVsY9GVBeQzhoF39VBvUrmNs2UZ0-C5LDC-nTDSGE6fgbDbqGfGFrlh4f450uw-wu73eUSijBrrrZC7up7cGu4En9GZ90u2KEOaG2b2ze7ZdHrfHy0TaeAgA0jl_S-7ovuMfXgv3yBf0UP-bbHXaruImCr4RTPV3yGB_LWwWcFgKyiQRxXdJJ3-T5lNpAfYrCmWNrS93arLohcujWRwJ5vp6mFj7LUlWeA4fmhCU8joyCtxkBzl0tDVXvGH_mSDc0oLzcRiB1hZyE8Y7uDRyymtEeXcmImfd8SbFYt2HabcLmByV_AdEP1bnQlCLijGubqBNsOKjRBIiYkGD7CZNFOsaPXcMGRFIPSKkDAYP_KCe3HYUgfEltKX6v7Vgtp7s1D0ODKjZ_hcINqzIiAE9oRaCgwniXVFmS3ZyXlau6eV3XEqvvNLTFSmMYi7nKZ-lkpyGz3Vk=w1284-h919)


В разделе "о проекте" указан демонстрационный сайт реализующий данный проект и технологии которые используются.

Хостинг бесплатный, поэтому бывают проблемы с прогрузкой css, тогда нужно обновить страницу.

Для презентабильности проекта взят готовый html, css (js написан с нуля) и данные для бд из [remanga](https://remanga.org/)

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

**Поиск.**
**Закладки.**
**Регистрация, авторизация, выход.** Основаны на сессиях.

**Ajax**, чтобы не обновлять страницу при GET, POST запросах.
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

Для запуска с данными, нужно разархивировать архив с бд в директории **database_data** там же

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

