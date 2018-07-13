faq_mapping = {
    'properties': {
        'title': {
            'type': 'text',
            'analyzer': 'standard',
            'fields': {
                'french_heavy': {
                    'type': 'text',
                    'analyzer': 'french_heavy'
                },
                'french_light': {
                    'type': 'text',
                    'analyzer': 'french_light'
                },
                'edge_ngram': {
                    'type': 'text',
                    'analyzer': 'edge_ngram_custom'
                },
            },
        },
        'text': {
            'type': 'text',
            'analyzer': 'standard',
            'fields': {
                'french_heavy': {
                    'type': 'text',
                    'analyzer': 'french_heavy'
                },
                'french_light': {
                    'type': 'text',
                    'analyzer': 'french_light'
                },
                'edge_ngram': {
                    'type': 'text',
                    'analyzer': 'edge_ngram_custom'
                },
            },
        },
    },
}
