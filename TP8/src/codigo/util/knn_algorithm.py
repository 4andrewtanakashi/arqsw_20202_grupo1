from math import sqrt
import numpy as np
from util.utils import load_obj_to_file, save_obj_to_file

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

    jaccard = a/(a+b+c)

    return jaccard


def get_nearest_neighbors(X_train, y_train, x, k):
  distances = []
  for i in range(len(X_train)):
    distances.append((calculate_similarity_Jaccard(X_train[i], x), y_train[i]))

  nearest_neighbors = sorted(distances)[:k]

  return list(zip(*nearest_neighbors))[1]


def use_database(file):
    dicionary_data = load_obj_to_file(file)

    list_X = []
    list_Y = []
    for elem_dict in dicionary_data:
        list_internal_X = []
        list_internal_Y = []
        list_internal_X.append(elem_dict['type'])
        list_internal_X.append(elem_dict['imports'])
        list_internal_X.append(elem_dict['annotation'])
        i = 0
        while (i < len(elem_dict['annotation'])) and list_internal_Y == []:
            if (elem_dict['annotation'][i].__contains__("Repository")):
                list_internal_Y.append("Repository")
            elif (elem_dict['annotation'][i].__contains__("Controller")):
                list_internal_Y.append("Controller")
            elif (elem_dict['annotation'][i].__contains__("Service")):
                list_internal_Y.append("Service")
            elif (elem_dict['annotation'][i].__contains__("Entity")):
                list_internal_Y.append("Model")
            i += 1

        list_internal_Y.append(elem_dict['name_obj'])
        list_X.append(list_internal_X)
        list_Y.append(list_internal_Y)



    X_train, y_train = np.array(list_X,dtype=list), np.array(list_Y,dtype=list)

    return X_train, y_train



def knn_algorithm(file):
    X_train, y_train = use_database(file)

    predictions = []
    nearest_neighbors = ""
    for x in X_train:
        nearest_neighbors = get_nearest_neighbors(X_train, y_train, x, k = len(y_train))


    print('Vizinhos mais próximos :', nearest_neighbors)
    list_Model = []
    list_Repo = []
    list_Serv = []
    list_Control = []
    for nea_nei in nearest_neighbors:
        if len(nea_nei) == 2:
            if nea_nei[0] == "Model":
                list_Model.append(nea_nei[1])
            elif nea_nei[0] == "Repository":
                list_Repo.append(nea_nei[1])
            elif nea_nei[0] == "Service":
                list_Serv.append(nea_nei[1])
            elif nea_nei[0] == "Controller":
                list_Control.append(nea_nei[1])

    obj = []
    dict_model = {}
    dict_model["arquivos"] = list_Model
    obj.append(dict_model)
    save_obj_to_file(obj, "Model.json")

    obj = []
    dict_repo = {}
    dict_repo["arquivos"] = list_Repo
    obj.append(dict_repo)
    save_obj_to_file(obj, "Repository.json")

    obj = []
    dict_serv = {}
    dict_serv["arquivos"] = list_Serv
    obj.append(dict_serv)
    save_obj_to_file(obj, "Service.json")

    obj = []
    dict_control = {}
    dict_control["arquivos"] = list_Control
    obj.append(dict_control)
    save_obj_to_file(obj, "Controller.json")
