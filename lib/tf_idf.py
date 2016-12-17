from . import megatron

class TFIDF:
    def __init__(self, megatron):
            self.megatron = megatron

    def compute_idf(self):
            self.megatron.word_book_controller.add_indices()
            self.megatron.tf_idf_controller.drop_tables()
            self.megatron.tf_idf_controller.create_tables()
            self.megatron.tf_idf_controller.compute_idf()

    def compute_tfidf(self):
            self.megatron.tf_idf_controller.add_idf_indices()
            self.megatron.tf_idf_controller.compute_tfidf()

    def compute_top_words(self):
            self.megatron.tf_idf_controller.add_tfidf_indices()
            self.megatron.tf_idf_controller.compute_top_words()
