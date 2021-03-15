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

from antlr4 import *
from g4_java8_python.Java8Lexer import Java8Lexer
from g4_java8_python.Java8Parser import Java8Parser
from g4_java8_python.Java8ParserListener import Java8ParserListener
from antlr4.tree.Trees import *
import numpy as np

from util.utils import load_obj_to_file, attributes_from_project, generated_rules_unique
from util.Generated_rules_file import *
from util.Grafo import *


class bcolors:
    HEADER = '\033[97m'
    DIVERGENCE = '\033[93m'
    ABSENSE = '\033[91m'
    CONVERGENCE = '\033[92m'
    WARNING = '\033[96m'
    TITLE = '\033[95m'
    ENDC = '\033[0m'


def find_class_deps(class_name, classes_dependences, classes_names):
    class_index = classes_names.index(class_name)
    class_deps = classes_dependences[class_index]
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


def get_nearest_neighbors(X_train, y_train, x, classes_names, k):
    distances = []
    for i in range(len(X_train)):
        if not (X_train[i] == np.array(x, dtype="object")).all():
            distances.append((calculate_similarity_Jaccard(X_train[i], x), y_train[i], classes_names[i]))

    nearest_neighbors = sorted(distances, reverse=True, key=lambda tup: tup[0])[:k]

    return list(zip(*nearest_neighbors))[1]


def classify(nearest_neighbors, classes):
    count_classes = []
    for class_id in range(len(classes)):
        count_classes.append((nearest_neighbors.count(class_id), list(classes)[class_id]))

    return max(count_classes)[1]


def load_deps(path, packages):
    dictionary_data = load_obj_to_file(path)
    classes_dependences = []
    classes_names = []
    classes_extends_implements = []
    for elem_dict in dictionary_data:
        dep_intern = []
        dep_intern.append(elem_dict['type'])
        dep_intern.append(elem_dict['imports'])
        dep_intern.append(elem_dict['annotation'])
        dep_intern.append(elem_dict['method_names'])
        dep_intern.append(elem_dict['invocation'])
        dep_intern.append(elem_dict['structure'])

        classes_names.append(elem_dict['name_obj'])
        classes_extends_implements.append({'extends': elem_dict['extends'], 'implements': elem_dict['implements']})

        classes_dependences.append(dep_intern)

    package_classes = []
    for class_name in classes_names:
        for package in packages:
            if class_name in packages[package]:
                package_classes.append(package)

    return package_classes, classes_names, classes_dependences, classes_extends_implements


def dsm(restrictions, classes_connections):
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


    # Imprime classificação das relações
    print(bcolors.TITLE + '***************** // Classificação das Relações // *****************' + bcolors.ENDC)
    for package_name in dsm:
        for access_package in dsm[package_name]:
            if len(dsm[package_name][access_package]) > 0:
                print('\n', bcolors.HEADER + access_package, '->', package_name + ':')
                for access in dsm[package_name][access_package]:
                    if access['situation'] == 'D':
                        print('\t' + bcolors.DIVERGENCE + access['access_class'], '->', access['accessed_class'] + bcolors.ENDC)
                    elif access['situation'] == 'A':
                        print('\t' + bcolors.ABSENSE + access['access_class'], '->', access['accessed_class'] + bcolors.ENDC)
                    elif access['situation'] == '?':
                        print('\t' + bcolors.WARNING + access['access_class'], '->', access['accessed_class'] + bcolors.ENDC)
                    else:
                        print('\t' + bcolors.CONVERGENCE + access['access_class'], '->', access['accessed_class'] + bcolors.ENDC)

    return dsm


if __name__ == '__main__':
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

        for i in range(len(files_name)):
            externalLista[i]["file_name"] = files_name[i]

        attributes_from_project(externalLista)
        save_obj_to_file(externalLista, "/files/json_files/deps/" + sys.argv[2])

        path_data_deps = "/files/json_files/deps/" + sys.argv[4]

        # Gera um grafo contendo os acessos de cada classe do projeto de entrada
        g = Grafo(path_data_deps)
        for class_name in g.pseudo_adjacent_matrix:
            print(class_name + ':', g.pseudo_adjacent_matrix[class_name])


        # Carrega a arquitetura ideal de um projeto por meio de um arquivo JSON
        restrictions = load_obj_to_file(sys.argv[3])


        # dsm = DSM(restrictions=restrictions, classes_connections=g.pseudo_adjacent_matrix)
        dsm = dsm(restrictions, g.pseudo_adjacent_matrix)


        # Carrega pacotes e dependências de todas as classes do projeto de entrada
        package_classes, classes_names, classes_dependences, classes_extends_implements = load_deps(path_data_deps, restrictions['Pacotes'])


        # Inicia lógica de recomendações de reparação arquitetural considerando cada tipo de violação
        for accessed_package in dsm:
            for access_package in dsm[accessed_package]:
                if len(dsm[accessed_package][access_package]) > 0:
                    for access in dsm[accessed_package][access_package]:
                        if access['situation'] == 'D':
                            access_class = access['access_class']
                            accessed_class = access['accessed_class']
                            access_class_deps = find_class_deps(access_class, classes_dependences, classes_names)
                            
                            # X Recomendação: Mover classe para pacote de maior similaridade
                            nearest_neighbors = get_nearest_neighbors(np.array(classes_dependences, dtype=list), np.array(package_classes, dtype=list), access_class_deps, classes_names, k = 3)
                            ideal_package = classify(nearest_neighbors, set(package_classes))
                            if access_package != ideal_package:
                                print("Recomenda-se mover a classe", access_class, "para o pacote:", ideal_package)

                            # X Recomendação: Substuição de classe pai em decorrer de violação de derivação
                            parent_accessed_class = classes_extends_implements[classes_names.index(accessed_class)]['extends']
                            if len(parent_accessed_class) > 0:
                                parent_class_index = classes_names.index(parent_accessed_class[0])
                                package_parent_class = package_classes[parent_class_index]

                                if package_parent_class != accessed_package:
                                    print("Recomenda-se substituir a classe acessada", accessed_class, "pela sua classe pai", parent_accessed_class[0], "que está no pacote", package_parent_class)


    except OSError:
        print('Algum erro aconteceu')
