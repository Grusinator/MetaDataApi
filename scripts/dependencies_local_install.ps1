
$django_generic_serializer_filename = Get-ChildItem -Path .\lib\ -Name -Include django_generic_serializer*
$django_json2model_filename = Get-ChildItem -Path .\lib\ -Name -Include django_json2model*

pipenv uninstall django_generic_serializer django_json2model

pipenv install .\lib\$django_json2model_filename .\lib\$django_generic_serializer_filename
