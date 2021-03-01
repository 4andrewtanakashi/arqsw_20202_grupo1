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
from util.utils import load_obj_to_file, attributes_from_project, generated_rules_unique
from util.clusterization import *
from util.Generated_rules_file import *


if __name__ == '__main__':
    dict_rules = load_obj_to_file(sys.argv[1])
    tuple_lig_uni = generated_rules_unique(dict_rules)
    Generated_rules_file.rules(tuple_lig_uni, dict_rules)


    global current_path
    directory = os.path.join(os.getcwd(), sys.argv[2])

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
        save_obj_to_file(externalLista, "/files/json_files/" + sys.argv[3])

        g = Grafo("/files/json_files/" + sys.argv[3])


    except OSError:
        print('Algum erro aconteceu')
