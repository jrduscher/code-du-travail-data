fiches_service_public_mapping = {
    'properties': {
        'url': {
            'type': 'text',
            'analyzer': 'keyword',
        },
        'title': {
            'type': 'text',
            'analyzer': 'standard',
            'fields': {
                'edge_ngram': {
                    'type': 'text',
                    'analyzer': 'edge_ngram_custom'
                },
                'french': {
                    'type': 'text',
                    'analyzer': 'french_custom'
                },
            },
        },
        'tags': {
            'type': 'text',
            'analyzer': 'standard',
            'fields': {
                'edge_ngram': {
                    'type': 'text',
                    'analyzer': 'edge_ngram_custom'
                },
                'french': {
                    'type': 'text',
                    'analyzer': 'french_custom'
                },
            },
        },
        'refs_sujets': {
            'type': 'text',
            'analyzer': 'standard',
        },
        'refs_sources': {
            'type': 'text',
            'analyzer': 'standard',
        },
    },
}
