__author__ = 'Lukianchikov'


# Code from Chapter 15 of Machine Learning: An Algorithmic Perspective
# by Stephen Marsland (http://seat.massey.ac.nz/personal/s.r.marsland/MLBook.html)

# You are free to use, change, or redistribute the code in any way you wish for
# non-commercial purposes, but please maintain the name of the original author.
# This code comes with no warranty of any kind.

# Stephen Marsland, 2008

# The 1D Kalman filter

from pylab import *
from numpy import *
import securities as sc


def kalman(obs=None,mu_init=array([-0.37727]), cov_init=0.1*ones((1)), nsteps=50):
    """obs - the price series for which we build kalman approximation of the average.
    Set nsteps to the equal amount as the obs size.
    returns obs-1 number of averages."""
    ndim = shape(mu_init)[0]
    if obs is None:
        mu_init = tile(mu_init, (1,nsteps))
        cov_init = tile(cov_init, (1, nsteps))
        obs = random.normal(mu_init, cov_init, (ndim, nsteps))
    Sigma_x = eye(ndim)*1e-5
    A = eye(ndim)
    H = eye(ndim)
    mu_hat = 0
    cov = eye(ndim)
    R = eye(ndim)*0.01
    m = zeros((ndim, nsteps), dtype=float)
    ce = zeros((ndim, nsteps), dtype=float)
    for t in range(1, nsteps):
        # Make prediction
        mu_hat_est = dot(A, mu_hat)
        cov_est = dot(A, dot(cov, transpose(A))) + Sigma_x
        # Update estimate
        error_mu = obs[:, t] - dot(H,mu_hat_est)
        error_cov = dot(H, dot(cov, transpose(H))) + R
        K = dot(dot(cov_est, transpose(H)), linalg.inv(error_cov))
        mu_hat = mu_hat_est + dot(K, error_mu)
        #m[:,:,t] = mu_hat
        m[:, t] = mu_hat
        if ndim > 1:
            cov = dot((eye(ndim) - dot(K, H)), cov_est)
        else:
            cov = (1-K)*cov_est
        ce[:, t] = cov
    return m[0, 1:]

    #figure()
    #plot(obs[0, :], 'ko', ms=6)
    #plot(m[0, 1:], 'k-', lw=3)
    #plot(m[0,:]+20*ce[0,:],'k--',lw=2)
    #plot(m[0,:]-20*ce[0,:],'k--',lw=2)
    #legend(['Noisy Datapoints','Kalman estimate','Covariance'])
    #legend(['Prices','Kalman estimate'])
    #xlabel('Time')
    #show()




#mu_init=array([-0.37727])
#ndim = shape(mu_init)[0]
#cov_init=0.1*ones((1))
#nsteps=50
#cov_init = tile(cov_init,(1, nsteps))
#xxx = random.normal(mu_init, cov_init, (ndim,nsteps))
#print(type(xxx))
#print(xxx)
#print(shape(xxx))
#yyy = xxx[0,:]

#print(shape(yyy))
somestock=sc.Stock("IBM")
obs = array([somestock.get_prices(60).values])
print(type(obs))
print(shape(obs))
kalman(obs, nsteps=60)
