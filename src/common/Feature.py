
class Feature:
    def __init__(self, query, context_queries):
        self._feature_data = []
        self._feature_name = {}
        self._construct_feature(query, context_queries)

    def get_feature_by_index(self, index):
        pass

    def get_feature_by_indices(self, indices):
        pass

    def get_feature_by_name(self):
        pass

    def set_feature_by_index(self):
        pass

    def get_features(self):
        return [0.1,0.3,0.4]


class TextualFeature(Feature):
    def __init__(self, query, context_queries):
        super.__init__(query, context_queries)
        self.previous_terms=set()
        self.last_query_terms = set()
        self.current_terms = set()

    def _construct_feature(self, query, context_queries):
        '''
        Token(16 features)
        ratio of new terms
        ratio of used terms
        average terms  in previous queries
        median terms in previous queries
        trend of number of terms
        unique terms added from last query
        unique terms retained from last query
        unique terms removed from last query
        unique terms added from all previous queries
        occurrence of terms in previous queries

        query(7 features)
        frequency in previous queries
        character n-gram similarity with previous queries
        token n-gram similarity with previous queries

        Session (3 features)
        position in session
        unique terms in session
        common terms in session
        :return:
        '''

        # construct term set
        for term in query.split():
            self.current_terms.add(term)
        for i, context_query in enumerate(context_queries):
            for term in context_query[0].split():
                self.previous_terms.add(term)
                if i == 0:
                    self.last_query_terms.add(term)
        #Token(16 features)
        #ratio of new terms

        #ratio of used terms
        #average terms  in previous queries
        #median terms in previous queries
        #trend of number of terms
        #unique terms added from last query
        #unique terms retained from last query
        #unique terms removed from last query
        #unique terms added from all previous queries
        #occurrence of terms in previous queries
        pass


class FastEmbeddingFeature(Feature):
    def __init__(self, query, context_queries, word2vec):
        super.__init__(query, context_queries)
        pass

    def _construct_feature(self):
        pass