
install:
	poetry install

dev:
	poetry run python manage.py runserver

PORT ?= 8000
start:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) app.wsgi

migrations:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

test:
	poetry run python manage.py test

lint:
	flake8 app

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage xml --include=app/* --omit=app/settings.py

create-locale-ru-ru:
    poetry run manage.py makemessages -l ru_RU

compile-locale:
    poetry run manage.py compilemessages
