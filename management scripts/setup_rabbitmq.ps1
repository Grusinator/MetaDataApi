rabbitmqctl add_user django dev1234
rabbitmqctl add_vhost meta_data_api
rabbitmqctl set_permissions -p meta_data_api django ".*" ".*" ".*"
rabbitmq-plugins enable rabbitmq_management
rabbitmqctl set_user_tags django administrator