import numpy as np

def fitgauss1d(xx,yy,truncate = True):
    # Truncate the data to reduce the effect of the noise.
    # The final x0 will be at the center of xx1.
    # This method is only valid when xx is ascending equal-spacing array.
    if truncate:
        x0, xx, yy = truncate_center(xx,yy)
    else:
        x0 = np.sum(xx * yy) / np.sum(yy)


    sigma = np.sqrt(np.abs(np.sum((xx - x0) ** 2 * yy) / np.sum(yy)))
    return x0, sigma

def truncate_center(xx,yy):
    x0 = np.sum(xx * yy) / np.sum(yy)
    xx0 = []
    xx1 = xx
    while not np.array_equal(xx0, xx1):
        xx0 = xx1
        if x0 - xx0[0] < xx0[-1] - x0:
            xx1 = xx0[0:xx0[xx0 < x0 * 2 - xx0[0]].size + 1]
            yy = yy[0:xx0[xx0 < x0 * 2 - xx0[0]].size + 1]
        elif x0 - xx0[0] > xx0[-1] - x0:
            xx1 = xx0[-xx0[xx0 > x0 * 2 - xx0[-1]].size - 1:-1]
            yy = yy[-xx0[xx0 > x0 * 2 - xx0[-1]].size - 1:-1]
        else:
            xx1 = xx0
        x0 = np.sum(xx1 * yy) / np.sum(yy)

    return x0, xx1, yy

def gauss1d(mu,sigma,max,x):
    func = lambda t: max * np.exp(-(t - mu) ** 2 / (2 * sigma ** 2))
    return func(x)

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    xx = np.arange(4000)
    yy = gauss1d(1000,200,1,xx)
    plt.plot(xx,yy)
    plt.show()
    x0, xx, yy = truncate_center(xx,yy)
    print(x0)
    print(xx)
    print(yy)