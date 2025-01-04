# manga_site_django
 
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

**Есть версия на FastAPI [https://github.com/TimurMeshchenko/manga_site_fastapi](https://github.com/TimurMeshchenko/manga_site_fastapi)**

**Основные отличия от FastAPI версии:**

* Redis используется только для Celery.
* Через Celery, а не RabbitMQ, отправляются письма для восстановления пароля.
* Регистрация, авторизация основаны на сессиях.
* Вместо Fetch Ajax.

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

### Настройка postgresql
# Запуск postgresql с контейнера
```bash
docker run --name postgres -e POSTGRES_PASSWORD=postgres -v ./database_backups:/database_backups -d -p 5432:5432 postgres:16
```

```bash
sudo -u postgres psql
create database remanga;
sudo -u postgres psql -d remanga -f database_backups/release_plain.sql
```

### Запуск

```bash
poetry install
poetry run python -m uvicorn remanga_site.asgi:application --reload

poetry run ./run_with_reload.sh
```

Прод:

/remanga/templates/bookmarks.html, /remanga/templates/title.html

ws=new WebSocket(`wss://${window.location.host}/manga/ws/${session_id}`);

poetry run python -m uvicorn remanga_site.asgi:application --ssl-keyfile /etc/letsencrypt/live/meshchenko.ru/privkey.pem --ssl-certfile /etc/letsencrypt/live/meshchenko.ru/fullchain.pem

MacOS nginx
```bash
proxy_pass to /usr/local/etc/nginx/nginx.conf
brew services restart nginx
```

### Для возможности восстанавливать пароль по почте

```bash
poetry run python -m celery -A remanga_site worker --pool=solo -l info
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

**Запуск парсера**

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

# Webpack optimization

docker build -f Dockerfile.webpack -t manga_webpack .
docker run --name manga_webpack_container -p 8080:8080 -v ./optimized:/app/optimized -v ./webpack.config.js:/app/webpack.config.js -d manga_webpack
sudo docker exec -it manga_webpack_container bash

npx webpack

sudo docker stop manga_webpack_container
sudo docker rm manga_webpack_container
sudo docker rmi manga_webpack