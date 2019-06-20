from pdb import set_trace
import numpy as np
from sigmoid import *

def predict(theta, X):
	
	predict = sigmoid(np.dot(X, theta))
	predict = 1 * (predict >= 0.5)

	return predict	
	