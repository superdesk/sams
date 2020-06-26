"""
**schema** =
``_id`` *string*
    Destination name
``provider` *string*
    Destination's Provider name
"""

destinationSchema = {
    '_id': {
        'type': 'string',
        'unique': True
    },
    'provider': {
        'type': 'string'
    }
}
