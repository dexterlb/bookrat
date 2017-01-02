from . import megatron

class TFIDF:
    def __init__(self, megatron):
            self.megatron = megatron

    def compute_idf(self):
            print('creating index')
            self.megatron.word_book_controller.add_indices()
            print('created index')

            print('dropping old tfidf tables')
            self.megatron.tf_idf_controller.drop_tables()
            self.megatron.tf_idf_controller.create_tables()
            print('precomputing top book word count')
            self.megatron.tf_idf_controller.compute_top_book_word_count()
            print('precomputing idf')
            self.megatron.tf_idf_controller.compute_idf()

            print('creating index on idf')
            self.megatron.tf_idf_controller.add_idf_indices()
            print('created index')


    def compute_tfidf(self):
            self.megatron.tf_idf_controller.compute_tfidf()

            print('creating index on tfidf')
            self.megatron.tf_idf_controller.add_tfidf_indices()
            print('finished creating index')

    def compute_top_words(self):
            self.megatron.tf_idf_controller.compute_top_words()

            print('creating index on topwords')
            self.megatron.tf_idf_controller.add_top_words_indices()
            print('finished creating index')
