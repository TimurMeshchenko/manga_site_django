# manga_site_django

[![](https://lh3.googleusercontent.com/fife/AK0iWDxPc2aVTZr3Qj2tiwfBo9_5LJm4inzlT2eiTBCmrGcicBQdpaqaj1ceSpaMI3MltZ9sMxBTikQeTKNeavjfOaxGalR-Yh8LfMIaJh72GM6mm-Vc4xmUUmZMXo0Qrx6pTJl0ZEfAcggbZTYQ7OeajtJKAAFyLvynpfirbc6T8_rhSFbG7435JwrRgJs3nhOG1G9zq6SCQ6wVEN9zeldc270qCukbbry_MDp_ulo21xihUr2H2XL7d5CZut6UdSNxSrGknwt17bLpriLCacNw7RT34eFLuET4c_6LLtpRfm8lTm_n8gu4DYNpAaBkrXkdrHgKX1XqgYjZM6gzflPILFoDPRszdeFGcngNS8LXerkbc-ZHDm4_zJvSVx90HiCV2s7ELxReHUpULsMYGrnTqFpdsMiY6Tvlomw5uQoHqlivqPWy6lm3ZrFQWQ1YIbtkaI0Oq9vwGrSti5YyJqoMqHXLBPhziUSFgShvAqL_NDo6pK0FRG3gNv0xA2q64dM-0jUWamW75J0sA-vXppl9kua6Yti3JcI0LlmbGYcAbtpYEIaI2bupudffx9vlAXyi6qi0j7XvVKwb2Im8s1TU-n8WB7i6IyAz7jcFU0bMRHwInsScAqw4bEwNmTXyKXVIJomIO2_BbAIDjMkWFVCTDiQ8i20ypCu7LDcLjPEyno85h_PowSQOvGPYK3jGtvOc0lULFRWIEb59u1YO1xq0riXc25-fp9Lmojx-I8nlbNrYZ0fQ8eIkKLqsZdO0cnRB2peFngmcFMs_QDcea2w0oe7GCM_aaptArDQuHxE4v1d8F7Ir9VmIXldIgRiN4HrHOgE4vkG4xWBaNz-WzmNgdgS--JZ_J3tLwseUvWMvlRnHZ0rnZdBFwFD5X-RJ1ko4r5dXNnTD2w4Vr0G-se-8QHQAWHnwF48g2Jyr0KoSNXAz5ZlFu5D3GLZrnMwNlcKDNbkwHP3V1aD1Pq5evObdwkar3AOXhN8ZoMTqeLzaO5ZXloizkH4-qrqm_JLvvzLlw_y4wiaJ3PV5KIbtCxU7uIs7PnNe8_Zd9OQBA_ZgibS0PxwRcO9wblu_M2CKvXswhYe_WH0INwnjnrsAi8s1GNnhCaDUQOStLrNUne4nsytxwmcrRBKjhoS_tcl6oQeP_vFZD4t_tcKf3q8Yy83MhJvJzaWJJUbk6hF-rh6ZzWVWdmHsiIx2htywKBvO6RZ2H0YYxmTRH3e7sONvCQepXe1EZ44UiwE4-CP9WsUSnvnPlPDW9-W9PkDRh5HYicuE2o1j8o17_UoGjz40FPg0QF1LDQ3xCkueSzYazAKVaCFq2LFk5pfEnz89QuPoCHxsmsWSl67K_RgQE7o5Z7qVUOGhWD6d0d-Wlzf9YdSeVWvSYXlSfwDT3tEpgN0yI1tHf6F_D9zFROsaGGGTbcGSVJBuC3FakfmtzXOrg2_9a1jYziH6pFdvSN9Sl_jiKjpSmiuawJHdOgsHt8jBqZQhnxUrMTVaK8WOkdZdg6chXdi_5YpVRFVILI_IvDXHyuiTb9Q=w1284-h919)
]

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

