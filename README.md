# Проект "Предсказание рисков сердечного приступа" (DS-48-расширенный, Мастерская 1)

## Описание

Данный репозиторий представляет собой проект по разработке модели машинного обучения, предназначенной для оценки вероятности возникновения сердечного приступа у пациентов. В рамках проекта мы планируем реализовать следующую функциональность:

- Разработка ML-модели для классификации рисков сердечных заболеваний.
- Создание библиотеки функций для удобного взаимодействия с моделью.
- Реализация интерфейса для тестирования модели на новых наборах данных.

Цель проекта — создание инструмента, способного эффективно помогать медицинским специалистам выявлять риски сердечно-сосудистых патологий среди различных групп населения.

---

## Оглавление

[Установка](#установка)

[Структура проекта](#структура-проекта)

[Описание API](#описание-api)

[Тестирование API](#тестирование-api)

## Установка

Для начала работы с проектом выполните следующие шаги:

### Клонирование репозитория

```bash
git clone https://github.com/Golden-Gekko/workshop_1.git
cd workshop_1
```

### Настройка виртуального окружения Python

Рекомендуется использовать виртуальные среды для изоляции зависимостей проекта. Вы можете воспользоваться venv следующим образом:

```bash
# Для Linux/macOS
python3 -m venv env 
source env/bin/activate 
```

```bash
# Для Windows
python -m venv env 
env\Scripts\activate
```

Далее установите необходимые зависимости командой:

```bash
pip install -r requirements.txt
```

[к оглавлению](#оглавление)

## Структура проекта

Проект имеет следующую иерархию каталогов и файлов:

```
.
├── app                         # Веб-приложение на FastAPI + Jinja2
│ ├── api                       # Пакет с API функционалом
│ │ ├── nn_module.py            # Модуль с определением нейронной сети
│ │ ├── pt_models.py            # Загрузка и работа с PyTorch моделями
│ │ ├── router.py               # Обработчики запросов (маршрутизация)
│ │ └── schemas.py              # Определение схем данных для моделей
│ ├── static                    # Статические ресурсы приложения
│ │ ├── icon                    # Иконка сердца
│ │ │ └── heart_icon.png        
│ │ ├── js                      # Файлы JavaScript
│ │ │ └── script.js             
│ │ ├── models                  # Директория с натренированными моделями
│ │ │ └── jit_model_230625_1141.pt  # Модель PyTorch, преобразованная в torch.jit
│ │ └── style                   # Файлы CSS
│ │   └── style.css            
│ ├── templates                 # Шаблоны страниц
│ │ └── index.html
│ ├── main.py                   # Точка входа приложения (FastAPI)
│ └── settings.py               # Конфигурация приложения
├── source                      # Источники данных
│ ├── heart_test.csv            # Тестовая выборка
│ ├── heart_test_predict.csv    # Предсказанные значения для теста
│ └── heart_train.csv           # Тренировочная выборка
├── model_training.ipynb        # Блокнот с процессом подготовки и обучения модели
├── requirements.txt            # Список требований и зависимостей
└── README.md
```

### Детали структуры:

- **data.csv**: основной набор данных для тренировки модели.
- **model.ipynb**: рабочий блокнот с кодом разработки и проверки модели.
- **app/**: Корневой каталог приложения. Содержит логику веб-серверной части
  - **api/**: маршруты и контроллеры API.
  - **static/**: статичные файлы вроде стилей и скриптов.
  - **templates/**: шаблоны HTML-разметки для рендеринга страниц.
  - **main.py**: главный модуль запуска приложения.
  - **settings.py**: конфигурационные настройки проекта.
- **source/**: дополнительные файлы и вспомогательные инструменты, такие как наборы данных и утилиты предобработки.

[к оглавлению](#оглавление)

## Описание API

### Получение предсказания риска сердечного приступа

**Endpoint:** `/api/get_prediction/`

**Метод:** `POST`

#### Формат входных данных:
| Поле | Тип | Описание |
|---|---|---|
| diabetes | bool | Наличие диабета |
| family_history | bool | Заболевания в семье |
| obesity | bool | У пациента ожирение |
| alcohol_consumption | bool | Пациент употребляет алкоголь |
| previous_heart_problems | bool | Проблемы с сердцем ранее |
| medication_use | bool | Принимает препараты |
| diet | int | Тип диеты (от 0 до 2) |
| stress_level | int | Уровень стресса (от 1 до 10) |
| physical_activity_days_per_week | int | Количество дней физической активности в неделю (от 0 до 7) |
| age | float | Возраст пациента (нормализованное значение от 0 до 1) |
| cholesterol | float | Уровень холестерина (нормализованное значение от 0 до 1) |
| heart_rate | float | Пульс (нормализованное значение от 0 до 1) |
| exercise_hours_per_week | float | Часы занятий спортом в неделю (нормализованное значение от 0 до 1) |
| sedentary_hours_per_day | float | Часы пассивного образа жизни в день (нормализованное значение от 0 до 1) |
| bmi | float | Индекс массы тела (ИМТ), нормализованный от 0 до 1 |
| triglycerides | float | Уровень триглицеридов (нормализованное значение от 0 до 1) |
| sleep_hours_per_day | float | Продолжительность сна в сутки (нормализованное значение от 0 до 1) |
| blood_sugar | float | Уровень глюкозы в крови (нормализованное значение от 0 до 1) |
| ck_mb | float | Уровень фермента креатинкиназы (нормализованное значение от 0 до 1) |
| troponin | float | Уровень тропонина (нормализованное значение от 0 до 1) |
| systolic_blood_pressure | float | Систолическое артериальное давление (нормализованное значение от 0 до 1) |
| diastolic_blood_pressure | float | Диастолическое артериальное давление (нормализованное значение от 0 до 1) |

Пример JSON-запроса:

```
{
  "diabetes": true,
  "family_history": false,
  "obesity": true,
  "alcohol_consumption": false,
  "previous_heart_problems": true,
  "medication_use": true,
  "diet": 1,
  "stress_level": 8,
  "physical_activity_days_per_week": 3,
  "age": 0.5,
  "cholesterol": 0.6,
  "heart_rate": 0.7,
  "exercise_hours_per_week": 0.3,
  "sedentary_hours_per_day": 0.8,
  "bmi": 0.75,
  "triglycerides": 0.5,
  "sleep_hours_per_day": 0.6,
  "blood_sugar": 0.4,
  "ck_mb": 0.3,
  "troponin": 0.2,
  "systolic_blood_pressure": 0.65,
  "diastolic_blood_pressure": 0.45
}
```

#### Формат выходных данных

JSON-ответ содержит вероятность развития сердечного приступа, выраженную в процентах:

```
{
  "predict": 85.2
}
```

### Получение нескольких предсказаний одновременно

**Endpoint:** `/api/get_predictions/`

**Метод:** `POST`

#### Формат входных данных:

Запрос должен содержать CSV-файл с набором записей для предсказания.
Каждый ряд файла должен соответствовать формату, приведенному [для одного предсказания](#формат-входных-данных)

#### Формат выходных данных

API вернет массив объектов JSON, каждый объект соответствует одной строке входного CSV и содержит одно предсказанное значение риска сердечного приступа в процентах.

```
[
  {
    "id": "1",
    "predict": 85.2
  },
  {
    "id": "2",
    "predict": 12.4
  }
]
```

[к оглавлению](#оглавление)

## Тестирование API

Для удобства тестирования реализован Web-интерфейс, позволяющий получить как одно, так и множество предсказаний.

Сервер приложения запускается с помощью команды uvicorn. Полный синтаксис команды с дополнительными параметрами:

```
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Параметры команды:
- `app.main:app`: Указывает путь к основному приложению. Здесь app — название пакета, main — имя модуля внутри пакета, а app — экземпляр FastAPI.
- `--host 0.0.0.0`: Позволяет серверу прослушивать запросы извне (актуально при размещении сервиса в локальной сети).
- `--port 8000`: Определяет порт, на котором будет запущен сервер. По умолчанию используется порт 8000.
- `--reload`: Включает режим автоматического перезапуска сервера при изменении файлов проекта. Это полезно во время разработки, так как изменения автоматически применяются без необходимости вручную перезагружать сервер.

Пример команд для запуска в разных сценариях:
- **Разработка с автоматическим обновлением**
```
uvicorn app.main:app --reload
```
- **Продуктивное использование на публичном IP**
```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
- **Изменение порта на нестандартный (например, 8080)**
```
uvicorn app.main:app --port 8080
```

[к оглавлению](#оглавление)
