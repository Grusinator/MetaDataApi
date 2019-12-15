$env:PGPASSWORD = "dev1234"
psql -h localhost -p 5432 -U django -d  "meta_data_api"  -f .\scripts\delete_and_create_database.sql

pipenv run python manage.py migrate

manage.py createsuperuser2 --username django --password dev1234 --noinput

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'password')" |
        pipenv run python manage.py shell
