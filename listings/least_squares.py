#!/usr/bin/env python

"""
LEAST SQUARES PARAMETER ESTIMATION

GEOS F4/669, R. Grapenthin, UAF
"""

import numpy as np
import matplotlib.pyplot as plt
import math

# Forward model of a line y = a+bx
print("Forward model of a line y = a+bx")

a       = 1
b       = 3.5
std_dev = 0.5

x = np.vstack(np.arange(0, 4, 0.1))
y = np.vstack(a+b*x)

plt.figure()
plt.plot(x, y)
plt.plot(x, y, 'o')
plt.xlabel("x")
plt.ylabel("y")
plt.show()

# Forward model with noise: y = a + bx + e
print("Forward model of a line with noise yn = a + bx + e")

noise = np.vstack(np.random.normal(0,std_dev,len(x)))
yn = np.vstack(a+b*x+noise)

plt.figure()
plt.plot(x, y)
plt.plot(x, yn, "o")
plt.xlabel("x")
plt.ylabel("y")
plt.show()

# Now we can't see the line any more. These are our data.
print("Clean forward model removed ... these are the measured data.")

plt.figure()
plt.plot(x, yn, "o")
plt.xlabel("x")
plt.ylabel("y")
plt.show()

a_guess = 0.0
b_guess = 4.5
y_guess = np.vstack(a_guess + b_guess * x)

print( "Residuals after guessing a model (a=%f, b=%f) ..." % (a_guess, b_guess))

G      = np.matrix(np.hstack((np.vstack(np.ones(len(x))), x)))
m      = np.vstack((a_guess,b_guess))
resids = yn - G*m

plt.figure()
plt.subplot(2,1,1)
plt.plot(x, yn, "o")
plt.plot(x, y_guess)
plt.xlabel("x")
plt.ylabel("y")
plt.subplot(2,1,2)
plt.plot(x, resids, "o")
plt.xlabel("x")
plt.ylabel("residuals")

plt.show()

print("Respective norms ...")

print("L2-norm:  %f" % ( math.sqrt(sum([v**2   for v in resids])) ))
print("L1-norm:  %f" % ( math.sqrt(sum([abs(v) for v in resids])) ))

print("Multiply last residual by 100 to simulate large outlier... impact on norms:")

resids[-1] = resids[-1]*100
print("L2-norm:  %f" % ( math.sqrt(sum([v**2   for v in resids])) ))
print("L1-norm:  %f" % ( math.sqrt(sum([abs(v) for v in resids])) ))

#we want to invert the data for the model parameters:

print("Inversion ... model parameters:")

m = (G.T*G).I * G.T * yn
m = m.getA()
print(m)

print("Calculate and plot forward model from estimated model parameters...")

yf = m[0]+m[1]*x
plt.figure()
plt.plot(x, yn, "o")
plt.plot(x, yf)
plt.xlabel("x")
plt.ylabel("y")
plt.show()

print("Residuals and respective norms ")
resids = yn-yf
print("L2-norm:  %f" % ( math.sqrt(sum([v**2   for v in resids])) ))
print("L1-norm:  %f" % ( math.sqrt(sum([abs(v) for v in resids])) ))

plt.figure()
plt.plot(x, resids, "o")
plt.xlabel("x")
plt.ylabel("residuals")
plt.show()

