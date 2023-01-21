 varDist = 0
    U_reduce = U[:,:K]
    Z = np.dot(U_reduce.T , X)
    x_approx = np.dot(U_reduce,Z)
    diff = X - x_approx
    # diff = (X_  - x_approx)[K,:]
    
    # varDist = (np.sqrt(np.dot(diff,diff))**2).sum()
    # dist = (np.sqrt(np.dot(X,X))**2).sum()
    # return  (varDist/K) / (dist/K)

    for i in range(K):
        var_distance = np.sqrt(np.dot(diff[:,i],diff[:,i]))**2
        distance = np.sqrt(np.dot(X[:,i],X[:,i]))**2
        varDist += var_distance
        dist += distance
    return  (varDist/K) / (dist/K)


       
    for i in range (K):
        dist_var += (diff[:,i]**2).sum()
        dist += (X[:,i]**2).sum()
    if dist == 0:
        return 0
    else :
        variance = dist_var / dist
    return variance