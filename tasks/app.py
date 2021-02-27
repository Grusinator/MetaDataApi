from invoke import task


@task
def setup_py(command):
    command_string = "python setup.py bdist_wheel"
    command.run(command_string, echo=True)


@task
def run(command):
    command.run("python3 /code/manage.py migrate --noinput && python3 /code/manage.py runserver 0.0.0.0:80")
