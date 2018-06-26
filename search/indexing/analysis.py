filters = {
    'edge_ngram_filter': {
        'type': 'edge_ngram',
        'min_gram': 4,
        'max_gram': 20,
    },
    'french_elision': {
        'type': 'elision',
        'articles_case': True,
        'articles': [
            'l', 'm', 't', 'qu', 'n', 's',
            'j', 'd', 'c', 'jusqu', 'quoiqu',
            'lorsqu', 'puisqu',
        ],
    },
    'french_stemmer': {
        'type': 'stemmer',
        'language': 'light_french',
    },
}


analyzers = {
    'edge_ngram_custom': {
        'type': 'custom',
        'char_filter': ['html_strip'],
        'tokenizer': 'standard',
        'filter': [
            'asciifolding',
            'lowercase',
            'edge_ngram_filter',
        ],
    },
    'french_custom': {
        'tokenizer': 'standard',
        'char_filter': ['html_strip'],
        'filter': [
            'french_elision',
            'lowercase',
            'french_stemmer',
        ],
    },
    'path_analyzer_custom': {
        'tokenizer': 'tags',
    },
}

tokenizers = {
    'tags': {
        'type': 'path_hierarchy',
    },
}
