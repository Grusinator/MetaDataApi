docker cp ./scripts/ metadataapi_db:/scripts
# docker exec -it metadataapi_db chmod +x /scripts/*.sh

docker exec -it metadataapi_db /scripts/db_recreate.sh

#docker exec -it meta_data_api_db psql -h localhost -p 5432 -U django -d  "meta_data_api"  -f ./scripts/db_recreate.sql

docker exec -it metadataapi_django ./scripts/db_setup.sh
