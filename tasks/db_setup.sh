echo $DOCKER
[ "$DOCKER" = 1 ] &&
  python manage.py migrate ||
  pipenv run python manage.py migrate

[ "$DOCKER" = 1 ] &&
  python manage.py shell < ./tasks/create_default_super_user.py ||
  pipenv run python manage.py shell  < ./tasks/create_default_super_user.py
