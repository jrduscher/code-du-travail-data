code_du_travail_mapping = {
    'properties': {
        'num': {
            'type': 'text',
            'analyzer': 'keyword',
        },
        'titre': {
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
        'nota': {
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
        'bloc_textuel': {
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
            'analyzer': 'path_analyzer_custom',
            'fielddata': True,
        },
        'id': {
            'type': 'text',
            'index': False,
        },
        'section': {
            'type': 'text',
            'index': False,
        },
        'etat': {
            'type': 'text',
            'index': False,
        },
        'date_debut': {
            'type': 'date',
            'format': 'yyyy-MM-dd',
            'index': False,
        },
        'date_fin': {
            'type': 'date',
            'format': 'yyyy-MM-dd',
            'index': False,
        },
        'cid': {
            'type': 'text',
            'index': False,
        },
    },
}
