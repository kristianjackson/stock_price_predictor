import yfinance
import numpy as np
from scipy import stats

STOCK = 'AAPL'
START_DATE = '2016-01-01'
END_DATE = '2020-09-04'

stock_data = yfinance.download(
    STOCK,
    START_DATE,
    END_DATE,
)


def calculate_prereq(values):
    std = np.std(values)
    mean = np.mean(values)
    return std, mean


def calculate_distribution(mean, std):
    norm = stats.norm(mean, std)
    return norm


def extrapolate(norm, x):
    return norm.pdf(x)


def values_to_norm(dicts):
    for dictionary in dicts:
        for term in dictionary:
            std, mean = calculate_prereq(dictionary[term])
            norm = calculate_distribution(mean, std)
            dictionary[term] = norm
    return dicts


def compare_possibilities(dicts, x):
    probabilities = []
    for dictionary in dicts:
        dict_probs = []
        for i in range(len(x)):
            value = x[i]
            dict_probs.append(extrapolate(dictionary[i], value))
        probabilities.append(np.prod(dict_probs))
    return probabilities.index(max(probabilities))


drop = {}
increase = {}

for day in range(10, len(stock_data) - 1):
    previous_close = stock_data['Close'][day - 10:day]
    ratios = []
    for i in range(1, len(previous_close)):
        ratios.append(previous_close[i] / previous_close[i - 1])
    if stock_data['Close'][day + 1] > stock_data['Close'][day]:
        for i in range(len(ratios)):
            if i in increase:
                increase[i] += (ratios[i], )
            else:
                increase[i] = ()
    elif stock_data['Close'][day + 1] < stock_data['Close'][day]:
        for i in range(len(ratios)):
            if i in drop:
                drop[i] += (ratios[i], )
            else:
                drop[i] = ()

new_close = stock_data['Close'][-11:-1]
ratios = []
for i in range(1, len(new_close)):
    ratios.append(new_close[i] / new_close[i - 1])
for i in range(len(ratios)):
    if i in increase:
        increase[i] += (ratios[i], )
    else:
        increase[i] = ()

X = ratios
print(X)
dicts = [increase, drop]
dicts = values_to_norm(dicts)
compare_possibilities(dicts, X)
