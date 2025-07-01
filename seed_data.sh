#!/bin/bash

rm -rf bangazonapi/migrations
rm db.sqlite3
python manage.py makemigrations bangazonapi
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata customers
python manage.py loaddata product_category
python manage.py loaddata product
python manage.py loaddata productrating
python manage.py loaddata payment
python manage.py loaddata order
python manage.py loaddata order_product
python manage.py loaddata favoritesellers
