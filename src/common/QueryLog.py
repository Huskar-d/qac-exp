import copy

from common.QueryVocabulary import QueryVocabulary


class QueryLog(object):
    def __init__(self, log_path, session_interval, log_vocabulary=None):
        self.session_cache = {}
        self.session_interval = session_interval
        self.log_file_current = open(log_path)
        self.log_vocabulary = log_vocabulary
        if self.log_vocabulary is None:
            self.log_vocabulary = QueryVocabulary()

    def __iter__(self):
        return self

    def __next__(self):
        line = self.log_file_current.readline(1)
        if line == '':
            raise StopIteration()
        uid, query, time = line.split()
        # update session
        if uid not in self.session_cache:
            self.session_cache[uid] = []
        self.session_cache[uid].append((query, time))

        # knocked out old query from session
        old_session = self.session_cache[uid]
        cur_session = []
        for previous_query, previous_time in old_session:
            if self._time_interval(time, previous_time) <= self.session_interval:
                cur_session.append((previous_query, previous_time))
        self.session_cache[uid] = cur_session
        query_log = {}
        query_log['uid'] = uid
        query_log['query'] = query
        query_log['context'] = cur_session[:-1]
        return query_log

    def get_candidates(self, query, max_prefix_length):
        candidates = {}
        for i in range(max_prefix_length):
            prefix_length = i+1
            if prefix_length > max_prefix_length or prefix_length > len(query):
                break
            prefix = query[:prefix_length]
            candidates[prefix] = self.log_vocabulary.get_by_prefix(prefix)
