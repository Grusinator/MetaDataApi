sudo service postgresql start
sudo service redis-server start

sh start_celery_worker.sh
sh start_celery_beat.sh
# sudo /etc/init.d/redis-server stop
# pg_ctl -D /usr/local/var/postgres stop
# redis-cli shutdown
