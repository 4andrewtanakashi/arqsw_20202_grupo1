#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

"""
Este programa clusteriza arquivos de projeto Spring Boot

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
from util.utils import save_obj_to_file, attributes_from_project
from util.clusterization import *
from util.Grafo import *


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
        #
        #     input = FileStream(path, "UTF-8")
        #     lexer = Java8Lexer(input)
        #     stream = CommonTokenStream(lexer)
        #
        #     stream.fill()
        #
        #     print("current_path: {}".format(str(current_path)))
        #     parser = Java8Parser(stream)
        #     tree = parser.compilationUnit()
        #     listener = Java8ParserListener()
        #     walker = ParseTreeWalker()
        #     walker.walk(listener, tree)
        #     externalLista.append(listener.dicionario)
        #
        #
        # for i in range(len(files_name)):
        #     externalLista[i]["file_name"] = files_name[i]
        #
        # attributes_from_project(externalLista)
        # save_obj_to_file(externalLista, "data.json")

        clusters = clusterization('data.json')

        for cluster in clusters:
            print(cluster + ':')
            for class_name in clusters[cluster]:
                print('\t' + class_name)
            print()

        g = Grafo("data.json")
        print()
        print(g.pseudo_adjacent_matrix)
        print()

        dep_clusters = set()
        new_names_clusters = {}
        views_mvc_dep = []
        for pivo_cluster in clusters:
            classes_to_remove = []
            for class_name in clusters[pivo_cluster]:
                class_deps = g.pseudo_adjacent_matrix[class_name.split('.')[0]]
                if len(class_deps) > 0:
                    print(class_name.split('.')[0], '\t', class_deps)
                    for dep_name in class_deps:
                        for cluster in clusters:
                            if dep_name + '.java' in clusters[cluster]:
                                dep_clusters.add(cluster)

                    print('Aqui:', class_name.split('.')[0])
                    print('Dep_clusters:', dep_clusters)
                    not_dep_clusters = set(clusters_names) - dep_clusters
                    print('Not_dep_clusters:', not_dep_clusters)
                    if len(not_dep_clusters) == 1 and list(not_dep_clusters)[0] != pivo_cluster:
                        clusters[list(not_dep_clusters)[0]].append(class_name)
                        classes_to_remove.append(class_name)

                        if 'Controller' not in new_names_clusters.values():
                            new_names_clusters[list(not_dep_clusters)[0]] = 'Presenter'

                        for pivo_dep_name in class_deps:
                            for dep_name in class_deps:
                                if pivo_dep_name != dep_name:
                                    if dep_name in g.pseudo_adjacent_matrix[pivo_dep_name]:
                                         views_mvc_dep.append(dep_name)

                    # else:

                    print()

            for class_name in classes_to_remove:
                for pivo_class_name in clusters[pivo_cluster]:
                    if class_name == pivo_class_name:
                        clusters[pivo_cluster].remove(class_name)

        print()
        for cluster in clusters:
            print(cluster + ':')
            for class_name in clusters[cluster]:
                print('\t' + class_name)
            print()

        print(new_names_clusters)
        print()
        print(views_mvc_dep)

    except OSError:
        print('Algum erro aconteceu')
