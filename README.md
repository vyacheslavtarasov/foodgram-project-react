# Проект Foodgram

[![Python](https://img.shields.io/badge/Python-%203.9-6495ED?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-%203.2-6495ED?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![Pytest](https://img.shields.io/badge/Pytest-6.2.4-6495ED?style=flat-square&logo=pytest-)](https://docs.pytest.org/en/6.2.x/)


## Описание:
Проект Foodgram хранит и систематизирует рецепты. 
Позволяет создавать новые рецепты, подписываться на авторов и сохранять список ингредиентов выбранных рецептом как список покупок.


## Функционал

- Проект Foodgram позволяет создавать рецепты блюд каждому зарегистрированому пользователю;
- Каждому блюду могут быть выставлены теги для удобства поиска;
- Добавлять ингредиенты для составления рецептов и теги может только администратор.
- Пользователь может подписываться на других пользователей, чтобы смотреть их рецепты;
- Поользователь может скачать список ингредиентов из выбранных рецептов, как список для покупок;
- Пользователь может заносить рецепты в избраное.
- Размер фото приготовленного блюда не должен превышать 1Mb.


## Локальный запуск сайта
Установите платформу Docker (c wsl2.0 для Windows) с сайта:
```
https://docs.docker.com/desktop/
```
Запустите процесс-сервис платформы Docker:
```
Для Linux - sudo systemctl start docker
Для Windows - запустите приложение Docker из места установки
```
Клонируйте репозиторий.
```
git clone git@github.com:vyacheslavtarasov/foodgram-project-react.git
```
Перейдите парку infra, склонированного репозитория.    
Создйте и заполните там файл ".env" по примеру файла ".env.example" (уже лежащего в папке).   
Запустите разворачивание сайта на локальной платфоре Docker и дождаться завершения.   
```
docker-compose up
```
Зайдите на контейнер бекенда в докере через командную строку или чрезе UI докер клиента.
```
docker exec -it infra-backend-1 bash
```
Выполните миграции:
```
python3 manage.py migrate
```
Загрузите начальные данные в базу.
```
python manage.py dbdataimport
```
Создайте супер пользователя:
```
python3 manage.py makeadminsuperuser
```

Сайт будет доступен по адресу http://localhost:9000/   
Админ зона http://localhost:9000/admin/   
Суперпользователь:   
 - Имя - admin
 - Пароль - admin123admin


## Разработка и тестирование API
Разработку и тестирование API удобно осуществлять локально при помоищи встроенного Django сервера.   
Для этого надо:   

Клонировать репозиторий.
```
git clone git@github.com:vyacheslavtarasov/foodgram-project-react.git
```
Перейти в папку проекта backend.  
Cоздать виртуальное окружение.
```
python3 -m venv env
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Перейти в папку проекта foodgram.  
В настройках django проекта (foodgram.settings.py) изменить базу на локальную db.sqlite3. (раскомментить секцию DATABASES)
Выполнить миграции:
```
python3 manage.py migrate
```
Загрузить начальные данные в базу.
```
python manage.py dbdataimport
```
Запустить проект.
```
python manage.py runserver
```
API будет доступа по адресу http://localhost:9000/  


## Поддержка развёрнутого в интеренете проекта.
Сайт и API развёрнуты и доступны в интернете по адресу https://practicum16aihal21.ddns.net/  
Для осуществления поддержки развёрнутого со своей машины необходимо:  
Склонировать репозиторий на свой аккаунт GitHub  
```
https://github.com/vyacheslavtarasov/foodgram-project-react
```
Заполнить секретные переменные (foodgram-project-react/settings/secrets/actions) на сайте github в своём склонированном репозитории.  
Имена переменных докер репозитория, которые нужно заполнить:  
``` 
- secrets.DOCKER_USERNAME
- secrets.DOCKER_PASSWORD
Параметры доступа к серверу:  
- secrets.HOST
- secrets.USER
- secrets.SSH_KEY
- secrets.SSH_PASSPHRASE
```
Клонировать репозиторий.
```
git clone git@github.com:vyacheslavtarasov/foodgram-project-react.git
```
Внести необходимые правки, проверить их локально любым удобным способом.   
Залить обратно в репозиторий git.



## Автор проекта:
- [Vyacheslav Tarasov](https://github.com/vyacheslavtarasov)
