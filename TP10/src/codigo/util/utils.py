import os
import json
import collections
from util.B_Colors import *

def save_obj_to_file (obj, path_name_file):
    try:
        file_path = os.path.join(os.getcwd() + path_name_file)
        arr_file = path_name_file.split("/")
        name_file = arr_file[len(arr_file)-1]
        if name_file.endswith(".json"):
            with open(file_path, 'w') as fp:
                json.dump(obj, fp)
        else:
            with open(file_path, 'w') as fp:
                fp.writelines(obj)
        print(B_Colors.OKBLUE + "Arquivo " + name_file + " criado e salvo os dados" + B_Colors.ENDC)
        print(B_Colors.OKBLUE + "no diretório: {}".format(str(file_path.split(name_file)[0])) + B_Colors.ENDC + "\n")
    except OSError:
        print(B_Colors.FAIL + 'Algum erro aconteceu ao salvar no arquivo' + B_Colors.ENDC)

def load_obj_to_file (path_name_file):
    try:
        file_path = os.path.join(os.getcwd() + path_name_file)
        with open(file_path, 'r') as fp:
            arr_file = path_name_file.split("/")
            name_file = arr_file[len(arr_file)-1]
            print(B_Colors.OKBLUE + "Arquivo " + name_file + " carregado para objeto com sucesso" + B_Colors.ENDC  + "\n")
            return json.load(fp)
    except OSError:
        print(B_Colors.FAIL + 'Algum erro aconteceu ao carregar no arquivo de JSON' + B_Colors.ENDC)

def attributes_from_project (externalList):
    for elem_dict in externalList:
        elem_dict["structure"]["count_attr_from_proj"] = 0
        for elem_dictII in externalList:
            if elem_dict["name_obj"] != elem_dictII["name_obj"]:
                 if elem_dict["type"].__contains__(elem_dictII["name_obj"]):
                    elem_dict["structure"]["count_attr_from_proj"] += 1
                    continue
            else:
                continue

def delete_elems_from_dict (dict_obj, key, content):
    dict_obj[key].remove(content)
    if (dict_obj[key] == []):
        del dict_obj[key]

def clean_emptys (Ligacoes):
    lig_cpy = copy_content(Ligacoes)
    for k_lig, content_lig in lig_cpy.items():
        if content_lig == {}: # ex.: k_lig: {}
            del Ligacoes[k_lig]
            continue
        for k_lig_inter, content_lig_inter in content_lig.items():
            if content_lig_inter == []: # ex.:'k_lig': {'content_lig_inter': []}
                del Ligacoes[k_lig][k_lig_inter]

def if_not_exist_rule_in_others_sessions (k_param, content_param, Ligacoes, flag_del=False):
    for k_lig, content_lig in Ligacoes.items():
        if k_lig != k_param:
            for k_lig_inter, content_lig_inter in content_lig.items():
                if content_lig_inter.__contains__(content_param):
                    if flag_del:
                        delete_elems_from_dict(content_lig_inter, k_lig_inter, content_param)
                    return False
    return True

def copy_content(Ligacoes_rules):
    copy = {}
    for key, content in Ligacoes_rules.items():
        copy[key] = {}
        for key_internal, cont_internal in content.items():
            copy[key][key_internal] = []
            for elem_cont in cont_internal:
                copy[key][key_internal].append(elem_cont)
    return copy

def load_ligacoesUnicas (LigacoesUnicas, Ligacoes_rules):
    Ligacoes_copy = copy_content(Ligacoes_rules)
    for k_lig_Pac, content_lig_Pac in Ligacoes_copy.items():
        LigacoesUnicas[k_lig_Pac] = {}
        for k_lig_inter, cont_lig_inter in content_lig_Pac.items(): #Pode / Deve
            LigacoesUnicas[k_lig_Pac][k_lig_inter] = []
            for elem_content in content_lig_Pac[k_lig_inter]: # nomes de classes e/ou pacotes
                if if_not_exist_rule_in_others_sessions(k_lig_Pac, elem_content, Ligacoes_rules):
                    LigacoesUnicas[k_lig_Pac][k_lig_inter].append(elem_content)
                    delete_elems_from_dict(Ligacoes_rules[k_lig_Pac], k_lig_inter, elem_content)


def generated_rules_unique (obj):
    LigacoesUnicasPacotes = {}
    LigacoesDePacotes = obj["LigacoesDePacotes"]
    load_ligacoesUnicas(LigacoesUnicasPacotes, LigacoesDePacotes)

    clean_emptys(LigacoesUnicasPacotes)
    clean_emptys(LigacoesDePacotes)
    return LigacoesUnicasPacotes
