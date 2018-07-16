all_mapping = {
    'properties': {
        'source': {
            'type': 'text',
            'analyzer': 'keyword',
        },
        'url': {
            'type': 'text',
            'analyzer': 'keyword',
        },
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
        # Currently only available for `Code du travail`.
        'path': {
            'type': 'text',
            'analyzer': 'path_analyzer_custom',
            'fielddata': True,
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
        # Currently only available for `Fiches service public`.
        'tags': {
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
