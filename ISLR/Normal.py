from math import pi
from math import exp
from math import sqrt

'''
def height(mu, stdev, x):
    first_term = (sqrt(2 * pi * stdev**2)) ** -1
    exp_term = exp((-(x-mu) ** 2) / (2 * stdev**2))

    y = first_term * exp_term

    return y
'''


def height(mu, stdev, x):
    return x**3


def normalcdf(LB, UB, mu=0, stdev=1):
    n = 3   # Number of sub-intervals... must be divisible by 3

    # One Tailed Test
    a = LB
    b = UB
    h = (b-a) / n  # Sub-interval width

    points = [0]
    y_values = [height(mu, stdev, 0)]
    threes = []
    twos = []

    for i in range(n):
        points.append(points[-1] + h)
        y_values.append(height(mu, stdev, points[-1]))

    for j in range(len(points)):
        if j != 0 and j != (len(points) - 1):

            if j % 3 != 0:
                threes.append(points[j])

            else:
                twos.append(points[j])

    I = ((3 * h / 8) * (y_values[0]
                        + 3 * sum(threes)
                        + 2 * sum(twos)
                        + y_values[-1]))

    print(points)
    print(y_values)

    #print(len(points))
    
    print(threes)
    print(twos)

    return I

print(normalcdf(0, 6))