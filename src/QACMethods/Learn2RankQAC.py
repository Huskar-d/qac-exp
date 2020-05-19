import numpy
import os

from common.Feature import TextualFeature, FastEmbeddingFeature
from common.QueryLog import QueryLog


class Learning2RankQAC(object):
    def __init__(self, tran_log_path, train_path, test_log_path, test_path, output_path):
        self.rank_lib_methods = ['lambdamart',]
        self.model_path = output_path
        self.train_set_path = train_path
        self.test_set_path = test_path
        self.generate_train_set = True
        self.generate_test_set = True
        self.session_interval = 300
        self._load_config()
        if self.generate_train_set:
            self._prepare_l2r_file(self.train_set_path, tran_log_path)
        if self.generate_train_set:
            self._prepare_l2r_file(self.test_set_path, test_log_path)

    def train(self, method='lambdamart'):
        if method in self.rank_lib_methods:
            self._train_with_ranklib()

    def evaluate(self,method='lambdamart'):
        if method in self.rank_lib_methods:
            self._evaluate_with_ranklib()

    def _prepare_l2r_file(self, output_path, log_path):
        word2vec = self.word2vec_training()
        #
        with open(output_path,'w') as l2r_train_file:
            query_logs = QueryLog(log_path, self.session_interval)
            qid = 0
            i = 0
            for query_log in query_logs:
                i += 1
                if i%10000 == 0:
                    print('processed %s query for log:%s'(i, log_path))
                query = query_log['query']
                context_queries = query_log['context']
                # file format
                # < line >.=.< target > qid: < qid > < feature >: < value > < feature >: < value > ... < feature >: < value >  # <info>
                # < target >.=.< positive integer >
                # < qid >.=.< positive integer >
                # < feature >.=.< positive integer >
                # < value >.=.< float >
                # < info >.=.< string >
                # example:
                # 3 qid:1 1:1 2:1 3:0 4:0.2 5:0 # 1A
                # 2 qid:1 1:0 2:0 3:1 4:0.1 5:1 # 1B
                # 1 qid:1 1:0 2:1 3:0 4:0.4 5:0 # 1C
                # 1 qid:1 1:0 2:0 3:1 4:0.3 5:0 #                 # 1 qid:2 1:0 2:0 3:1 4:0.2 5:0 # 2A
                # 2 qid:2 1:1 2:0 3:1 4:0.4 5:0 # 2B
                # the following set of pairwise constraints is generated :1A>1B, 1A>1C, 1A>1D, 1B>1C, 1B>1D

                for prefix,match_queries in query_logs.get_candidates(query, self.max_prefix_length).items:
                    # for each qid(query prefix)
                    qid += 1
                    # prepare all candidates
                    candidates = [(query, 2), ]
                    for match_query in match_queries:
                        if query != match_query:
                            candidates.append((match_query,1))
                    # construct doc feature line for each candidate
                    line_elements = []
                    for candidate, target in candidates:
                        # generate a line for each candidate history query
                        feature_id = 1
                        line_elements.append(target)
                        line_elements.append('qid:%s' % qid)
                        features = self.get_features(candidate,context_queries)
                        for feature in features.getfeatures():
                            line_elements.append('%s:%s' % (feature_id, feature))
                        line = ' '.join(line_elements)
                        l2r_train_file.write('%s\n' % line)

    def get_features(self, query, context_queries):
        '''
        :return: list of feature values for the input value
        '''
        return []

    def _train_with_ranklib(self):
        os.system('java -jar bin/RankLib.jar -train MQ2008/Fold1/train.txt -test MQ2008/Fold1/test.txt -validate MQ2008/Fold1/vali.txt -ranker 6 -metric2t NDCG@10 -metric2T ERR@10 -save mymodel.txt')


    def _evaluate_with_ranklib(self):
        pass