### Expected results for parse.py unit tests
# coding: utf-8

from collections import OrderedDict

book_1 = {
    'book': {'filename': '1En', 'title': '1 Enoch', 'textStructure': ''},
    'version': [
        {
            'attributes': {'title': 'Ethiopic 1', 'author': 'Anonymous', 'fragment': '', 'language': 'Ethiopic',},
            'organisation_levels': 2,
            'divisions': {'labels': ['Chapter', 'Verse'], 'delimiters': [':'], 'text': ['', '']},
            'resources': [
                [
                    {'attributes': {'name': 'Resource1'}, 'info': ['Info 1', 'Info 2'], 'url': 'www.example.com'},
                    {'attributes': {'name': 'Resource2'}, 'info': ['Info 3', 'Info 4'], 'url': ''}
                ],
                [
                    {'attributes': {'name': 'Resource3'}, 'info': ['Info 5', 'Info 6'], 'url': 'www.example.com'},
                    {'attributes': {'name': 'Resource4'}, 'info': ['Info 7', 'Info 8'], 'url': ''}
                ],
            ],
            'manuscripts': [
                {
                    'p1': {
                        'attributes': {'abbrev': 'p1', 'language': 'Ethiopic', 'show': 'yes'},
                        'name': {'text': 'John Rylands Library Ethiopic 23', 'sup': ['Sup 1', 'Sup 2'],},
                        'bibliography': [],
                    },
                    'p2': {
                        'attributes': { 'abbrev': 'p2', 'language': 'Ethiopic', 'show': 'yes'},
                        'name': {'text': 'John Rylands Library Ethiopic 23', 'sup': [],},
                        'bibliography': [],
                    },
                    'p3': {
                        'attributes': {'abbrev': 'p3', 'language': 'Ethiopic', 'show': 'yes'},
                        'name': {'text': '', 'sup': ['Sup 1', 'Sup 2'],},
                        'bibliography': [
                            {'text': 'M. Knibb, The Ethiopic book of Enoch : A New Edition in the Light of the Aramaic Dead Sea Fragments. Oxford: Clarendon, 1978.', 'booktitle': ['Booktitle 1', 'Booktitle 2',]},
                            {'text': 'M. Knibb, The Ethiopic book of Enoch : A New Edition in the Light of the Aramaic Dead Sea Fragments. Oxford: Clarendon, 1978.', 'booktitle': []},
                            {'text': '', 'booktitle': ['Booktitle 3', 'Booktitle 4',]},
                            {'text': '', 'booktitle': []},
                        ],
                    },
                    'Bertalotto ': {
                        'attributes': {'abbrev': 'Bertalotto ', 'language': 'Ethiopic', 'show': 'yes'},
                        'name': {'text': "Bertalotto's correction of orthographic tendencies in ms p", 'sup': [],},
                        'bibliography': [
                            {'text': 'M. Knibb, The Ethiopic book of Enoch : A New Edition in the Light of the Aramaic Dead Sea Fragments. Oxford: Clarendon, 1978.', 'booktitle': []},
                        ]
                    },
                }
            ],
            'text_structure': {
                '1:1': {
                    'attributes': [
                        {'number': '1', 'fragment': 'Fragment 1',},
                        {'number': '1', 'fragment': 'Fragment 2',},
                    ],
                    'units': [
                        {'id': '1', 'group': '1', 'parallel': 'Parallel 1'},
                    ],
                    'readings': {
                        '1': {
                            'Bertalotto p': {
                                'attributes': {'option': '0', 'mss': 'Bertalotto p  ', 'linebreak': '', 'indent': '',},
                                'text': unicode('ቃለ፡​በረከት፡​ዘሄኖከ፡​ዘከመ፡​ባረከ፡​ኅሩያነ፡​ወጻድቃነ፡​እለ፡​ሀለዉ፡​ይኩኑ፡​በዕለተ፡​ምንዳቤ፡​ለአሰስሎ፡​ኵሎ፡​እኩያን፡​ወረሲዓን፡​', encoding='utf-8'),
                                'w': []
                            }
                        }
                    }
                },
                '1:2': {
                    'attributes': [
                        {'number': '1', 'fragment': 'Fragment 1',},
                        {'number': '2', 'fragment': '',},
                    ],
                    'units': [
                        {'id': '2', 'group': '2', 'parallel': ''},
                        {'id': '3', 'group': '0', 'parallel': 'Parallel 2'},
                        {'id': '4', 'group': '0', 'parallel': ''},
                    ],
                    'readings': {
                        '2': {
                            'Bertalotto p': {
                                'attributes': {'option': '0', 'mss': 'Bertalotto p ', 'linebreak': 'following', 'indent': '',},
                                'text': unicode('ወአውሥአ፡​ሄኖክ፡​ወይቤ፡​ብእሲ፡​ጻድቅ፡​ዘእምኀበ፡​እግዚአብሔር፡​እንዘ፡​አዕይንቲሁ፡​ክሡታት፡​ወይሬኢ፡​', encoding='utf-8'),
                                'w': [
                                    {
                                        'attributes': {'morph': 'morph', 'lex': 'lex', 'style': 'style', 'lang': 'lang'},
                                        'text': 'w 1'
                                    },
                                ]
                            }
                        },
                        '3': {
                            'p': {
                                'attributes': {'option': '0', 'mss': 'p ', 'linebreak': '', 'indent': '',},
                                'text': unicode('ራዕየ፡​', encoding='utf-8'),
                                'w': [
                                    {
                                        'attributes': {'morph': 'morph', 'lex': 'lex', 'style': 'style', 'lang': ''},
                                        'text': 'w 2'
                                    },
                                ]
                            },
                            'Bertalotto': {
                                'attributes': {'option': '1', 'mss': 'Bertalotto ', 'linebreak': '', 'indent': 'yes',},
                                'text': unicode('ራእየ፡​', encoding='utf-8'),
                                'w': [
                                    {
                                        'attributes': {'morph': 'morph', 'lex': 'lex', 'style': '', 'lang': 'lang'},
                                        'text': 'w 3'
                                    },
                                ]
                            }
                        },
                        '4': {
                            'Bertalotto p': {
                                'attributes': {'option': '0', 'mss': 'Bertalotto p ', 'linebreak': '', 'indent': 'no',},
                                'text': unicode('ቅዱሰ፡​ዘበሰማያት፡​ዘአርአዩኒ፡​መላእክት፡​ወሰማዕኩ፡​እምኀቤሆሙ፡​ኵሎ፡​ወአእመርኩ፡​አነ፡​ዘእሬኢ፡​ወአኮ፡​ለዝ፡​ትውልድ፡​አላ፡​ለዘ፡​ይመጽኡ፡​ትውልድ፡​ርሑቃን፡​', encoding='utf-8'),
                                'w': [
                                    {
                                        'attributes': {'morph': 'morph', 'lex': 'lex', 'style': '', 'lang': ''},
                                        'text': 'w 4'
                                    },
                                ]
                            }
                        },
                    }
                },
                '1:3': {
                    'attributes': [
                        {'number': '1', 'fragment': 'Fragment 1',},
                        {'number': '3', 'fragment': '',},
                    ],
                    'units': [
                        {'id': '5', 'group': '0', 'parallel': ''},
                        {'id': '6', 'group': '0', 'parallel': ''},
                        {'id': '7', 'group': '0', 'parallel': ''},
                    ],
                    'readings': {
                        '5': {
                            'Bertalotto p': {
                                'attributes': {'option': '0', 'mss': 'Bertalotto p ', 'linebreak': 'following', 'indent': 'yes',},
                                'text': unicode('በእንተ፡​ኅሩያን፡​እቤ፡​ወአውሣእኩ፡​በእንቲአሆሙ፡​ምስለ፡​ዘይወጽእ፡​ቅዱስ፡​', encoding='utf-8'),
                                'w': [
                                    {
                                        'attributes': {'morph': 'morph', 'lex': '', 'style': 'style', 'lang': 'lang'},
                                        'text': 'w 5'
                                    },
                                ]
                            }
                        },
                        '6': {
                            'p': {
                                'attributes': {'option': '0', 'mss': 'p ', 'linebreak': '', 'indent': '',},
                                'text': unicode('ወዓቢይ፡​', encoding='utf-8'),
                                'w': [
                                    {
                                        'attributes': {'morph': 'morph', 'lex': '', 'style': 'style', 'lang': ''},
                                        'text': 'w 6'
                                    },
                                ]
                            },
                            'Bertalotto': {
                                'attributes': {'option': '1', 'mss': 'Bertalotto ', 'linebreak': '', 'indent': '',},
                                'text': unicode('ወዐቢይ፡​', encoding='utf-8'),
                                'w': [
                                    {
                                        'attributes': {'morph': 'morph', 'lex': '', 'style': '', 'lang': 'lang'},
                                        'text': 'w 7'
                                    },
                                ]
                            }
                        },
                        '7': {
                            'Bertalotto p': {
                                'attributes': {'option': '0', 'mss': 'Bertalotto p ', 'linebreak': '', 'indent': '',},
                                'text': unicode('እማኅደሩ', encoding='utf-8'),
                                'w': [
                                    {
                                        'attributes': {'morph': 'morph', 'lex': '', 'style': '', 'lang': ''},
                                        'text': 'w 8'
                                    },
                                ]
                            }
                        },
                    }
                },  # end of <div>
                '2:1': {
                    'attributes': [
                        {'number': '2', 'fragment': '',},
                        {'number': '1', 'fragment': 'Fragment 3',},
                    ],
                    'units': [
                        {'id': '25', 'group': '0', 'parallel': ''},
                        {'id': '26', 'group': '0', 'parallel': ''},
                        {'id': '27', 'group': '0', 'parallel': ''},
                        {'id': '28', 'group': '0', 'parallel': ''},
                        {'id': '29', 'group': '0', 'parallel': ''},
                    ],
                    'readings': {
                        '25': {
                            'Bertalotto p': {
                                'attributes': {'option': '0', 'mss': 'Bertalotto p ', 'linebreak': '', 'indent': '',},
                                'text': unicode('ጠየቁ፡​ኵሎ፡​ዘውስተ፡​ሰማይ፡​ግብረ፡​እፎ፡​ኢይመይጡ፡​ፍናዊሆሙ፡​ብርሃናት፡​ዘውስተ፡​ሰማይ፡​ከመ፡​ኵሉ፡​ይሠርቅ፡​', encoding='utf-8'),
                                'w': [
                                    {
                                        'attributes': {'morph': '', 'lex': 'lex', 'style': 'style', 'lang': 'lang'},
                                        'text': 'w 9'
                                    },
                                ]
                            }
                        },
                        '26': {
                            'Bertalotto': {
                                'attributes': {'option': '0', 'mss': 'Bertalotto ', 'linebreak': '', 'indent': '',},
                                'text': unicode('ወየዐርብ፡​', encoding='utf-8'),
                                'w': [
                                    {
                                        'attributes': {'morph': '', 'lex': 'lex', 'style': 'style', 'lang': ''},
                                        'text': 'w 10'
                                    },
                                ]
                            },
                            'p': {
                                'attributes': {'option': '1', 'mss': 'p ', 'linebreak': '', 'indent': '',},
                                'text': unicode('ወየዓርብ፡​', encoding='utf-8'),
                                'w': [
                                    {
                                        'attributes': {'morph': '', 'lex': 'lex', 'style': '', 'lang': 'lang'},
                                        'text': 'w 11'
                                    },
                                ]
                            }
                        },
                        '27': {
                            'Bertalotto p': {
                                'attributes': {'option': '0', 'mss': 'Bertalotto p ', 'linebreak': '', 'indent': '',},
                                'text': unicode('ሥሩዕ፡​ኵሉ፡​በዘመኑ፡​', encoding='utf-8'),
                                'w': [
                                    {
                                        'attributes': {'morph': '', 'lex': 'lex', 'style': '', 'lang': ''},
                                        'text': 'w 12'
                                    },
                                ]
                            }
                        },
                        '28': {
                            'Bertalotto': {
                                'attributes': {'option': '0', 'mss': 'Bertalotto ', 'linebreak': '', 'indent': '',},
                                'text': unicode('ወኢይትዐደዉ፡​', encoding='utf-8'),
                                'w': [
                                    {
                                        'attributes': {'morph': '', 'lex': '', 'style': 'style', 'lang': 'lang'},
                                        'text': 'w 13'
                                    },
                                ]
                            },
                            'p': {
                                'attributes': {'option': '1', 'mss': 'p ', 'linebreak': '', 'indent': '',},
                                'text': unicode('ወኢይትዓደዉ፡​', encoding='utf-8'),
                                'w': [
                                    {
                                        'attributes': {'morph': '', 'lex': '', 'style': 'style', 'lang': ''},
                                        'text': 'w 14'
                                    },
                                ]
                            }
                        },
                        '29': {
                            'Bertalotto': {
                                'attributes': {'option': '0', 'mss': 'Bertalotto ', 'linebreak': '', 'indent': '',},
                                'text': unicode('እምትእዛዞሙ።', encoding='utf-8'),
                                'w': [
                                    {
                                        'attributes': {'morph': '', 'lex': '', 'style': '', 'lang': 'lang'},
                                        'text': 'w 15'
                                    },
                                ]
                            },
                            'p': {
                                'attributes': {'option': '1', 'mss': 'p ', 'linebreak': '', 'indent': '',},
                                'text': unicode('እምትዛዞሙ።', encoding='utf-8'),
                                'w': [
                                    {
                                        'attributes': {'morph': '', 'lex': '', 'style': '', 'lang': ''},
                                        'text': 'w 16'
                                    },
                                ]
                            }
                        },
                    }
                },   # end of <div>
            }   # end of text_structure
        },   # end of version
        {
            'attributes': {'title': 'Ethiopic 2', 'author': 'Anonymous', 'fragment': 'Fragment 1', 'language': '',},
            'organisation_levels': 2,
            'divisions': {'labels': ['Chapter', 'Verse'], 'delimiters': [':'], 'text': ['', '']},
            'resources': [],
            'manuscripts': [
                {
                    'p1': {
                        'attributes': {'abbrev': 'p1', 'language': 'Ethiopic', 'show': 'yes'},
                        'name': {'text': 'John Rylands Library Ethiopic 23', 'sup': [],},
                        'bibliography': [],
                    },
                }
            ],
            'text_structure': {
                '1:1': {
                    'attributes': [
                        {'number': '1', 'fragment': '',},
                        {'number': '1', 'fragment': '',},
                    ],
                    'units': [
                        {'id': '1', 'group': '0', 'parallel': ''},
                    ],
                    'readings': {
                        '1': {
                            'Bertalotto p': {
                                'attributes': {'option': '0', 'mss': 'Bertalotto p  ', 'linebreak': '', 'indent': '',},
                                'text': unicode('ቃለ፡​በረከት፡​ዘሄኖከ፡​ዘከመ፡​ባረከ፡​ኅሩያነ፡​ወጻድቃነ፡​እለ፡​ሀለዉ፡​ይኩኑ፡​በዕለተ፡​ምንዳቤ፡​ለአሰስሎ፡​ኵሎ፡​እኩያን፡​ወረሲዓን፡​', encoding='utf-8'),
                                'w': []
                            }
                        }
                    }
                },
            }   # end of text_structure
        },   # end of version
        {
            'attributes': {'title': 'Ethiopic 3', 'author': 'Anonymous', 'fragment': '', 'language': '',},
            'organisation_levels': 2,
            'divisions': {'labels': ['Chapter', 'Verse'], 'delimiters': [':'], 'text': ['', '']},
            'resources': [],
            'manuscripts': [
                {
                    'p1': {
                        'attributes': {'abbrev': 'p1', 'language': 'Ethiopic', 'show': 'yes'},
                        'name': {'text': 'John Rylands Library Ethiopic 23', 'sup': [],},
                        'bibliography': [],
                    },
                }
            ],
            'text_structure': {
                '1:1': {
                    'attributes': [
                        {'number': '1', 'fragment': '',},
                        {'number': '1', 'fragment': '',},
                    ],
                    'units': [
                        {'id': '1', 'group': '0', 'parallel': ''},
                    ],
                    'readings': {
                        '1': {
                            'Bertalotto p': {
                                'attributes': {'option': '0', 'mss': 'Bertalotto p  ', 'linebreak': '', 'indent': '',},
                                'text': unicode('ቃለ፡​በረከት፡​ዘሄኖከ፡​ዘከመ፡​ባረከ፡​ኅሩያነ፡​ወጻድቃነ፡​እለ፡​ሀለዉ፡​ይኩኑ፡​በዕለተ፡​ምንዳቤ፡​ለአሰስሎ፡​ኵሎ፡​እኩያን፡​ወረሲዓን፡​', encoding='utf-8'),
                                'w': []
                            }
                        }
                    }
                },
            }   # end of text_structure
        },   # end of version
    ],
}

book_2 = {
    'book': {'filename': '1En', 'title': '1 Enoch', 'textStructure': 'Book with textStructure'},
    'version': [
        {
            'attributes': {'title': 'Ethiopic', 'author': 'Anonymous', 'fragment': '', 'language': '',},
            'organisation_levels': 2,
            'divisions': {'labels': ['Chapter', 'Verse'], 'delimiters': [':'], 'text': ['', '']},
            'resources': [],
            'manuscripts': [
                {
                    'p1': {
                        'attributes': {'abbrev': 'p1', 'language': 'Ethiopic', 'show': 'yes'},
                        'name': {'text': 'John Rylands Library Ethiopic 23', 'sup': [],},
                        'bibliography': [],
                    }
                }
            ],
            'text_structure': {
                '1:1': {
                    'attributes': [
                        {'number': '1', 'fragment': '',},
                        {'number': '1', 'fragment': '',},
                    ],
                    'units': [
                        {'id': '1', 'group': '0', 'parallel': ''}
                    ],
                    'readings': {
                        '1': {
                            'Bertalotto p': {
                                'attributes': {'option': '0', 'mss': 'Bertalotto p  ', 'linebreak': '', 'indent': '',},
                                'text': unicode('ቃለ፡​በረከት፡​ዘሄኖከ፡​ዘከመ፡​ባረከ፡​ኅሩያነ፡​ወጻድቃነ፡​እለ፡​ሀለዉ፡​ይኩኑ፡​በዕለተ፡​ምንዳቤ፡​ለአሰስሎ፡​ኵሎ፡​እኩያን፡​ወረሲዓን፡​', encoding='utf-8'),
                                'w': []
                            }
                        }
                    }
                }
            }
        }
    ],
}



