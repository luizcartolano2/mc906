import numpy as np


def sigmoid(z):
	"""
		:param: z - can be a matrix, vector or scalar

		:return: g - sigmoid de cada valor
	"""
	try:
		g = 1/(1+np.exp(-z))
	except:
		import pdb
		pdb.set_trace()

	return g
