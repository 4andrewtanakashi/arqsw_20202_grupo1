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
import random

from antlr4 import *
from g4_java8_python.Java8Lexer import Java8Lexer
from g4_java8_python.Java8Parser import Java8Parser
from g4_java8_python.Java8ParserListener import Java8ParserListener
from antlr4.tree.Trees import *
from util.utils import load_obj_to_file, attributes_from_project, generated_rules_unique
from util.Generated_rules_file import *
from util.Grafo import *

import numpy as np
from mayavi import mlab


def scale_calc(x, x_max, x_min, delta=0.1):
    normal_x = (x - x_min) / (x_max - x_min)
    result = normal_x * (1 - 2 * delta) + delta
    return result

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
        # externalLista = []
        # for path in files_path:
        #     current_path = path

        #     input = FileStream(path, "UTF-8")
        #     lexer = Java8Lexer(input)
        #     stream = CommonTokenStream(lexer)

        #     stream.fill()

        #     print("current_path: {}".format(str(current_path)))
        #     parser = Java8Parser(stream)
        #     tree = parser.compilationUnit()
        #     listener = Java8ParserListener()
        #     walker = ParseTreeWalker()
        #     walker.walk(listener, tree)
        #     externalLista.append(listener.dicionario)

        # for i in range(len(files_name)):
        #     externalLista[i]["file_name"] = files_name[i]

        # attributes_from_project(externalLista)
        # save_obj_to_file(externalLista, "/files/json_files/" + sys.argv[3])

        # Gera um grafo contendo os acessos de cada classe do projeto de entrada
        # g = Grafo("/files/json_files/" + sys.argv[2])
        g = Grafo("/files/json_files/data_mvc.json")
        for class_name in g.pseudo_adjacent_matrix:
            print(class_name + ':', g.pseudo_adjacent_matrix[class_name])

        dictionary_data = load_obj_to_file("/files/json_files/data_mvc.json")

        class_list = []
        files_names = []
        quant_classes = len(dictionary_data)

        for elem_dict in dictionary_data:
            list_internal_X = []
            list_internal_X.append(elem_dict['name_obj'])
            list_internal_X.append(elem_dict['structure'])

            class_list.append(list_internal_X)

            files_names.append(elem_dict['file_name'])

        for line in class_list:
            print(line)

        dict_packages = {'Model': [], 'Controller': [], 'View': []}
        dict_packages['Model'] = class_list[:4]
        dict_packages['Controller'] = class_list[4:11]
        dict_packages['View'] = class_list[11:]

        print()
        for pack in dict_packages:
            print(dict_packages[pack])
            print()

        methods_quant = []
        for pack in dict_packages:
            for class_name in dict_packages[pack]:
                methods_quant.append(class_name[1]['count_attributes'])

        max_methods = np.asarray(methods_quant).max()
        min_methods = np.asarray(methods_quant).min()

        extern_counter = 0
        for pack in dict_packages:
            intern_counter = 0
            pack_color = (random.uniform(0.1, 0.7), random.uniform(0.1, 0.7), random.uniform(0.1, 0.7))

            for class_name in dict_packages[pack]:
                lateral_scale = scale_calc(class_name[1]['count_attributes'], max_methods, min_methods)
                mlab.barchart([intern_counter], [extern_counter], [0], [class_name[1]['count_methods']], lateral_scale=lateral_scale, color=pack_color, opacity=0.5)
                mlab.text3d(intern_counter, extern_counter, 0, text=class_name[0], scale=0.15)
                mlab.text3d(intern_counter, extern_counter, class_name[1]['count_methods']+0.2, text="NOM: " + str(class_name[1]['count_methods']) + "\nNOA: " + str(class_name[1]['count_attributes']), scale=0.1)

                intern_counter += 1
            extern_counter += 2

        # b1 = mlab.barchart([0], [0], [0], [4], lateral_scale=0.9, name="Pessoa")
        # mlab.barchart([1], [0], [0], [1], lateral_scale=0.1, name="ProfessorView")
        # mlab.barchart([2], [0], [0], [3], lateral_scale=0.9, name="EscolaController")
        # mlab.barchart([3], [0], [0], [1], lateral_scale=0.1)
        # mlab.barchart([0], [1], [0], [1], lateral_scale=0.1)
        # mlab.barchart([1], [1], [0], [5], lateral_scale=0.9)
        # mlab.barchart([2], [1], [0], [2], lateral_scale=0.5)
        # mlab.barchart([3], [1], [0], [1], lateral_scale=0.1)
        # mlab.barchart([0], [2], [0], [4], lateral_scale=0.9)
        # mlab.barchart([1], [2], [0], [1], lateral_scale=0.1)
        # mlab.barchart([2], [2], [0], [4], lateral_scale=0.9)
        # mlab.barchart([3], [2], [0], [1], lateral_scale=0.1)
        # mlab.barchart([0], [3], [0], [2], lateral_scale=0.5)
        # mlab.barchart([1], [3], [0], [5], lateral_scale=0.9)
        # mlab.barchart([2], [3], [0], [2], lateral_scale=0.5)
        # mlab.barchart([3], [3], [0], [4], lateral_scale=0.9)
        # # mlab.savefig("show.png")
        mlab.show()

    # Generated_rules_file.rules(tuple_lig_uni, dict_rules, data_text)

    except OSError:
        print('Algum erro aconteceu')
