from . import megatron

class TFIFD:
	def __init__(self, megatron):
		self.megatron = megatron


	def compute_idf(self):
		self.megatron.idf_controller.compute_idf()