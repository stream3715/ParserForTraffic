import datetime
import time

import pandas as pd


def parselog():

    logs = pd.read_csv('secure.log', sep=' ', header=None)
    del_array = []

    logs['unixtime'] = 0
    logs = logs.loc[:,
           ["unixtime", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]]

    for log_index, log_data in logs.iterrows():
        if str(log_data[4]).find("sshd") == -1:
            del_array.append(log_index)
        elif str(log_data[4]) == logs.at[(log_index - 1), 4]:
            del_array.append(log_index)
        else:
            dt_data = "2019-06-" + str(log_data[1]) + " " + str(log_data[2])
            logs.at[log_index, "unixtime"] = time.mktime(
                (datetime.datetime.strptime(dt_data, '%Y-%m-%d %H:%M:%S')).timetuple())

    logs = logs.drop(del_array)

    logs.to_csv("changed.csv")