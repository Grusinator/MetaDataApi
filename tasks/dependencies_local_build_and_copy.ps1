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