from sklearn.linear_model import LinearRegression as LR


def f_test(X, y):
    '''
    type(X) == 2D Pandas dataframe or 2D array

    RSS = B0 + B1x1 + B2x2 +...+ Bpxp

    X.columns[j] == name of column in dataframe aka j
    X[X.columns[j]][i] == i.th value of column j
    sum([ B[j] * X[X.columns[j][i]] ]) == B1x1 +...+ Bpxp
    '''

    n = len(y)
    p = len(X.columns)

    y_mean = sum(y) / n

    reg = LR().fit(X, y)
    intercept = reg.intercept_
    B = reg.coef_  # List

    TSS = sum([(y[i] - y_mean) ** 2 for i in range(n)])
    RSS = sum([(y[i] - (intercept + sum(
        [B[j] * X[X.columns[j]][i] for j in range(p)]))) ** 2 for i in
               range(n)])

    F = ((TSS - RSS) / p) / (RSS / (n - p - 1))

    return F  # Returns the F-statistic, doesn't perform an F-test