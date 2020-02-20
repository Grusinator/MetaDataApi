# settings.py
import os
from os.path import join, dirname

from dotenv import load_dotenv


def load_env(base_dir=None):
    base_dir = base_dir or dirname(__file__)
    dotenv_path = join(base_dir, '.env')
    load_dotenv(dotenv_path)


def get_env_var(env_name: str, default=None):
    return os.environ.get(env_name)
