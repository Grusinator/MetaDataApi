find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
rm db.sqlite3
sudo -u postgres -H -- psql -d "meta_data_api" -c\
"DROP SCHEMA public CASCADE; \
CREATE SCHEMA public; \
"
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate