import collections
import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.font_manager import FontProperties

fp = FontProperties(fname=r'/System/Library/Fonts/ヒラギノ明朝 ProN.ttc', size=14)

start_time = 1560092400
end_time = 1560438000
unix_tick = 60


def split():
    df = pd.read_csv('./changed.csv')
    count_list = []
    count_dict = {}

    split_time = start_time
    i = 0

    try:

        count = 0

        while split_time <= end_time and i < len(df):
            time = df.loc[i, "unixtime"]
            if time > split_time + unix_tick:
                count_list.append(count)
                count_dict[split_time] = count
                print(str(split_time) + " of " + str(end_time) + " in " + str(i))
                while split_time + unix_tick < time:
                    count_dict[split_time] = 0
                    count_list.append(0)
                    split_time += unix_tick
                count = 1

            else:
                count += 1

            i += 1

    except KeyError as ke:
        print("reach the end : " + str(ke))

    d = collections.Counter(count_list)
    x = range(11)
    values = [d[key] for key in x]
    lamb = (i - 1) / 5760.0
    print("lamb = " + str(lamb))
    poisson_val = [poisson_probability(n, lamb) for n in x]

    count_sum = 0.0
    for item in values:
        count_sum += item

    for index, item in enumerate(values):
        values[index] = item / count_sum

    left = np.arange(len(x))
    width = 0.3
    plt.bar(left, values, width=width, label="観測データ")
    plt.bar(left + width, poisson_val, width=width, label="ポアソン分布")

    x_ticks = 1
    plt.xticks(left + width / 2, x[::x_ticks])
    plt.ylim(0, 1)
    plt.title("1分あたりの到着数の確率質量関数", fontproperties=fp)
    plt.xlabel("到着数 [回/min]", fontproperties=fp)
    plt.ylabel("確率", fontproperties=fp)
    plt.legend(prop=fp)
    plt.show()


def poisson_probability(n, lambda_poisson):
    return (lambda_poisson ** n) * math.exp(-lambda_poisson) / math.factorial(n)

