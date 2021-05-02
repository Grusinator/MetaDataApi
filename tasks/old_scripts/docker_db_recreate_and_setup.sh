docker cp ./tasks/ metadataapi_db:/tasks/

docker exec -it metadataapi_db bash ./tasks/db_recreate.sh

#docker exec -it meta_data_api_db psql -h localhost -p 5432 -U django -d  "meta_data_api"  -f ./tasks/db_recreate.sql

docker exec -it metadataapi_django bash ./tasks/db_setup.sh
