from logger.core_logger import *
import numpy as np
def test():

	n_samples = 100
	mean = [0, 0]
	cov = [[3, 1], [1, 0.3]]  # covariance matrix to create correlation

	data = np.random.multivariate_normal(mean, cov, n_samples)

	log.start_experiment("test_pca")
	pca_data = data 
	log.create_plot("pca", pca_data, template="pca")
	log.finalize()
