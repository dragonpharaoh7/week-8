from collections import defaultdict

import numpy as np


class MarkovText(object):

    def __init__(self, corpus):
        self.corpus = corpus
        self.term_dict = None

    def get_term_dict(self):
        # Duplicates ARE kept. Every time a word follows another word, it gets
        # appended again. A word that follows more often shows up more times
        # in the list, raising its probability of being chosen. This is a simple way to make the
        # generated text more like the original text.

        tokens = self.corpus.split()

        term_dict = defaultdict(list)

        for i in range(len(tokens) - 1):
            term_dict[tokens[i]].append(tokens[i + 1])

        # maccount fo r last
        if len(tokens) > 0 and tokens[-1] not in term_dict:
            term_dict[tokens[-1]] = []

        self.term_dict = dict(term_dict)

        return self.term_dict

    def generate(self, seed_term=None, term_count=15):
        if self.term_dict is None:
            self.get_term_dict()

        if seed_term is None:
            # pick a random word from the corpus to start with
            term = np.random.choice(list(self.term_dict.keys()))
        else:
            if seed_term not in self.term_dict:
                raise ValueError(f"'{seed_term}' is not in the corpus.")
            term = seed_term

        terms = [term]

        for _ in range(term_count - 1):
            next_terms = self.term_dict.get(term, [])

            # dead end: nothing ever followed this word, so stop here
            if len(next_terms) == 0:
                break

            term = np.random.choice(next_terms)
            terms.append(term)

        return ' '.join(terms)
