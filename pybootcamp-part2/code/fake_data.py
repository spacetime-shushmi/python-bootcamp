import numpy as np
import george
from george.kernels import ExpSquaredKernel, Matern32Kernel
from matplotlib import pyplot as plt
import seaborn as sns
sns.set()


def create_fake_data():
    # fake 1D lightcurve. 
    # data is a constant, plus and airmass term, plus a random cloud
    x = np.linspace(0,8,101)

    # model cloud using Gaussian Process
    kernel = 2*Matern32Kernel(1.0) 
    gp = george.GP(kernel)
    gp.compute(x, 0.1*np.ones_like(x))
    cloud = np.fabs(gp.sample(x))

    # const + airmass + cloud
    ybase = 20.0 + 5*np.sin(np.pi*x/12.) - cloud
    plt.plot(ybase)
    plt.show()

    # stack many times to get 2D array [stars,hours]
    nstars = 20
    data = np.repeat(ybase[:,np.newaxis],nstars,axis=1).T

    # add gaussian noise (amplitude around 1)
    data += np.random.normal(loc=0,scale=0.8,size=data.shape)
    return data
    
from itertools import count
filename = ('star_data_{0}.csv'.format(i) for i in count(1))
for i in range(12):
    data = create_fake_data()
    np.savetxt( next(filename), data, delimiter=',')


