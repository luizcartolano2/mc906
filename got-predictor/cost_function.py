#@Copyright (c) 2019 UHEDGE Trading Solutions All Rights Reserved.
import numpy as np
import pandas as pd
from sigmoid import sigmoid
from pdb import set_trace

def cost_function_reg(theta, X, y, lmbda):
	"""
		:param: theta - 
		:param: X - 
		:param: y - 
		:param: lmbda - 

		:return: J - 
		:return: grad - 
	"""
	theta = np.transpose(np.array(theta)[np.newaxis])
	if X.shape[1] != theta.shape[0]:
		raise Exception('O numero de linhas da matriz THETA deve ser igual ao numero de colunas da matriz X!')

	m = len(y)

	length = len(theta)
	mod_theta = theta[1:]
	
	# aqui nao funfa, descobrir como fazer
	mod_X = X[:, 1:]

	# variaveis auxiliares
	sigmoide_value = sigmoid(np.dot(X, theta))
	X_size = X.shape[0]

	# variaveis a serem retornadas
	J = 0
	grad = np.zeros((1,1))

	J = (np.dot(-y.T, np.log(sigmoide_value)) - np.dot((1-y).T, np.log(1-sigmoide_value))) / X_size + np.dot(lmbda * mod_theta.T, mod_theta) / (2*X_size)
	J = J.item(-1)

	grad = np.add(grad, np.mean(sigmoide_value - y))
	temp = np.add((lmbda / X_size * mod_theta), (np.dot(mod_X.T, (sigmoide_value - y))/X_size))
	grad = np.append(grad, temp, axis=0)
	

	return J, grad


def cost_function(theta, X, y):
	"""
		:param: theta -
		:param: X - 
		:param: y -

		:return: J - 
		:return: grad - 
	"""
	theta = np.transpose(np.array(theta)[np.newaxis])
	
	if X.shape[1] != theta.shape[0]:
		raise Exception('O numero de linhas da matriz THETA deve ser igual ao numero de colunas da matriz X!')

	# m armazena o tamanho da matriz y
	m = len(y)

	# variaveis auxiliares
	sigmoide_value = sigmoid(np.dot(X, theta))
	X_size = X.shape[0]

	# variaveis retornadas
	# J eh o custo calculado
	J = ((np.dot(-y.T, np.log(sigmoide_value)) - np.dot((1-y).T, np.log(1-sigmoide_value))) / X.shape[0]).item(-1)
	# grad eh o grau de variacao
	grad = np.dot(X.T, sigmoide_value - y) / X_size

	return J, grad
