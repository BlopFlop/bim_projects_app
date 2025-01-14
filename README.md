# BIM Projects APP

## О проекте

**Цели:** 

Основные функции:

- **None**

## DataModel Сюда ссылку :)

## Стек :)
- Python
- FastAPI
- Выбрать Брокера сообщенй
- PostgreSQL

## Настройка

### Репозиторий
- Базовая рабочая ветка - develop. Здесь располагается "чистый" основной рабочий код после ревью. Все остальные ветки создаем только от нее
**Все объединения проводятся исключительно через Pull requests**
- ‼️ Ветка `master` - ветка для чистого кода, подготовленного к деплою на сервер.
- Правила именования веток:
  - `feature/<краткое описание>` - для веток, реализующих основной и дополнительный функционал ТЗ
  - `fix/<краткое описание>` - для веток, исправляющих или дополняющие уже реализованный функционал


### Настройка после клонирования репозитория

После клонирования репозиторий имеет следующую структуру:

```
bim_projects_app
│
├── infra/                              Каталог с файлами инфраструктуры
│   ├── env.example                     Пример конфигурационного файла
│   └── dev-docker-compose.yml          Настройки для docker compose
│
├── src/                                Каталог с файлами проекта
|   └── __init__.py
│   └── main.py                         Основной запускаемый файл проекта
│   └── admin/                          Админка
│   └── core/                           Настройки проекта
|   |   └── __init__.py
|   |   └── base.py                     Настройки бд
|   |   └── config.py                   Конфигурация проекта
|   |   └── db.py                       Настройки бд
|   └── utils/                          Вспомогательный модуль
│
├── tests/                              Тестирование
|   └── conftest.py                     Тестовые компоненты
│
├── .gitignore                          Что игнорировать в Git
├── requirements.txt                    Основные зависимости проекта
├── requirements_style.txt              Зависимости для стилизации кода
├── .pre-commit-config.yaml             Настройки для проверок перед комитом
├── style.cfg                           Настройки для isort и flake8
├── black.cfg                           Настройки для black
└── README.md                           Этот файл
```

**Устанавливаем и активируем виртуальное окружение**

```shell
python3.11 -m venv .venv
source .venv/bin/activate
```

Устанавливаем зависимости
```shell
pip install -r requirements.txt
pip install -r requirements_style.txt
```

Настраиваем `pre-commit`

```shell
pre-commit install
```

Проверяем, что `pre-commit` работает корректно

```shell
pre-commit run --all-files
```

Возможно потребуется запуск несколько раз. В итоге должен получиться примерно такой вывод:

```shell
trim trailing whitespace............Passed
fix end of files....................Passed
check yaml..........................Passed
check for added large files.........Passed
check for merge conflicts...........Passed
isort...............................Passed
flake8..............................Passed
black...............................Passed
```
#Запуск проекта
Пример .env
POSTGRES_USER=your_db_username # Заменить
POSTGRES_PASSWORD=your_db_password # Заменить
POSTGRES_DB=bim_projects_app
POSTGRES_SERVER=localhost # Изменить на название контейнера с БД в Docker Compose
POSTGRES_PORT=5432
```
Добавить папку src в рабочую директорию
```
```
Перейти в папку src
```
cd src
```
Запустить проект через терминал командой
```
python main.py
```
Для развертывания проетка локально на своем пк перейдите в папку infra
```
cd ..
cd infra
```
Запустите docker compose
```
docker compose up
```
Для развертывания на сервере необходимо запушить изменеия в ветку main и он автоматически развернется
