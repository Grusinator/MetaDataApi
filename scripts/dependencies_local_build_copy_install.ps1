Remove-Item "lib\*.whl"

Set-Location ..\django-generic-serializer
Remove-Item "dist\*.whl"
python setup.py bdist_wheel
Copy-Item  dist\django_generic_serializer-*.whl ..\MetaDataApi\lib\

Set-Location ..\django-json2model
Remove-Item "dist\*.whl"
python setup.py bdist_wheel
Copy-Item dist\django_json2model-*.whl ..\MetaDataApi\lib\

Set-Location ..\MetaDataApi

$django_generic_serializer_filename = Get-ChildItem -Path .\lib\ -Name -Include django_generic_serializer*
$django_json2model_filename = Get-ChildItem -Path .\lib\ -Name -Include django_json2model*

pipenv uninstall django_generic_serializer django_json2model

pipenv install .\lib\$django_json2model_filename .\lib\$django_generic_serializer_filename
