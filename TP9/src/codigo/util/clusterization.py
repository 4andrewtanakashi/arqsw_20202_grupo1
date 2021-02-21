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

    for i in range(len(x1)):
        inter_ele = np.intersect1d(x1[i], x2[i])
        for elem_intersection in inter_ele:
            if elem_intersection != []:
                array_all.append(elem_intersection)
    a = len(array_all)

    array_all = []
    for i in range(len(x1)):
        inter_ele = np.setdiff1d(x1[i], x2[i])
        for elem_diff in inter_ele:
            if elem_diff != []:
                array_all.append(elem_diff)
    b = len(array_all)


    array_all = []
    for i in range(len(x1)):
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

  print()
  print(X_train)
  print('\n', x)
  print('\nDistancias:\n', distances)
  nearest_neighbors = sorted(distances, reverse=True, key=lambda tup: tup[0])[:k]
  print('\nVizinhos mais próximos:\n', nearest_neighbors)

  return list(zip(*nearest_neighbors))[1]


def classify(nearest_neighbors, classes):
    count_classes = []

    for class_id in range(len(classes)):
        count_classes.append((nearest_neighbors.count(class_id), class_id))

    return max(count_classes)[1]


def knn_algorithm(X_train, y_train, files_names):
    predictions = {clusters_names[0]: [], clusters_names[1]: [], clusters_names[2]: []}
    for i in range(len(X_train)):
        nearest_neighbors = get_nearest_neighbors(X_train, y_train, X_train[i], files_names, k = 5)
        print('\nVizinhos mais próximos (Label):\n', nearest_neighbors, '\n')
        y = classify(nearest_neighbors, clusters_names)
        print(y, '\n')
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


        list_X.append(list_internal_X)
        # if cont <= quant_classes / 3:
        #     list_Y.append(0)
        # elif cont > quant_classes / 3 and cont <= (quant_classes / 2):
        #     list_Y.append(1)
        # elif cont > (quant_classes / 3):
        #     list_Y.append(2)
        list_Y.append(random.randint(0, 2))
        files_names.append(elem_dict['file_name'])
        cont += 1

    X_train, y_train = np.array(list_X,dtype=list), np.array(list_Y,dtype=list)

    return X_train, y_train, files_names


def clusterization(file):
    X_train, y_train, files_names = use_database(file)
    print()
    print(X_train)
    print()
    print(y_train)
    print()
    print(files_names)
    # sys.exit()

    predictions = knn_algorithm(X_train, y_train, files_names)

    # print(predictions)
    # decod_predictions = [clusters_names[p] for p in predictions]

    # final_clusters = sorted(zip(files_names, decod_predictions), key=lambda tup: tup[1])

    return predictions
