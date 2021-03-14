#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

"""
Obs.: Este programa pode gerar documentação com seguinte comando (no Linux):
    python3 -m pydoc -w analisador

    Para visualização no terminal: python3 -m pydoc analisador
"""
__author__ = "Andrew Takeshi and Gabriel Amorim"
__copyright__ = "Copyright 2020, Por nós"
__credits__ = ["Desenvolvido para disciplina de Arquitetura de Software"]
__devs__ = "@4andrewtanakashi & @ghamorim"
__status__ = "Production"


import os
import sys
import io

import numpy as np

from antlr4 import *
from g4_java8_python.Java8Lexer import Java8Lexer
from g4_java8_python.Java8Parser import Java8Parser
from g4_java8_python.Java8ParserListener import Java8ParserListener
from antlr4.tree.Trees import *
from util.utils import load_obj_to_file, attributes_from_project, generated_rules_unique
from util.Generated_rules_file import *
from util.Grafo import *

def use_database(file):
    dictionary_data = load_obj_to_file(file)

    list_X = []
    for elem_dict in dictionary_data:
        list_internal_X = []
        list_internal_X.append(elem_dict['type'])
        list_internal_X.append(elem_dict['imports'])
        list_internal_X.append(elem_dict['annotation'])
        list_internal_X.append(elem_dict['method_names'])
        list_internal_X.append(elem_dict['invocation'])
        list_internal_X.append(elem_dict['structure'])

        list_X.append(list_internal_X)
 
    X_train = np.array(list_X,dtype=list)

    return X_train


def find_class_deps(class_name, classes_dependences, classes_names):
    class_index = classes_names.index(class_name)
    class_deps = classes_dependences[class_index]
    print()
    print()
    print()
    print(class_deps)
    return class_deps


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
        if not (X_train[i] == np.array(x, dtype="object")).all():
            distances.append((calculate_similarity_Jaccard(X_train[i], x), y_train[i], files_names[i]))

    print()
    print('\n', x)
    print('\nDistancias:\n', distances)
    nearest_neighbors = sorted(distances, reverse=True, key=lambda tup: tup[0])[:k]
    print('\nVizinhos mais próximos:\n', nearest_neighbors)

    return list(zip(*nearest_neighbors))[1]


def classify(nearest_neighbors, classes):
    count_classes = []
    for class_id in range(len(classes)):
        count_classes.append((nearest_neighbors.count(class_id), list(classes)[class_id]))

    return max(count_classes)[1]


def knn_algorithm(X_train, y_train, files_names):
    # predictions = {clusters_names[0]: [], clusters_names[1]: [], clusters_names[2]: []}
    # for i in range(len(X_train)):

    nearest_neighbors = get_nearest_neighbors(X_train, y_train, X_train[i], files_names, k = 3)
    y = classify(nearest_neighbors, clusters_names)
    # predictions[clusters_names[y]].append(files_names[i])

    return y


if __name__ == '__main__':
    # dict_rules = load_obj_to_file(sys.argv[1])
    # tuple_lig_uni = generated_rules_unique(dict_rules)
    # Generated_rules_file.rules(tuple_lig_uni, dict_rules)


    global current_path
    directory = os.path.join(os.getcwd(), sys.argv[1])

    files_name = []
    files_path = []

    dict_templates = {}

    for root, dirs, files in os.walk(directory):
        for name in files:
            if name.endswith(".java"):
                files_name.append(name)
                file_path = os.path.join(root, name)
                files_path.append(file_path)

    print('Nome dos arquivos:\n', files_name, '\n')

    try:
        externalLista = []
        for path in files_path:
            current_path = path

            input = FileStream(path, "UTF-8")
            lexer = Java8Lexer(input)
            stream = CommonTokenStream(lexer)

            stream.fill()

            print("current_path: {}".format(str(current_path)))
            parser = Java8Parser(stream)
            tree = parser.compilationUnit()
            listener = Java8ParserListener()
            walker = ParseTreeWalker()
            walker.walk(listener, tree)
            externalLista.append(listener.dicionario)

        # help(Java8Parser)
        for x in externalLista[0]:
            print(x)
        sys.exit()


        # for i in range(len(files_name)):
        #     externalLista[i]["file_name"] = files_name[i]

        # attributes_from_project(externalLista)
        # save_obj_to_file(externalLista, "/files/json_files/" + sys.argv[3])


        # Gera um grafo contendo os acessos de cada classe do projeto de entrada
        g = Grafo("/files/json_files/" + sys.argv[3])
        for class_name in g.pseudo_adjacent_matrix:
            print(class_name + ':', g.pseudo_adjacent_matrix[class_name])


        # Carrega a arquitetura ideal de um projeto por meio de um arquivo JSON
        restrictions = load_obj_to_file(sys.argv[2])


        # Inicializa DSM de acordo com os nomes dos pacotes da arquitetura
        dsm = {}
        for accessed_package in restrictions['Pacotes']:
            dsm[accessed_package] = {}
            for access_package in restrictions['Pacotes']:
                dsm[accessed_package][access_package] = []


        # Inicia a análise de conformidade arquitetural
        for class_name in g.pseudo_adjacent_matrix:
            class_package = ''
            for package_name in restrictions['Pacotes']:
                if class_name in restrictions['Pacotes'][package_name]:
                    class_package = package_name

            class_deps_packs = set()
            for dependency_class in g.pseudo_adjacent_matrix[class_name]:
                for package_name in restrictions['Pacotes']:
                    if dependency_class in restrictions['Pacotes'][package_name]:
                        class_deps_packs.add(package_name)
                        dsm[package_name][class_package].append({'accessed_class': dependency_class, 'access_class': class_name, 'situation': ''})

            # Verifica as existências das restrições 'Pode' e 'Deve'
            have_can = 'Pode' in restrictions['LigacoesDePacotes'][class_package].keys()
            have_must = 'Deve' in restrictions['LigacoesDePacotes'][class_package].keys()
            package_restrictions = set()
            if have_can and have_must:
                package_restrictions = set(restrictions['LigacoesDePacotes'][class_package]['Pode']) | set(restrictions['LigacoesDePacotes'][class_package]['Deve'])
            elif have_can:
                package_restrictions = set(restrictions['LigacoesDePacotes'][class_package]['Pode'])
            elif have_must:
                package_restrictions = set(restrictions['LigacoesDePacotes'][class_package]['Deve'])

            # Verifica se há restrições de acesso impróprio ou alguma ausência de acesso para poder classificar corretamente
            if len(package_restrictions.symmetric_difference(class_deps_packs)) > 0:
                improper_access = class_deps_packs - package_restrictions
                appropriate_access = class_deps_packs & package_restrictions
                if len(improper_access) > 0:
                    for improper_access_pack in improper_access:
                        for access in dsm[improper_access_pack][class_package]:
                            if access['access_class'] == class_name:
                                access['situation'] = 'D'

                absence_access = package_restrictions - class_deps_packs
                for absence_access_pack in absence_access:
                    if have_must and absence_access_pack in restrictions['LigacoesDePacotes'][class_package]['Deve']:
                        dsm[absence_access_pack][class_package].append({'accessed_class': 'A', 'access_class': class_name, 'situation': 'A'})
                    if have_can and absence_access_pack in restrictions['LigacoesDePacotes'][class_package]['Pode']:
                        dsm[absence_access_pack][class_package].append({'accessed_class': '?', 'access_class': class_name, 'situation': '?'})

                for appropriate_access_pack in appropriate_access:
                    for access in dsm[appropriate_access_pack][class_package]:
                        if access['access_class'] == class_name:
                            access['situation'] = 'C'


            else:
                for package_restriction in package_restrictions:
                    for access in dsm[package_restriction][class_package]:
                        if access['access_class'] == class_name:
                            access['situation'] = 'C'


        data_text = "***************** // DSM Final // *****************\n"
        print()
        print('***************** // DSM Final // *****************')
        for package_name in dsm:
            for access_package in dsm[package_name]:
                if len(dsm[package_name][access_package]) > 0:
                    print(package_name + '-' + access_package + ':')
                    data_text += package_name + '-' + access_package + ':'
                    for access in dsm[package_name][access_package]:
                        print('\t', access)
                        data_text += ('\t' + str(access))
            print()


        print()

        dictionary_data = load_obj_to_file("/files/json_files/" + sys.argv[3])
        classes_dependences = []
        classes_names = []
        package_classes = []
        for elem_dict in dictionary_data:
            dep_intern = []
            dep_intern.append(elem_dict['type'])
            dep_intern.append(elem_dict['imports'])
            dep_intern.append(elem_dict['annotation'])
            dep_intern.append(elem_dict['method_names'])
            dep_intern.append(elem_dict['invocation'])
            dep_intern.append(elem_dict['structure'])

            classes_names.append(elem_dict['name_obj'])
            package_classes.append(elem_dict['package'])

            classes_dependences.append(dep_intern)
    
        for x in classes_dependences:
            print(x)
        print(set(package_classes))

        for package_name in dsm:
            for access_package in dsm[package_name]:
                if len(dsm[package_name][access_package]) > 0:
                    for access in dsm[package_name][access_package]:
                        if access['situation'] == 'D':
                            access_class_dep = find_class_deps(access['access_class'], classes_dependences, classes_names)
                            
                            nearest_neighbors = get_nearest_neighbors(np.array(classes_dependences,dtype=list), np.array(package_classes,dtype=list), access_class_dep, classes_names, k = 3)
                            y = classify(nearest_neighbors, set(package_classes))

                            if package_name != y:
                                print("Recomenda-se mover esta classe para o pacote:", y)

                            # sys.exit()



        # Generated_rules_file.rules(tuple_lig_uni, dict_rules, data_text)


    except OSError:
        print('Algum erro aconteceu')
