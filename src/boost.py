import numpy as np
import pandas as pd
import os
import json
from sklearn.ensemble import GradientBoostingClassifier

from src.utils import get_data
from src.const import *


def boost(data_set, max_depth_values=(5,), n_estimators_values=(100,), min_sample_split_values=(2,),
          trainning_sizes=(-1,)):
    x_train, y_train, x_test, y_test = get_data(data_set=data_set,
                                                batch_format="sklearn")

    max_depth_values = list(max_depth_values)
    n_estimators_values = list(n_estimators_values)
    min_sample_split_values = list(min_sample_split_values)

    data = []
    data_dict = {}
    for max_depth in max_depth_values:
        data_dict[max_depth] = {}
        for n_estimators in n_estimators_values:
            data_dict[max_depth][n_estimators] = {}
            for min_sample_split in min_sample_split_values:
                data_dict[max_depth][n_estimators][min_sample_split] = {}
                for train_size in trainning_sizes:
                    clf = GradientBoostingClassifier(max_depth=max_depth,
                                                     n_estimators=n_estimators,
                                                     min_samples_split=min_sample_split
                                                     )
                    clf.fit(X=np.array(x_train[:train_size]),
                            y=np.array(y_train[:train_size]).ravel())
                    score = clf.score(X=x_test,
                                      y=y_test.ravel())
                    data.append((score, max_depth, n_estimators, min_sample_split, train_size))
                    data_dict[max_depth][n_estimators][min_sample_split][train_size] = score

    data_frame = pd.DataFrame(data, columns=["score", "max_depth", "n_estimators", "min_sample_split", "train_size"])
    data_dict_indexes = {'max_depth': 0,
                         'n_estimators': 1,
                         'min_sample_split': 2,
                         'train_size': 3}
    return data_frame, data_dict, data_dict_indexes


if __name__ == "__main__":
    data_set_name = "creditcard"
    df, dd, ddi = boost(data_set_name,
                        max_depth_values=range(1, 5, 1),
                        n_estimators_values=range(10, 200, 10),
                        min_sample_split_values=range(2, 10, 2),
                        trainning_sizes=[-1])
    if not os.path.exists("stats"):
        os.makedirs("stats")
    df.to_csv(path_or_buf="stats/boost_" + data_set_name + ".csv")
    json.dump(dd, open("stats/boost_" + data_set_name + "_dict.json", 'w'))
    json.dump(ddi, open("stats/boost_" + data_set_name + "_dict_indexes.json", 'w'))
