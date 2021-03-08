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
from util.circos import *
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
    directory = os.path.join(os.getcwd(), sys.argv[2])

    files_name = []
    files_path = []

    dict_templates = {}

    packages = {}
    for root, dirs, files in os.walk(directory):
        for pack in dirs:
            packages[pack] = []
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
        
        for elem_dict in externalLista:
            packages[elem_dict["package"]].append(elem_dict["name_obj"])
        
        print("packages: ", packages)
        
        attributes_from_project(externalLista)
        save_obj_to_file(externalLista, "/files/json_files/" + sys.argv[3])
        
        # Gera um grafo contendo os acessos de cada classe do projeto de entrada
        g = Grafo("/files/json_files/" + sys.argv[3])
        for class_name in g.pseudo_adjacent_matrix:
            print(class_name + ':', g.pseudo_adjacent_matrix[class_name])
        
        obj_json = {}
        obj_json["packages"] = packages
        obj_json["LigacoesDeClasses"] = g.pseudo_adjacent_matrix
        
        save_obj_to_file(obj_json, sys.argv[1])

        initialize_circos_plot(load_obj_to_file(sys.argv[1]))

        ### VisuArch
        # Carrega arquivo JSON com as dependências de um projeto
        dictionary_data = load_obj_to_file("/files/json_files/" + sys.argv[3])

        # Armazena os pacotes, suas classes e a quantidade de atributos e métodos de cada classe
        packages_dict = {}
        for elem_dict in dictionary_data:
            if elem_dict['package'] not in packages_dict.keys():
                packages_dict[elem_dict['package']] = []
            else:
                packages_dict[elem_dict['package']].append([elem_dict['name_obj'], elem_dict['structure']])

        methods_quant = []
        for pack in packages_dict:
            for class_name in packages_dict[pack]:
                methods_quant.append(class_name[1]['count_attributes'])

        max_methods = np.asarray(methods_quant).max()
        min_methods = np.asarray(methods_quant).min()

        extern_counter = 0
        for pack in packages_dict:
            intern_counter = 0
            pack_color = (random.uniform(0.1, 0.7), random.uniform(0.1, 0.7), random.uniform(0.1, 0.7))

            for class_name in packages_dict[pack]:
                lateral_scale = scale_calc(class_name[1]['count_attributes'], max_methods, min_methods)
                mlab.barchart([intern_counter], [extern_counter], [0], [class_name[1]['count_methods']], lateral_scale=lateral_scale, color=pack_color, opacity=0.5)
                mlab.text3d(intern_counter, extern_counter, 0, text=class_name[0], scale=0.15)
                mlab.text3d(intern_counter, extern_counter, class_name[1]['count_methods']+0.2, text="NOM: " + str(class_name[1]['count_methods']) + "\nNOA: " + str(class_name[1]['count_attributes']), scale=0.1)

                intern_counter += 1
            extern_counter += 2

        mlab.show()



    except OSError:
        print('Algum erro aconteceu')
