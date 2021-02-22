from math import sqrt
import numpy as np
from util.utils import load_obj_to_file, save_obj_to_file
import sys
import random


clusters_names = ['ClusterA', 'ClusterB', 'ClusterC']


def calculate_similarity_Jaccard(x1, x2):
    array_all = []
    a = 0
    b = 0
    c = 0

    for i in range(len(x1)-1):
        inter_ele = np.intersect1d(x1[i], x2[i])
        for elem_intersection in inter_ele:
            if elem_intersection != []:
                array_all.append(elem_intersection)
    a = len(array_all)

    x1_attr_proj = x1[len(x1)-1]['count_attr_from_proj']
    x2_attr_proj = x2[len(x2)-1]['count_attr_from_proj']
    if x1_attr_proj + x2_attr_proj > 0:
        a += a * (x1_attr_proj / x2_attr_proj) if x1_attr_proj < x2_attr_proj else a * (x2_attr_proj / x1_attr_proj)

    a = (x1[len(x1)-1]['count_eleme_view'] * x2[len(x2)-1]['count_eleme_view'])

    array_all = []
    for i in range(len(x1)-1):
        inter_ele = np.setdiff1d(x1[i], x2[i])
        for elem_diff in inter_ele:
            if elem_diff != []:
                array_all.append(elem_diff)
    b = len(array_all)

    array_all = []
    for i in range(len(x1)-1):
        inter_ele = np.setdiff1d(x2[i], x1[i])
        for elem_diff in inter_ele:
            if elem_diff != []:
                array_all.append(elem_diff)
    c = len(array_all)

    quotient = (a + b + c)
    jaccard = a / quotient if quotient != 0 else 0

    return jaccard


def get_nearest_neighbors(X_train, y_train, x, files_names, k):
  distances = []
  for i in range(len(X_train)):
      if not (X_train[i] == x).all():
          distances.append((calculate_similarity_Jaccard(X_train[i], x), y_train[i], files_names[i]))

  nearest_neighbors = sorted(distances, reverse=True, key=lambda tup: tup[0])[:k]

  return list(zip(*nearest_neighbors))[1]


def classify(nearest_neighbors, classes):
    count_classes = []
    for class_id in range(len(classes)):
        count_classes.append((nearest_neighbors.count(class_id), class_id))

    return max(count_classes)[1]


def knn_algorithm(X_train, y_train, files_names):
    predictions = {clusters_names[0]: [], clusters_names[1]: [], clusters_names[2]: []}
    for i in range(len(X_train)):
        nearest_neighbors = get_nearest_neighbors(X_train, y_train, X_train[i], files_names, k = 1)
        y = classify(nearest_neighbors, clusters_names)
        predictions[clusters_names[y]].append(files_names[i])

    return predictions


def use_database(file):
    dictionary_data = load_obj_to_file(file)

    list_X = []
    list_Y = []
    files_names = []
    quant_classes = len(dictionary_data)
    cont = 0
    for elem_dict in dictionary_data:
        list_internal_X = []
        list_internal_Y = []
        list_internal_X.append(elem_dict['type'])
        list_internal_X.append(elem_dict['imports'])
        list_internal_X.append(elem_dict['annotation'])
        list_internal_X.append(elem_dict['method_names'])
        list_internal_X.append(elem_dict['invocation'])
        list_internal_X.append(elem_dict['structure'])

        list_X.append(list_internal_X)
        if cont <= quant_classes / 3:
            list_Y.append(0)
        elif cont > quant_classes / 3 and cont < (quant_classes - quant_classes / 3 ):
            list_Y.append(1)
        elif cont >= (quant_classes / 3):
            list_Y.append(2)

        files_names.append(elem_dict['file_name'])
        cont += 1
    X_train, y_train = np.array(list_X,dtype=list), np.array(list_Y,dtype=list)

    return X_train, y_train, files_names


def clusterization(file):
    X_train, y_train, files_names = use_database(file)

    predictions = knn_algorithm(X_train, y_train, files_names)

    return predictions
