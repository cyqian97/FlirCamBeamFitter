import numpy as np
import time
from scipy import optimize


class Parameter:
    def __init__(self, value):
        self.value = value

    def set(self, value):
        self.value = value

    def __call__(self):
        return self.value


def fit(function, parameters, y, x=None):
    def f(params):
        i = 0
        for p in parameters:
            p.set(params[i])
            i += 1
        return y - function(x)

    if x is None: x = np.arange(y.shape[0])
    p = [param() for param in parameters]
    return optimize.leastsq(f, p)

def fitgauss1d(xx,yy,truncate = True):
    if truncate:
        x0, xx, yy = truncate_center(xx, yy)
    else:
        x0 = np.sum(xx * yy) / np.sum(yy)
    mu = Parameter(x0)
    sigma = Parameter(yy[yy > (max(yy) * np.exp(-1 / 2))].size / 2)
    height = Parameter(max(yy))
    background = Parameter(min(yy))
    def f(x):
        return height() * np.exp(-((x - mu()) / sigma()) ** 2/2) + background()
    return fit(f, [mu, sigma, height, background], yy)

def fitgauss1d_moment(xx, yy, truncate = True):
    '''
    Fit 1d gaussian function using moment.
    :param xx:
    :param yy:
    :param truncate:
    :return: x0, sigma
    '''
    if truncate:
        x0, xx, yy = truncate_center(xx,yy)
    else:
        x0 = np.sum(xx * yy) / np.sum(yy)
    cm0 = np.sum(yy)
    cm2 = np.sum((xx - x0) ** 2 * yy)
    cm4 = np.sum((xx - x0) ** 4 * yy)
    s0 = xx.size
    s2 = np.sum((xx - x0) ** 2)
    s4 = np.sum((xx - x0) ** 4)
    if (cm4*s0-cm0*s4)**2-4*3*(cm2*s0-cm0*s2)*(cm4*s2-cm2*s4) > 0:
        sigma = (np.sqrt(np.abs((cm4*s0-cm0*s4+np.sqrt((cm4*s0-cm0*s4)**2-4*3*(cm2*s0-cm0*s2)*(cm4*s2-cm2*s4)))/(6*(cm2*s0-cm0*s2)))))
    else:
        sigma = np.sqrt(np.abs(np.sum((xx - x0) ** 2 * yy) / np.sum(yy)))
    return x0, sigma

def truncate_center(xx,yy):
    '''
    Truncate the data to reduce the effect of the noise.
    The final x0 will be at the center of xx1.
    This method is only valid when xx is ascending equal-spacing array
    and yy is a symmetric function with ignorable tail at the edge of xx.
    :param xx:
    :param yy:
    :return: x0, xx, yy
    '''
    x0 = np.sum(xx * yy) / np.sum(yy)
    xx0 = []
    while not np.array_equal(xx0, xx):
        xx0 = xx
        if x0 - xx0[0] < xx0[-1] - x0:
            xx = xx0[:xx0[xx0 < x0 * 2 - xx0[0]].size + 1]
            yy = yy[:xx0[xx0 < x0 * 2 - xx0[0]].size + 1]
        elif x0 - xx0[0] > xx0[-1] - x0:
            xx = xx0[-xx0[xx0 > x0 * 2 - xx0[-1]].size - 1:]
            yy = yy[-xx0[xx0 > x0 * 2 - xx0[-1]].size - 1:]
        else:
            xx = xx0
        x0 = np.sum(xx * yy) / np.sum(yy)

    return x0, xx, yy

def gauss1d(mu,sigma,max,x):
    return max * np.exp(-(x - mu) ** 2 / (2 * sigma ** 2))

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    xx = np.arange(0,4000,1)
    yy = gauss1d(1000,200,1,xx)+1+np.random.rand(xx.size)*0.5
    plt.plot(xx,yy)
    plt.show()
    start_time = time.time()
    for i in range(1000):
        x0, sigma = fitgauss1d_moment(xx, yy)
    print("--- %.8f seconds ---" % (time.time() - start_time))
    print(x0,sigma)

    start_time = time.time()
    for i in range(1000):
        result = fitgauss1d(xx, yy)
    print("--- %.8f seconds ---" % (time.time() - start_time))
    print(result)

