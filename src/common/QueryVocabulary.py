import string
import datrie

class QueryVocabulary(object):
    def __init__(self, query_log_path):
        self.vocabulary = datrie.Trie(string.ascii_lowercase)
        with open(query_log_path) as log_file:
            for line in log_file:
                uid, query, time = line.split()
                if query not in self.vocabulary:
                    self.vocabulary[query] = 1
                else:
                    self.vocabulary[query] += 1

    def get_by_prefix(self, prefix):
        keys = self.vocabulary.keys(prefix)
        return keys
