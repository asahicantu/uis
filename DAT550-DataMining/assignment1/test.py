#%%
from sklearn.datasets import fetch_openml
import numpy as np
mnist = fetch_openml('mnist_784', cache=False)
X = mnist.data
y = mnist.target.astype(int)
#%%
np.where(y == 0)
X_i = []
X_i_cov = []
for i in np.arange(10):
    i = 0
    x = X[np.where(y == i)]
    x_mean = x.mean(axis=0)
    x_std = x.std(axis=0)
    x_std[x_std == 0] = 1
    x_p = (x - x_mean) / x_std
    X_i.append( x_p )
    X_i_cov.append( np.cov(x_p) )
    
#$$


def getSVD(cov_matrix):
    U, S, V = np.linalg.svd(cov_matrix,  full_matrices=False)
    return U, S, V


X_i_U = []
X_i_S = []
X_i_V = []

for i in np.arange(10):
    u, s, v = getSVD(X_i_cov[i])
    X_i_U.append(u)
    X_i_S.append(s)
    X_i_V.append(v)
#%%

# Xij = X.shape
# X_ = np.zeros(Xij)
# X_mean = X.mean(axis=0)
# X_sdev = X.std(axis=1)
# for i in np.arange(Xij[1]):
#     X_[:, i] = (X[:, i] - X_mean[i]) / X_sdev[i]
# print("calculating covariance")
# print(X_)
# X_cov = np.cov(X_)
# print("Covariance is:  " + X_cov)


# %%
