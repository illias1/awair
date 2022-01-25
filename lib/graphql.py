import os
import requests
from dotenv import load_dotenv

load_dotenv()

HASURA_ADMIN_SECRET = os.environ.get('HASURA_ADMIN_SECRET')
headers = {'x-hasura-admin-secret': HASURA_ADMIN_SECRET}
graphql_url = 'https://square-ox-76.hasura.app/v1/graphql'


def graphql(query, variables):
    try:
        graphql_request = requests.post(
            graphql_url,
            json={'query': query, 'variables': variables},
            headers=headers
        )
        response = graphql_request.json()
        return True, response
    except Exception as e:
        return False, e
