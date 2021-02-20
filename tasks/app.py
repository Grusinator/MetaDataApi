from invoke import task


@task
def setup_py(command):
    command_string = "python setup.py bdist_wheel"
    command.run(command_string, echo=True)


@task
def run(command):
    # for somehow reason streamlit does not want to import from optisoil when the path has not been set
    command.run("streamlit run optisoil/app/optisoil_engineering_tools.py")
