import numpy as np
import matplotlib.pyplot as matplot



def reg(x,y,order = 1):
    A = np.array([np.ones(len(x))])
    for i in range(order):
        A = np.vstack((np.array([np.power(x,i+1)]),A))
    coeff = np.dot( np.linalg.pinv(A.T), np.array([y]).T )
    return coeff
    #rx = np.r_[x.min():x.max()] #TODO: not sure what the default step will be
    #matplot.scatter(x, y)
    #A = np.array([np.ones(len(rx))])
    #for i in range(order):
    #    A = np.vstack((np.array([np.power(rx,i+1)]),A))
    #matplot.plot(x, np.dot(A.T,coeff), 'k')
    #matplot.show()

def applyPoly(x,coeff):
    order = len(coeff)-1
    A = np.array([np.ones(len(x))])
    for i in range(order):
        A = np.vstack((np.array([np.power(x,i+1)]),A))
    y = np.dot(A.T, coeff)
    return y
    
