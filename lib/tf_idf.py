from . import megatron

class TFIDF:
    def __init__(self, megatron):
            self.megatron = megatron

    def compute_idf(self):
            print('creating index')
            self.megatron.word_book_controller.add_indices()
            print('created index')
            self.megatron.tf_idf_controller.drop_tables()
            self.megatron.tf_idf_controller.create_tables()
            print('precomputing top book word count')
            self.megatron.tf_idf_controller.compute_top_book_word_count_idf()
            print('precomputing idf')
            self.megatron.tf_idf_controller.compute_idf()


    def compute_tfidf(self):
            print('creating index')
            self.megatron.tf_idf_controller.add_idf_indices()
            print('created index')
            self.megatron.tf_idf_controller.compute_tfidf()

    def compute_top_words(self):
            print('creating index')
            self.megatron.tf_idf_controller.add_tfidf_indices()
            print('created index')
            self.megatron.tf_idf_controller.compute_top_words()
