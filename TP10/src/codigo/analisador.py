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
<<<<<<< HEAD
from util.utils import save_obj_to_file, attributes_from_project
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
=======
from util.utils import load_obj_to_file, generated_rules_unique
from util.clusterization import *
from util.Generated_rules_file import *


if __name__ == '__main__':
    dict_rules = load_obj_to_file(sys.argv[1])
    tuple_lig_uni = generated_rules_unique(dict_rules)
    Generated_rules_file.rules(tuple_lig_uni[0], tuple_lig_uni[1], dict_rules)

    # global current_path
    # directory = os.path.join(os.getcwd(), sys.argv[2])
    #
    # files_name = []
    # files_path = []
    #
    # dict_templates = {}
    #
    # for root, dirs, files in os.walk(directory):
    #     for name in files:
    #         if name.endswith(".java"):
    #             files_name.append(name)
    #             file_path = os.path.join(root, name)
    #             files_path.append(file_path)
    #
    # print('Nome dos arquivos:\n', files_name, '\n')

    # try:
>>>>>>> e508b2d622b62a7489b119b396eccd928f782b2a
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
        # save_obj_to_file(externalLista, "data_mvc2.json")


        # Gera um grafo contendo os acessos de cada classe do projeto de entrada
        g = Grafo("data_mvc.json")
        for class_name in g.pseudo_adjacent_matrix:
            print(class_name + ':', g.pseudo_adjacent_matrix[class_name])


        # Carrega a arquitetura ideal de um projeto por meio de um arquivo JSON
        restrictions = load_obj_to_file('arch_mvc2.json')


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


        print()
        print('***************** // DSM Final // *****************')
        for package_name in dsm:
            for access_package in dsm[package_name]:
                if len(dsm[package_name][access_package]) > 0:
                    print(package_name + '-' + access_package + ':')
                    for access in dsm[package_name][access_package]:
                        print('\t', access)
            print()


    except OSError:
        print('Algum erro aconteceu')
