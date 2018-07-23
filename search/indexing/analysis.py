from search.extraction.synonyms.data import SYNONYMS


filters = {
    # Normalize acronyms so that no matter the format, the resulting token will be the same.
    # E.g.: SmiC => S.M.I.C. => SMIC => smic.
    'acronyms': {
        'type': 'word_delimiter',
        'catenate_all': True,
        'generate_word_parts': False,
        'generate_number_parts': False,
    },
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
    'synonyms': {
        'type': 'synonym',
        'synonyms': SYNONYMS,
    },
}

analyzers = {
    'french_heavy': {
        'type': 'custom',
        'char_filter': ['html_strip'],
        'tokenizer': 'icu_tokenizer',
        'filter': [
            'french_elision',
            'icu_folding',
            'acronyms',
            'synonyms',
            'french_stemmer',
        ],
    },
    'french_light': {
        'type': 'custom',
        'char_filter': ['html_strip'],
        'tokenizer': 'icu_tokenizer',
        'filter': [
            'french_elision',
            'icu_folding',
        ],
    },
    'edge_ngram_custom': {
        'type': 'custom',
        'char_filter': ['html_strip'],
        'tokenizer': 'standard',
        'filter': [
            'asciifolding',
            'lowercase',
            'acronyms',
            'edge_ngram_filter',
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
