import pandas as pd
from math import sqrt

def LinearRegression(x: list, y: list) -> int:
    '''
    a = slope
    b = intercept
    '''
    def s_std():
        return sqrt(sum([(x[i] - x_mean)**2]) / (n - 1))

    n = len(x)
    x_mean = sum(x) / n
    y_mean = sum(y) / n

    num = 0
    den = 0

    for i in range(n):
        num = num + (x[i] - x_mean) * (y[i] - y_mean)
        den = den + (x[i] - x_mean) ** 2

    a = num / den
    b = y_mean - (a * x_mean)

    t_stat = (b - x_mean) / (s_std() / n)

    return a, b, t_stat

data = pd.read_csv('Credit.csv')
gender_val = []

for i in range(len(data['Gender'])):
    if data['Gender'][i] == 'Male':
        gender_val.append(0)
    else:
        gender_val.append(1)

data['gender_val'] = gender_val

print(LinearRegression(data['gender_val'], data['Balance']))


