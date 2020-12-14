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


matrix_inherit = {}
abstract_class_methods = {}
template_class = ''
concrete_method_dict = {}
classes_methods = {}


def check_method_call(tree, token):
    if tree.getText() == "<EOF>":
        return False
    elif isinstance(tree, TerminalNode):
        if tree.getText() == token and tree.getParent().getChild(0).getText() == '.':
            return True
    else:
        for child in tree.children:
            log_tmp = check_method_call(child, token)
            if log_tmp == True:
                return True
            elif log_tmp == False:
                return False


def walks(tree, goal_rule):
    if not isinstance(tree, TerminalNode):
        if Python3Parser.ruleNames[tree.getRuleIndex()] == goal_rule:
            return tree
        else:
            for child in tree.getChildren():
                tree = walks(child, goal_rule)
                if tree:
                    return tree


class RuleListener(Python3Listener):
    def enterEveryRule(self, ctx):
        global template_class

        if isinstance(ctx, Python3Parser.ClassdefContext):
            class_name = ctx.getChild(1).getText()

            matrix_inherit[class_name] = []

            # Pega o nome da classe abstrata (contém o método template) e armazena a herança de todas
            #   as classes
            for class_child in ctx.getChildren():
                if isinstance(class_child, Python3Parser.ArglistContext):
                    for arglist_child in class_child.getChildren():
                        if isinstance(arglist_child, Python3Parser.ArgumentContext):
                            for i in range(arglist_child.getChildCount()):
                                logic_large = arglist_child.getChild(i).getText() == 'metaclass' and arglist_child.getChild(i+1).getText() == '=' and arglist_child.getChild(i+2).getText() == 'ABCMeta'
                                if logic_large or arglist_child.getChild(i).getText().__contains__("ABC"):
                                    template_class = class_name

                            matrix_inherit[class_name].append(arglist_child.getText())


            # Armazena nome de todos métodos de cada classe
            classes_methods[class_name] = []
            suite_tree = walks(ctx, 'suite')
            for suite_child in suite_tree.getChildren():
                funcdef_tree = walks(suite_child, 'funcdef')
                
                if funcdef_tree:
                    method_name = funcdef_tree.getChild(1).getText()
                    classes_methods[class_name].append(method_name)


            # Armazena nome dos métodos abstratos e concretos da classe que possui o método template
            if template_class == class_name:
                suite_tree = walks(ctx, 'suite')

                for suite_child in suite_tree.getChildren():
                    decorated_tree = walks(suite_child, 'decorated')

                    if decorated_tree:
                        decorator_tree = walks(decorated_tree, 'decorator')

                        if decorator_tree and decorator_tree.getChild(1).getText() == 'abstractmethod':
                            funcdef_tree = walks(suite_child, 'funcdef')

                            if funcdef_tree:
                                abstract_class_methods['abstract'].append(funcdef_tree.getChild(1).getText())
                    else:
                       funcdef_tree = walks(suite_child, 'funcdef')
                       if funcdef_tree and funcdef_tree.getChild(1).getText() != '__init__':
                           abstract_class_methods['concrete'].append(funcdef_tree.getChild(1).getText())

                print('Metodos classe abstrata:', abstract_class_methods, '\n')


                # Verifica a existência de método template na classe abstrata
                list_template_method = []
                methods_list = [*list(abstract_class_methods.values())[0], *list(abstract_class_methods.values())[1]]
                for method in abstract_class_methods['concrete']:
                    if check_template_method(method, suite_tree, methods_list):
                        list_template_method.append(method)
                        print('Na classe:', class_name, 'existe o método template:', method)


                # Verifica se há erros como a existência de mais de um método template. Caso não exista nenhum
                #   método template, verifica se há métodos concretos que podem vir a ser
                if (len(list_template_method) > 1):
                    if len(list_template_method) > len(set(list_template_method)):
                        tmpStr = ""
                        for list_temp_met in list_template_method:
                            if list_template_method.count(list_temp_met) > 1 and tmpStr != list_temp_met:
                                print('[ERRO] Na classe:', class_name, 'há método template duplicado:', list_temp_met)
                                tmpStr = list_temp_met
                    else:
                        print('[ERRO] Na classe:', class_name, 'existe mais de um método template:', list_template_method)

                elif (len(list_template_method) < 1):
                    not_call_met = None
                    concrete_method = []
                    for concrete_method_child in concrete_method_dict:
                        not_call_met = set(methods_list) - set(concrete_method_dict[concrete_method_child])
                        not_call_met.discard(concrete_method_child)
                        concrete_method.append(concrete_method_child)
                    if not_call_met != None and len(list(not_call_met)) >= 1:
                        if len(concrete_method) > 1:
                            print('[ERRO] Na classe:', class_name, 'não existe método template, porém há métodos cadidatos que podem se tornar um:', concrete_method)
                        else:
                            print('[ERRO] Na classe:', class_name, 'não existe método template, porém o método:', concrete_method[0], 'é cadidato a ser um. Para isso, ele deve possuir chamada aos métodos:', not_call_met)
                    else:
                        print('[ERRO] Na classe:', class_name, 'não existe o método template e nem candidatos a se tornarem um')


def check_template_method(method, suite_tree, methods_list):
    for suite_child in suite_tree.getChildren():
        funcdef_tree = walks(suite_child, 'funcdef')

        if funcdef_tree:
            func_name = funcdef_tree.getChild(1).getText()

            count = 0
            if func_name == method:
                for abstract_class_method in methods_list:
                    if abstract_class_method != method:
                        logic_tmp_value = check_method_call(funcdef_tree, abstract_class_method)
                        if logic_tmp_value != None and logic_tmp_value == True:
                            if concrete_method_dict.get(method) == None:
                                concrete_method_dict[method] = []
                            concrete_method_dict[method].append(abstract_class_method)
                        else:
                            count += 1
                if (count > 0):
                    return False
    return True


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
        abstract_class_methods['abstract'] = []
        abstract_class_methods['concrete'] = []

        run(RuleListener)

        # Se uma classe abstrata existir, verifica se possui classes filhas e se elas implementam os métodos
        #   abstratos dela
        if template_class != '':
            abstract_class_children = []
            for class_name in matrix_inherit:
                for parent_class in matrix_inherit[class_name]:
                    if parent_class == template_class:
                        abstract_class_children.append(class_name)

            if len(abstract_class_children) > 1:
                print('\nClasses filhas: ', abstract_class_children, 'da classe abstrata:', template_class, '\n')
            else:
                print('\n[WARNING] A classe template method: ', template_class, 'não contém Hooks (classes filhas para o Design Patterns)\n')

            for class_name in classes_methods:
                if class_name in abstract_class_children:
                    difference_methods = list(set(abstract_class_methods['abstract']) - set(classes_methods[class_name]))
                    if len(difference_methods) > 0:
                        print('[ERRO] A classe filha', class_name, 'não implementa os seguintes métodos abstratos da classe', template_class + ':', difference_methods)

        else:
            print('[ERRO] Nenhuma classe abstrata foi encontrada, portanto não há template method')


    except OSError:
        print('Algum erro aconteceu')

