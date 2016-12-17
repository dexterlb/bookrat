from . import megatron

class TFIDF:
    def __init__(self, megatron):
            self.megatron = megatron

    def compute_idf(self):
            self.megatron.tf_idf_controller.compute_idf()

    def compute_tfidf(self):
            self.megatron.tf_idf_controller.compute_tfidf()

    def compute_top_words(self):
            self.megatron.tf_idf_controller.compute_top_words()
