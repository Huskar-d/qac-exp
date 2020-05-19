'''
convert raw dataset to training, testing and validate set
'''

class RawDataProcessor(object):

    def __init__(self, file_name_feature, query_log_dir='./'):
        self.query_files = self.get_query_files(file_name_feature, query_log_dir)
        # a map contains configuration about data process
        self.total_data_num=0
        self.train_data_num=0
        self.validate_data_num = 0
        # time interval to extract user context, in seconds
        self.session_interval = 300
        self.initiate_config()

    def initiate_config(self):
        self.total_data_num = 1000

    def load_query_log(self, query_log_dir='./'):
        pass

    def get_train_set(self, validation_ratio=0):
        pass

    def get_test_set(self):
        pass

    def get_vocabulary(self, store='memory'):
        pass


class AOLProcessor(object):
    def extractContext(self, options):
        '''
        extract session based query context info
        :param options:
        :return:
        '''
        pass
