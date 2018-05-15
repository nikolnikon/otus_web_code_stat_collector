import collections
from nltk import pos_tag


class Analyzer:
    def __init__(self):
        pass

    def get_words_count(self, words, part_of_speech, top_size):
        funcs = {
            'verb': self._get_verbs,
            'noun': self._get_nouns,
        }

        filtered_words = funcs[part_of_speech](words)
        return collections.Counter(filtered_words).most_common(top_size)

    def _get_verbs(self, words):
        words_info = pos_tag(words)
        return [tag[0] for tag in words_info if 'VB' in tag[1]]

    def _get_nouns(self, words):
        words_info = pos_tag(words)
        return [tag[0] for tag in words_info if 'NN' in tag[1]]