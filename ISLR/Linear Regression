def LinearRegression(x: list, y: list) -> int:
    
    '''
    a = slope
    b = intercept
    '''
    
    n = len(x)
    x_mean = sum(x) / n
    y_mean = sum(y) / n
    
    num = 0
    den = 0
    
    for i in range(n):
        num = num + (x[i] - x_mean) * (y[i] - y_mean)
        den = den + (x[i] - x_mean)**2
        
    a = num / den
    b = y_mean - (a * x_mean)
    
    return a, b
