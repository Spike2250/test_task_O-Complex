[![check](https://github.com/Spike2250/test_task_O-Complex/actions/workflows/CI.yml/badge.svg)](https://github.com/Spike2250/test_task_O-Complex/actions/workflows/CI.yml)

### Hosted
[link](https://test-task-o-complex.onrender.com/) on Render.com

## Тестовое задание

### вакансия - [Junior Python Разработчик](https://perm.hh.ru/vacancy/120908042) О-комплекс

### Текст задания:

Сделать web приложение, оно же сайт, где пользователь вводит название города, и получает прогноз погоды в этом городе на ближайшее время.

 - :heavy_check_mark: Вывод данных (прогноза погоды) должен быть в удобно читаемом формате.
 - :heavy_check_mark: Веб фреймворк можно использовать любой.
   - Использовал Django
 - :heavy_check_mark: api для погоды: https://open-meteo.com/ (можно использовать какое-нибудь другое, если вам удобнее)
   - Использовал [OpenWeatherMap](https://openweathermap.org/)
 
будет плюсом если:
- :heavy_check_mark: написаны тесты 
- :x: всё это помещено в докер контейнер
- :x: сделаны автодополнение (подсказки) при вводе города
- :x: при повторном посещении сайта будет предложено посмотреть погоду в городе, в котором пользователь уже смотрел ранее
- :heavy_check_mark: будет сохраняться история поиска для каждого пользователя, и будет API, показывающее сколько раз вводили какой город

что будет оцениваться:
- корректность работы
- удобство использования
- качество кода

в README.md просьба указать что из выше перечисленного было сделанно, пару слов о использованных технологиях, и как это всё запустит

## Запуск
### Клонировать репозиторий
```bash
git clone https://github.com/Spike2250/test_task_O-Complex.git
```
### Переменные среды
Создать .env файл по образцу [.env.template](https://github.com/Spike2250/test_task_O-Complex/blob/master/.env.template)
### Установка
```bash
poetry install
```
или
```bash
make install
```
### Запуск
```bash
poetry run python manage.py makemigrations
poetry run python manage.py migrate
poetry run python manage.py runserver
```
или
```bash
make start
```