code_du_travail_numerique_mapping = {
    'properties': {
        # Indicates the origin of the document, e.g. 'code_du_travail', 'fiches_service_public' etc.
        'source': {
            'type': 'text',
            'analyzer': 'keyword',
        },
        'url': {
            'type': 'text',
            'analyzer': 'keyword',
        },
        # A field that concatenate `title` and `text` fields.
        'all_text': {
            'type': 'text',
            'analyzer': 'standard',
            'store': True,
            'fields': {
                'french_heavy': {
                    'type': 'text',
                    'analyzer': 'french_heavy',
                },
                'french_light': {
                    'type': 'text',
                    'analyzer': 'french_light',
                },
            },
        },
        'title': {
            'type': 'text',
            'analyzer': 'standard',
            'fields': {
                'french_heavy': {
                    'type': 'text',
                    'analyzer': 'french_heavy',
                },
                'french_light': {
                    'type': 'text',
                    'analyzer': 'french_light',
                },
                'edge_ngram': {
                    'type': 'text',
                    'analyzer': 'edge_ngram_custom',
                },
            },
        },
        'text': {
            'type': 'text',
            'analyzer': 'standard',
            'fields': {
                'french_heavy': {
                    'type': 'text',
                    'analyzer': 'french_heavy',
                },
                'french_light': {
                    'type': 'text',
                    'analyzer': 'french_light',
                },
                'edge_ngram': {
                    'type': 'text',
                    'analyzer': 'edge_ngram_custom',
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
                    'analyzer': 'french_heavy',
                },
                'french_light': {
                    'type': 'text',
                    'analyzer': 'french_light',
                },
                'edge_ngram': {
                    'type': 'text',
                    'analyzer': 'edge_ngram_custom',
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
                    'analyzer': 'french_heavy',
                },
                'french_light': {
                    'type': 'text',
                    'analyzer': 'french_light',
                },
                'edge_ngram': {
                    'type': 'text',
                    'analyzer': 'edge_ngram_custom',
                },
            },
        },
    },
}
