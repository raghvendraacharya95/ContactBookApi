from flask_restplus import Api

from .auth import api as ns1
from .manage_contact_book import api as ns2
from .search_contact import api as ns3
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

api = Api(
    title='API For Contact Book App',
    version='1.0',
    description='Plivo Assignment',
    authorizations=authorizations
    # All API metadatas
)

api.add_namespace(ns1)
api.add_namespace(ns2)
api.add_namespace(ns3)