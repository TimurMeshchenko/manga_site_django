# manga_site_django

[![](https://lh3.googleusercontent.com/fife/AK0iWDzUxSwwk6Fkq6Wk1xl3j6kmHk76CPNvXbVNU91xocoEiUGPYtM4gkfozgkcg6WdxDY6vEW3gIJW15lgo2PHT-4OOkNtTxS_bq2BcUXWo4aGCrgjY2CBZm9_33kBzR902E2qRgpdRydZV6dvcJz3K_JG7pS-dvDka9CDP_TVPhIUbImnMcQGOzYHSGUUiXx7BroKwq_mZXvNtw2xKc7G34yGz7FvYGMUykF5qDfOzePHiUc6fgJNYTWx_gVYMb6zh-5I8LEs8U8Ga8RTD02I-Y8Hou6KFoVk6cXPh2PSKOTEbWj8AqyCcqyrvL__hv7fhxK6T3wYJ2GCoWBCucnUaRo-URCK3axV45nP-Hmm3IkUNecHOu3oANEe8Pc5Tm4W_Bna7Q9GHz8de0jH-6WFsx34ZMWHVrBjp86xfEZ44uBo3-qF7fRR0OAyo0ikYsE5r6Cq3RN_hQ8YtGjLoFXqx7OLO441yW0Mfl3hyad1Lz4kCdlyiJ4tZ0ttRTiaCknEn2hG_emUu5vtLQdDK7ulIDtsGfdNc2QDu2dGpLzm_HzYIGpaOqeviSYyaf22zFv0Ekgv7zo23eKi1I3kxqoNEZ5YB8y7Pmsq0uSobRk9TvpR5J4EqhwPXCnbr8yf8y5l6CwkNjQlLj_ma_BUTfH9lvHQHbLY5fHYIAhIuzeAGv6bKSzNA5FGTLlQbfLK6woPVpYq_JzkNFm-3be-COJgE5ZcTeoJwbJeLtta2hZ-wVZqPVzzznf-S6SEvnMQxzAfZHReR0gJQ6BV5SRcRgkb0ezSXycSb-Rui91kSYDslHCJrLkGyEMEOHoHTPw_vfvUclMYE1AtmnTiMbzwNTAmcXSI_lGyjSnZPVcd6Ez0TKTWuvbZZsjndp6_4AyDKLoQMHcWAcMdytePlPgHZ3ccqJ8_qoi5QTbT6uFSS43wbhdzBkApYkZBCO06kgixcHLhRJ9TUGxLkf-fb8EK0tF7_9wzOVe3Ru4asoCBh2abBbj-_3Iu6yyWOSy4uI9HGux7EFEy0K81a8OrXTknqqn4EqHHIcXw7LgLAMxgsbAtlYXU0c5NclZQ3_hoMask3XC1vD0Soigr3oXuTl7RJWN2caFL7rD4n131U9bME8DLDdPixi4Fp2iD2a7oqi35PA-imYXigLPAbftRVgFtlmmka51BElygr9WpBWR-BDch6IVT6kpwofChI3sMQa_KtOAvu5hfkn4SfN1ZD8j6FN3s-M9AgeP6GdnSX5W5BDaUeWqTXnHkvUyMp8wXQZ2o_5unXUkAvasiHFnKuRz9nlN4fcdH0K47YgfCf9q165gM9gY39pbrazEq3UsGpFtd-mUME7PINszAIZq28Gec1toFCfVwwBteYVG1I3rrkXUbDtF8wsU08IiCJgdaKSySNITSNWmn2360_dayOyY-zqP2RIKWYUavEPoEOgLCeMtjNHzv011laJ9SuQX0vIfgb-UQqKBanmHNcGfmCepow_pPDDf7FTbEUK9P3wvcnqMrdLG52bcgdhn_Kko8Z05dtLiCcIw=w1920-h919)]


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

