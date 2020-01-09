from math import pi
from math import exp
from math import sqrt


def height(mu, stdev, x):
    first_term = 1 / (sqrt(2 * pi * stdev**2))
    exp_term = exp((-(x-mu) ** 2) / (2 * stdev**2))

    y = first_term * exp_term

    return y


def simp3_8_normalcdf(LB, UB, mu=0, stdev=1):
    """Numerical integration using Simpson's 3/8"""
    n = 3000   # Number of sub-intervals... must be divisible by 3

    # One Tailed Test
    a = LB
    b = UB
    h = (b-a) / n  # Sub-interval width

    points = [a]
    y_values = [height(mu, stdev, a)]
    threes = []
    twos = []

    for i in range(n):
        points.append(points[-1] + h)
        y_values.append(height(mu, stdev, points[-1]))

    for j in range(len(y_values)):
        if j != 0 and j != (len(y_values) - 1):

            if j % 3 != 0:
                threes.append(y_values[j])

            else:
                twos.append(y_values[j])

    I = ((3 * h / 8) * (y_values[0]
                        + 3 * sum(threes)
                        + 2 * sum(twos)
                        + y_values[-1]))

    return I


def trap_normalcdf(LB, UB, mu=0, stdev=1):
    """Numerical integration using trapezoidal rule"""
    def area(x1, x2, y1, y2):
        return 0.5 * (y1+y2) * (x2-x1)

    n = 1000  # Number of sub-intervals

    a = LB
    b = UB
    w = (b-a) / n  # Width of sub-interval

    points = [a]
    y_values = [height(mu, stdev, a)]
    traps = []  # Areas of trapezoids

    for i in range(n):
        points.append(points[-1] + w)
        y_values.append(height(mu, stdev, points[-1]))
        traps.append(area(points[i], points[i + 1],
                          y_values[i], y_values[i + 1]))

    return sum(traps)


print(simp3_8_normalcdf(-5, 5))

print(trap_normalcdf(-5, 5))


