"""Module of tasks for running sphinx"""
import os
import shutil
from pathlib import Path

from invoke import task

PROJECT_ROOT_DIR = Path(__file__).parent.parent
SOURCE_DIR = "docs/source"
BUILD_DIR = "docs/build"
SOURCE_GENERATED_DIR = SOURCE_DIR + "/apidoc-generated"
PORT = 8003


@task
def sync(command):  # pylint: disable=unused-argument
    """Copies the list of files to the docs/source/ folder
    The purpose is to include additional files in the documentation (such as README in root folder location).
    Note that the files will only be synced when you run a sphinx task, not if you only update the files in the project folder and then git commit.
    """
    files = [f"{PROJECT_ROOT_DIR}/README.md"]

    for source_file in files:
        shutil.copy2(source_file, PROJECT_ROOT_DIR / SOURCE_DIR)


@task(pre=[sync])
def build(command):
    if os.path.isdir(PROJECT_ROOT_DIR / BUILD_DIR):
        print("Removing 'build'")
        shutil.rmtree(PROJECT_ROOT_DIR / BUILD_DIR)

    if os.path.isdir(PROJECT_ROOT_DIR / SOURCE_GENERATED_DIR):
        print("Removing source/apidoc-generated")
        shutil.rmtree(PROJECT_ROOT_DIR / SOURCE_GENERATED_DIR)
    command.command_prefixes.insert(0, f"cd {PROJECT_ROOT_DIR}")
    command.run(f"sphinx-apidoc -feo {SOURCE_GENERATED_DIR} . -t {SOURCE_DIR}/_templates")
    command.run(f"sphinx-build {SOURCE_DIR} {BUILD_DIR}")
    # command.run(f"start {BUILD_DIR}/index.html")


@task(pre=[sync])
def livereload(command):
    """Start autobuild documentation server and open in browser.

    The documentation server will automatically rebuild the documentation and refresh your browser when you update it.
    """
    command.run(f"sphinx-autobuild {SOURCE_DIR} {SOURCE_DIR}/_build/html --open-browser --port {PORT}")


@task(pre=[sync])
def run(command):
    command.run(f"sphinx-autobuild {SOURCE_DIR} {SOURCE_DIR}/_build/html --host 0.0.0.0 --port {PORT}")


@task(pre=[build])
def test(command):
    """Checks for broken internal and external links and runs the doc8 .rst linter to identify problems.

    Runs
    - the Sphinx 'dummy' builder to identify internal problems.
    - the Sphinx 'linkcheck' build to identify broken external links.
    - doc8 linter to identify .rst syntax errors
    """
    print("\nRunning the 'dummy' builder")
    print("The input is only parsed and checked for consistency. This is useful for linting purposes.")
    command.run(f"sphinx-build {SOURCE_DIR} {SOURCE_DIR}/_build/ -b dummy", echo=True, warn=True)

    print("\nRunning the 'linkcheck' builder")
    print("echo This builder scans all documents for external links, tries to open them with requests")
    command.run(f"sphinx-build {SOURCE_DIR} {SOURCE_DIR}/_build/ -b linkcheck", echo=True, warn=True)

    print("\nRunning the 'doc8' linter to identify .rst syntax errors")
    command.run(f"doc8 {SOURCE_DIR}", echo=True, warn=True)
