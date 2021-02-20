"""Module of Invoke tasks regarding docker builds to be invoked from the command line. Try

invoke --list

from the command line for a list of all available commands.
"""

import os

from dotenv import load_dotenv
from invoke import task

docker_files_path = ".\\devops\\docker\\"

load_dotenv()

# remember to set APP_NAME in env vars in the pipeline
app_image_name = os.getenv("APP_NAME")
base_image_name = app_image_name + "-base"
docs_image_name = app_image_name + "-docs"
ACR = os.getenv("ACR")
INITIALS = os.getenv("INITIALS")


@task
def acr_login(command):
    command.run(f"az acr login --name {ACR}")


@task(pre=[acr_login])
def build_base(command):
    docker_file = build_docker_file_path("base")
    command.run(f"docker build . -t {base_image_name}:latest -f {docker_file}", echo=True)


@task(pre=[acr_login])
def build(command):
    docker_file = build_docker_file_path("app")
    command.run(f"docker build . -t {app_image_name}:latest -f {docker_file}", echo=True)


@task(pre=[acr_login])
def build_docs(command):
    docker_file = build_docker_file_path("docs")
    # command.run(f"docker pull {ACR}/{docs_image_name}:20210212.1")
    command.run(f"docker build . -t {docs_image_name}:latest -f {docker_file}", echo=True)
    # --cache-from {ACR}/{docs_image_name}:20210212.1"


@task
def run_docs(command, name=docs_image_name, port=8003):
    remove_docker_container(command, name)
    run_docker_container(command, name, port)


@task
def run_test(command, name=app_image_name, port=8501):
    remove_docker_container(command, name)
    run_docker_container(command, name, port, docker_command="python -m pytest")


@task
def run(command, name=app_image_name, port=8501):
    remove_docker_container(command, name)
    run_docker_container(command, name, port)


def remove_docker_container(command, name):
    try:
        command.run(f"docker container stop {name}")
    except:
        pass
    try:
        command.run(f"docker container rm {name}")
    except:
        pass


def run_docker_container(command, name, port, docker_command=""):
    command.run(f"docker run --name {name} -p {port}:{port} {name} {docker_command}", echo=True)


def build_docker_file_path(name):
    return f"{docker_files_path}{name}.Dockerfile"
