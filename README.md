# API Music & Movies DB

## Описание:
Проект API Music & Movies DB собирает отзывы пользователей на произведения. Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка».
Произведению может быть присвоен жанр из списка предустановленных. Пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от 1 до 10. Пользователи могут оставлять комментарии к отзывам.

## Реализованный функционал:
Реализован механизм авторизации.
Тип пользователя определяется в соответствии с результатом авторизации.
Получать запрошенные данные при обращении к ресурсам: CATEGORIES, GENRES, TITLES, REVIEWS, COMMENTS, USERS
Возможность писать отызвы и комментарии к отзывам, ставить оценки произведениям.
К API есть документация по адресу http://127.0.0.1:8000/redoc/

## Стек проекта:
asgiref==3.6.0
atomicwrites==1.4.1
attrs==23.1.0
certifi==2023.5.7
charset-normalizer==2.0.12
colorama==0.4.6
Django==3.2
django-filter==23.2
djangorestframework==3.12.4
idna==3.4
iniconfig==2.0.0
packaging==23.1
pluggy==0.13.1
py==1.11.0
PyJWT==2.1.0
pytest==6.2.4
pytest-django==4.4.0
pytest-pythonpath==0.7.3
djangorestframework-simplejwt==4.7.2
pytz==2023.3
requests==2.26.0
sqlparse==0.4.4
toml==0.10.2
urllib3==1.26.15

## Установка и запуск проекта:
- Клонировать репозиторий и перейти в него в командной строке:
  ```
   git clone git@github.com:aten88/api_yamdb.git
  ```
  ```
   cd api_yamdb
  ```
- Cоздать и активировать виртуальное окружение:
  ```
   python 3.9 -m venv venv
  ```
  ```
   source venv/Scripts/activate
  ```

- Обновить pip и установить зависимости из файла requirements.txt:
  ```
   python -m pip install --upgrade pip
  ```
  ```
   pip install -r requirements.txt
  ```
- Выполнить миграции:
  ```
   python manage.py migrate
  ```
- Запустить проект:
  ```
  python manage.py runserver
  ```
## Примеры работы с API для всех пользователей:
- Для неавторизованных пользователей работа с API доступна в режиме чтения, что-либо изменить или создать не получится.
- Алгоритм регистрации пользователей
    Пользователь отправляет POST-запрос на эндпоинт: /api/v1/auth/signup/
    - в body:
  ```
   {
   "email": "user@example.com",
   "username": "string"
   }
  ```

- на e-mail приходит письмо с кодом подтверждения (confirmation_code).
   Пользователь отправляет POST-запрос на эндпоинт: /api/v1/auth/token/
    - в body:
      ```
       {
       "username": "string",
       "confirmation_code": "string"
       }
      ```
       в ответе на запрос ему приходит token (JWT-токен).

## Пользовательские роли:
Аноним — может просматривать описания произведений, читать отзывы и комментарии.
Аутентифицированный пользователь (user) — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
Модератор (moderator) — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
Суперюзер Django — обладет правами администратора (admin)

## Примеры обращений к ресурсам:

 - Ресурс CATEGORIES Получить список всех категорий Права доступа: Доступно без токена
   GET: http://127.0.0.1:8000/api/v1/categories/
   - в body:
   ```
    {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [{}]
    }

 - Создать категорию. Права доступа: Администратор.
   POST: http://127.0.0.1:8000/api/v1/categories/
   - в body:
     ```
     {
     "name": "string",
     "slug": "string"
     }
     ```
- Удалить категорию. Права доступа: Администратор.
DELETE: http://127.0.0.1:8000/api/v1/categories/{slug}/

- Ресурс GENRES Получить список всех жанров. Права доступа: Доступно без токена
  GET: http://127.0.0.1:8000/api/v1/genres/
  - в body:
    ```
    {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [{}]
    }
    ```
- Добавить жанр. Права доступа: Администратор.
  POST: http://127.0.0.1:8000/api/v1/genres/
  - в body:
    ```
    {
    "name": "string",
    "slug": "string"
    }
    ```
- Удалить жанр. Права доступа: Администратор.
  DELETE: http://127.0.0.1:8000/api/v1/genres/{slug}/

- Ресурс TITLES Получить список всех произведений. Права доступа: Доступно без токена.
  GET: http://127.0.0.1:8000/api/v1/titles/
  - в body:
    ```
    {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [{}]
    }
    ```
- Добавить новое произведение. Права доступа: Администратор.
  POST: http://127.0.0.1:8000/api/v1/titles/
  - в body:
    ```
    {
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
    "string"
    ],
    "category": "string"
    }
    ```
- Информация о произведении Права доступа: Доступно без токена
  GET: http://127.0.0.1:8000/api/v1/titles/{titles_id}/
  - в body:
    ```
    {
    "id": 0,
    "name": "string",
    "year": 0,
    "rating": 0,
    "description": "string",
    "genre": [
    {}
    ],
    "category": {
    "name": "string",
    "slug": "string"
     }
    }
    ```
- Обновить информацию о произведении Права доступа: Администратор
  PATCH: http://127.0.0.1:8000/api/v1/titles/{titles_id}/
  - в body:
    ```
    {
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": ["string"],
    "category": "string"
    }
    ```

- Удалить произведение. Права доступа: Администратор.
  DELETE: http://127.0.0.1:8000/api/v1/titles/{titles_id}/

- Ресурс REVIEWS Получить список всех отзывов. Права доступа: Доступно без токена.
  GET: http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
  - в body:
    ```
    {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [{}]
    }
    ```

- Добавить новый отзыв. Пользователь может оставить только один отзыв на произведение.
  Права доступа: Аутентифицированные пользователи.
  POST: http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
  - в body:
    ```
    {
    "text": "string",
    "score": 1
    }
    ```

- Получить отзыв по id для указанного произведения. Права доступа: Доступно без токена.
  GET: http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
  - в body:
    ```
    {
    "id": 0,
    "text": "string",
    "author": "string",
    "score": 1,
    "pub_date": "2019-08-24T14:15:22Z"
    }
    ```
    
- Частично обновить отзыв по id. Права доступа: Автор отзыва, модератор или администратор.
  PATCH: http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
  - в body:
    ```
    {
    "text": "string",
    "score": 1
    }
    ```

- Удалить отзыв по id Права доступа: Автор отзыва, модератор или администратор.
  DELETE: http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/

- Ресурс COMMENTS:
  Получить список всех комментариев к отзыву по id Права доступа: Доступно без токена.
  GET: http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
  - в body:
    ```
    {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [{}]
    }
    ```
    
- Добавить новый комментарий для отзыва. Права доступа: Аутентифицированные пользователи.
  POST: http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
  - в body:
    ```
    {
    "text": "string"
    }
    ```

- Получить комментарий для отзыва по id. Права доступа: Доступно без токена.
  GET: http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
  - в body:
    ```
    {
    "id": 0,
    "text": "string",
    "author": "string",
    "pub_date": "2019-08-24T14:15:22Z"
    }
    ```
- Частично обновить комментарий к отзыву по id. Права доступа: Автор комментария, модератор или администратор.
  PATCH: http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
  - в body:
    ```
    {
    "text": "string"
    }
    ```
- Удалить комментарий к отзыву по id. Права доступа: Автор комментария, модератор или администратор.
  DELETE: http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/

- Ресурс USERS:
  Получить список всех пользователей. Права доступа: Администратор
  GET: http://127.0.0.1:8000/api/v1/users/
  - в body:
    ```
    {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [{}]
    }
    ```
- Добавить нового пользователя. Права доступа: Администратор
  POST: http://127.0.0.1:8000/api/v1/users/
  - в body:
    ```
    {
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
    }
    ```

- Получить пользователя по username. Права доступа: Администратор
  GET: http://127.0.0.1:8000/api/v1/users/{username}/
  - в body:
    ```
    {
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
    }
    ```
- Изменить данные пользователя по username. Права доступа: Администратор.
  PATCH: http://127.0.0.1:8000/api/v1/users/{username}/
  - в body:
    ```
    {
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
    }
    ```

- Удалить пользователя по username. Права доступа: Администратор.
  DELETE: http://127.0.0.1:8000/api/v1/users/{username}/

- Получить данные своей учетной записи Права доступа: Любой авторизованный пользователь
  GET: http://127.0.0.1:8000/api/v1/users/me/
  - в body:
    ```
    {
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
    }
    ```

- Изменить данные своей учетной записи Права доступа: Любой авторизованный пользователь
  PATCH: http://127.0.0.1:8000/api/v1/users/me/
  - в body:
    ```
    {
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string"
    }
    ```
### Автор Алексей Тен.
