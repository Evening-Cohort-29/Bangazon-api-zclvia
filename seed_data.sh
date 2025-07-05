#!/bin/bash

rm -rf bangazonapi/migrations
rm db.sqlite3
poetry run python manage.py makemigrations bangazonapi
poetry run python manage.py migrate
poetry run python manage.py loaddata users
poetry run python manage.py loaddata tokens
poetry run python manage.py loaddata customers
poetry run python manage.py loaddata stores
poetry run python manage.py loaddata product_category
poetry run python manage.py loaddata product
poetry run python manage.py loaddata productrating
poetry run python manage.py loaddata payment
poetry run python manage.py loaddata order
poetry run python manage.py loaddata order_product
poetry run python manage.py loaddata favoritesellers
