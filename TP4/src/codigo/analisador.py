#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

"""
Este programa indica erros de Template Method no projeto

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
from g4_python.Python3Lexer import Python3Lexer
from g4_python.Python3Parser import Python3Parser
from g4_python.Python3Listener import Python3Listener


# Variáveis globais:
classes_data = {}
classes_name = []
class_instance = {}


def walks(tree, goal_rule):
    if not isinstance(tree, TerminalNode):
        if Python3Parser.ruleNames[tree.getRuleIndex()] == goal_rule:
            return tree
        else:
            for child in tree.getChildren():
                tree = walks(child, goal_rule)
                if tree:
                    return tree


class ClassListener(Python3Listener):
    def enterClassdef(self, ctx):
        classes_name.append(ctx.getChild(1).getText())


class RuleListener(Python3Listener):
    def enterEveryRule(self, ctx):
        """ enterEveryRule: este método faz a coleta de dados essênciais para a indicação de refatoração:
            * Nome da Classes
                * Nome dos atributos (instanciados e da classe)
                * Nome dos métodos
                * Nome dos parâmetros dos métodos

            entrada: ctx: São as regras da gramática, geradas por meio do árvore do Parse.
        """

        if isinstance(ctx, Python3Parser.ClassdefContext):
            class_name = ctx.getChild(1).getText()
            classes_data[class_name] = {}
            instance_attributes = {}

            suite_tree = walks(ctx, 'suite')

            for suite_child in suite_tree.getChildren():
                funcdef_tree = walks(suite_child, 'funcdef')

                if funcdef_tree:
                    method_name = funcdef_tree.getChild(1).getText()

                    suite_func_tree = walks(funcdef_tree, 'suite')

                    for suite_func_child in suite_func_tree.getChildren():
                        if isinstance(suite_func_child, Python3Parser.StmtContext):
                            tempNameAtrr = suite_func_child.getChild(0).getText().split('=')[0].replace("\n", '')
                            line_func = suite_func_child.getChild(0).getText()
                            for name in classes_name:
                                tuple_temp = sub_contains_key(instance_attributes, line_func)
                                if (name + '(' in line_func) or tuple_temp[0]:
                                    tempNameAtrr = tuple_temp[1] if tuple_temp[0] == True else tempNameAtrr
                                    class_instance[tempNameAtrr] = name
                                    if instance_attributes.get(tempNameAtrr) == None:
                                        instance_attributes[tempNameAtrr] = []
                                    if not instance_attributes[tempNameAtrr].__contains__(method_name.replace(" ", "")):
                                        instance_attributes[tempNameAtrr].append(method_name.replace(" ", ""))

                        classes_data[class_name]["instance_attribute"] = instance_attributes


class MethodsListener(ParseTreeListener):
    def enterEveryRule(self, ctx):
        """ enterEveryRule (MethodsListener):
            este método faz a análise em cada método utilizando os dados obtidos do último uso da árvore de sintaxe.

            entrada: ctx: São as regras da gramática, geradas por meio do árvore do Parse.
        """

        if isinstance(ctx, Python3Parser.ClassdefContext):
            class_name = ctx.getChild(1).getText()
            suite_tree = walks(ctx, 'suite')

            for suite_child in suite_tree.getChildren():
                funcdef_tree = walks(suite_child, 'funcdef')

                if funcdef_tree:
                    method_name = funcdef_tree.getChild(1).getText()

                    if method_name != '__init__':
                        print("Method Name: ", method_name)
                        suite_func_tree = walks(funcdef_tree, 'suite')

                        lines_method = suite_func_tree.getChildCount()-3
                        print("Linhas do método: {} ".format(str(lines_method)))

                        line_cont = 1
                        for instance_key in classes_data[class_name]["instance_attribute"]:
                            method_name_list = []
                            for method_name in classes_data[class_name]["instance_attribute"][instance_key]:
                                if method_name != '__init__':
                                    method_name_list.append(method_name)

                            count_ocr = 0
                            instance_key_out = None
                            if len(method_name_list) == 1 and method_name == method_name_list[0]:
                                for child_suite_func_tree in suite_func_tree.getChildren():
                                    if (not child_suite_func_tree.getText().isspace()):
                                        if instance_key in child_suite_func_tree.getText():
                                            print('Nome do método que usa a instância', "'" + instance_key + "'", 'na linha', str(line_cont) + ':', method_name_list[0])
                                            print('Linha:', child_suite_func_tree.getText())
                                            count_ocr += 1
                                            instance_key_out = instance_key
                                            print("instance_key: ", instance_key)
                                        line_cont += 1

                                if instance_key_out != None and (len(classes_data[class_name]["instance_attribute"][instance_key_out]) > 1):
                                    print("O método: {} é cadidato para Move Method por conta do atributo {}, com Porcentagem de {}% para classe {}".format(
                                        str(method_name),
                                        str(instance_key_out),
                                        str(count_ocr/lines_method*100),
                                        str(class_instance[instance_key_out])
                                    ))
                                    instance_key_out = None


def sub_contains_key(dict_word, string_word):
    for key in dict_word:
        if key in string_word:
            return (True, key)
    return (False, "")


def run(Listener):
    for path in files_path:
        input = FileStream(path, "UTF-8")
        lexer = Python3Lexer(input)
        stream = CommonTokenStream(lexer)

        stream.fill()

        parser = Python3Parser(stream)
        tree = parser.file_input()
        listener = Listener()
        walker = ParseTreeWalker()
        walker.walk(listener, tree)


if __name__ == '__main__':
    directory = os.path.join(os.getcwd(), sys.argv[1])

    files_name = []
    files_path = []

    for root, dirs, files in os.walk(directory):
        for name in files:
            if name.endswith(".py"):
                files_name.append(name)
                file_path = os.path.join(root, name)
                files_path.append(file_path)

    print('Nome dos arquivos:\n', files_name, '\n')

    try:
        run(ClassListener)
        # run(RuleListener)
        # run(MethodsListener)

    except OSError:
        print('Algum erro aconteceu')
