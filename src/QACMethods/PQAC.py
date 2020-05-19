'''
Reproduce method in SIGIR2019, Personalized Query Auto-Completion Through a Lightweight
Representation of the User Context
'''
from QACMethods.Learn2RankQAC import Learning2RankQAC
from common.Feature import TextualFeature, FastEmbeddingFeature


class PQAC(Learning2RankQAC):
    def __init__(self, input_path, output_path):
        super.__init__(input_path, output_path)
        self.word2vec = None

    def get_features(self,query, context_queries):
        textual_features = TextualFeature(query, context_queries)
        embedding_features = FastEmbeddingFeature(query, context_queries)
        return textual_features + embedding_features

