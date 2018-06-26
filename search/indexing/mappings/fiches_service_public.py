fiches_service_public_mapping = {
    'properties': {
        'url': {
            'type': 'text',
            'analyzer': 'keyword',
        },
        'sous_theme': {
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
        'refs': {
            'type': 'nested',
            'properties': {
                'url': {
                    'type': 'text',
                    'analyzer': 'keyword',
                },
                'source': {
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
                'sujet': {
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
        },
    },
}
