from aegis_db import AegisDB

schema = {
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string'
        },
        'age': {
            'type': 'integer'
        }
    },
    'required': ['name']
}

db = AegisDB()

print('Hello')