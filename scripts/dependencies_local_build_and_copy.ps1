del "lib\*.whl"

cd ..\django-generic-serializer
del "dist\*.whl"
python setup.py bdist_wheel
cp dist\django_generic_serializer-*.whl ..\MetaDataApi\lib\

cd ..\django-json2model
del "dist\*.whl"
python setup.py bdist_wheel
cp dist\django_json2model-*.whl ..\MetaDataApi\lib\

cd ..\MetaDataApi

