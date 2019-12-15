$apps = ("text", "boolean", "temporal", "file", "numeric", "related")
$apps | ForEach-Object {
    pipenv run python manage.py migrate $_ --fake 0001
    pipenv run python manage.py migrate $_
}
