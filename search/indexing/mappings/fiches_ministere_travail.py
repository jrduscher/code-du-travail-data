fiches_ministere_travail_mapping = {
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
        'text': {
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
        'questions': {
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
    },
}
