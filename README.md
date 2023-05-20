# 😽 QRKot - Благотворительный фонд поддержки бездомных котиков

<img alt="Python" src="https://img.shields.io/badge/Python-3.8-blue?style=flat&logo=python"> <img alt="Python" src="https://img.shields.io/badge/FastAPI-0.78-blue?style=flat&logo=fastapi">

## Содержание

- [Описание](#-описание)
- [Технологии](#%EF%B8%8F-технологии)
- [Запуск проекта](#%EF%B8%8F-запуск-проекта)
- [Документация](#документация)
- [Вклад](#вклад)
- [Лицензия](#%EF%B8%8F-лицензия)
- [Контактная информация](#-контактная-информация)


## 📖 Описание
`QRKot` представляет собой API благотворительного фонда поддержки бездомных животных.
В рамках проекта мы собираем средства на помощь бездомным котикам, а также на
их содержание в приютах. В приложении можно просматривать список благотворительных
проектов, регистрироваться, вносить пожертвования, пользователи могут просматривать свои
пожертвования. Администраторы могут создавать новые проекты, просматривать список пожертвований и
редактировать других пользователей, выгружать топ проектов по скорости сбора средств в 
Google Таблицы.

При первом запуске приложения суперпользователь создается автоматически.

## ⚙️ Технологии

- [Python 3.9](https://www.python.org/downloads/release/python-390/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Google Sheets API](https://developers.google.com/sheets/api)

## 🛠️ Запуск проекта

###### 📣 Перед установкой этого проекта, убедитесь что у вас установлен Python (3.9+)

1. Склонируйте репозиторий на локальную машину

```sh
git clone https://github.com/spaut33/cat_charity_fund.git
```

2. Создайте виртуальное окружение и активируйте его

```sh
python -m venv .venv
```
```shell
source .venv/bin/activate
```

3. Установите зависимости

```sh
pip install -r requirements.txt
```

4. Создайте файл .env и заполните его своими значениями

```sh
cp .env.example .env
```

5. Создайте базу данных, применив миграции

```sh
alembic upgrade head
```

6. Запустите проект

```sh
python -m uvicorn app.main:app --reload
```
<p align="right"><a href="#top">⬆️ Наверх</a></p>

## Документация

Документация доступна после запуска адресу http://127.0.0.1:8000/docs

## Вклад

Если вы хотите сделать вклад в этот проект, свяжитесь со мной. Контактная информация есть ниже.

## ⚠️ Лицензия

<a href="https://img.shields.io/badge/License-MIT-brightgreen?style=flat"><img alt="M.I.T. License use" src="https://img.shields.io/badge/License-MIT-brightgreen"></a>

## ‍💻 Контактная информация

[Роман Петраков @ github](https://github.com/spaut33)

<p align="right"><a href="#top">⬆️ Наверх</a></p>
