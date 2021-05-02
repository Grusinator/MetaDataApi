pipenv run python -m coverage run .\manage.py test
pipenv run python -m coverage xml -i
python-codacy-coverage -r coverage.xml