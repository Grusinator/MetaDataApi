import subprocess

from invoke import task


@task
def start_celery_worker(c):
    cmd = ["pipenv", "run", "celery", "-A", "MetaDataApi", "-l", "INFO", "worker", "-P", "eventlet"]
    subprocess.run(cmd)
