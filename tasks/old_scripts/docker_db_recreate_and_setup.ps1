docker cp ./scripts/ metadataapi_db:/scripts
docker cp ./scripts/ metadataapi_django:/scripts
# docker exec -it metadataapi_db chmod +x /scripts/*.sh

docker exec -it metadataapi_db bash /scripts/db_recreate.sh
docker exec -it metadataapi_django bash ./scripts/db_setup.sh
