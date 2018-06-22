faq_mapping = {
    'properties': {
        'question': {
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
        'reponse': {
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
        'theme': {
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
        'branche': {
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
