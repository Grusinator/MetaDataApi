export PGPASSWORD="dev1234"
psql -h localhost -p 5432 -U django -d  "meta_data_api"  -f ./scripts/db_recreate.sql