from math import pi
from math import exp
from math import sqrt

def height(mu, stdev, x):
    first_term = (sqrt(2 * pi * stdev**2)) ** -1
    exp_term = exp((-(x-mu) ** 2) / (2 * stdev**2))

    y = first_term * exp_term

    return y

def normalcdf(LB, UB, mu=0, stdev=1):
    n = 12  # Number of sub-intervals

    # One Tailed Test
    a = 0
    b = UB
    h = (b-a) / n  # Sub-interval width

    points = [0]
    y_values = [height(mu, stdev, 0)]

    for i in range(n):
        points.append(points[-1] + h)
        y_values.append(height(mu, stdev, points[-1]))

    return y_values


print(normalcdf(0, 400))