pipenv run celery -A MetaDataApi flower `
--port = 5555 --address = 0.0.0.0 `
--basic_auth = admin: admin_pass `
--broker = amqp: //django:dev1234@localhost: 5672/meta_data_api
