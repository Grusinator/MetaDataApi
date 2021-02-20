from invoke import task
from sqlalchemy import MetaData

from optisoil.db_client.direct_db_optisoil_client import OptisoilDbClient

object_file_path = "optisoil/db_client/objects/objects.py"

@task
def create_tables(command):
    meta = MetaData()

    from optisoil.db_client.objects import bases, tables
    temp = [tables, bases]
    client = OptisoilDbClient()

    meta.create_all(client.engine)


@task
def generate_code(command):
    client = OptisoilDbClient()
    db_url = client._create_connection_string()
    command.run(f"sqlacodegen {db_url}")
