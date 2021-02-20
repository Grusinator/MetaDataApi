import os

from dotenv import load_dotenv
from invoke import task

path = "devops/kubernetes"

load_dotenv()
INITIALS = os.getenv("INITIALS")


@task
def replace_vars(command):
    for file in os.listdir(path):
        with open(file) as f:
            content = f.read()
            content.replace()


@task
def login(command, pw):
    command.run(f"az login -u adm{INITIALS}@orsted.dk -p {pw}")
    command.run(f"az aks get-credentials --resource-group E-ART-K8S-RG-DEV --name eart-green-aks-dev-we "
                f"--subscription E-ART --overwrite-existing")
