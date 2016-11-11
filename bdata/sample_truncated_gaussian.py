#! /usr/bin/python
#from scipy.stats import truncnorm
#import matplotlib.pyplot as pyplot
import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np
#a,b = 0.1,2
mu,sigma = 0.361,0.025
lower, upper = mu-(1.28*sigma), mu+(1.28*sigma) # F(mu-n*sigma),F(mu+n*sigma),n=1.28,80%
                                                # n=1.64,90%, n=2,95%
X = stats.truncnorm(
    (lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
N = stats.norm(loc=mu, scale=sigma)
np.random.seed(125)
trunc_samples=stats.truncnorm.rvs(
          (lower-mu)/sigma,(upper-mu)/sigma,loc=mu,scale=sigma,size=100)
np.random.seed(125)
samples = np.random.normal(mu,sigma,100)
print trunc_samples, "\n",samples
fig, ax = plt.subplots(2, sharex=True)
ax[0].hist(X.rvs(100), normed=True)
ax[1].hist(N.rvs(100), normed=True)

plt.show()
#mean, var, skew, kurt = truncnorm.stats(a, b, moments='mvsk')
#print mean, var, skew, kurt


#mean = 0.784051915164
#var = 0.229150936765

#a= (clip-mean)/sqrt(var)
