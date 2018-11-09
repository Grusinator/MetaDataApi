# %%
from gql.transport.requests import RequestsHTTPTransport
from gql import gql, Client

# %%
_transport = RequestsHTTPTransport(
    url='https://graphql-pokemon.now.sh/',
    use_json=True,

)


client = Client(
    transport=_transport,
    fetch_schema_from_transport=True,
)
query = gql("""
{
    pokemon(name: "Pikachu") {
        attacks {
            special {
                name
            }
        }
    }
}
""")

res = client.execute(query)
