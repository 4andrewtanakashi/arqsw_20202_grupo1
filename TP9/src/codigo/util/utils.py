import os
import json
import collections

def save_obj_to_file (obj, name_file):
    try:
        file_path = os.path.join(os.getcwd() + "/json_files/" + name_file)
        print("Path JSON: " + file_path)
        with open(file_path, 'w') as fp:
            json.dump(obj, fp)
        print("Arquivo " + name_file + " criado e salvo os dados")
        print("no diretório: {}".format(str(file_path)))
    except OSError:
        print('Algum erro aconteceu ao salvar no arquivo de JSON')

def load_obj_to_file (name_file):
    try:
        file_path = os.path.join(os.getcwd() + "/json_files/" + name_file)
        with open(file_path, 'r') as fp:
            return json.load(fp)
        print("Arquivo " + name_file + " carregado para objeto com sucesso")
    except OSError:
        print('Algum erro aconteceu ao carregar no arquivo de JSON')

def attributes_from_project (externalList):
    for elem_dict in externalList:
        elem_dict["structure"]["count_attr_from_proj"] = 0
        for elem_dictII in externalList:
            if elem_dict["name_obj"] != elem_dictII["name_obj"]:
                 if elem_dict["type"].__contains__(elem_dictII["name_obj"]):
                    elem_dict["structure"]["count_attr_from_proj"] += 1
                    pass
            else:
                pass
