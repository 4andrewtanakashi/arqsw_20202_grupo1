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
matrix_inherit = {}
abstract_class_methods = {}
template_class = ''

def traverse(tree, indent = 0):
    if tree.getText() == "<EOF>":
        return
    elif isinstance(tree, TerminalNode):
        print("{0}TOKEN='{1}'".format("  " * indent, tree.getText()))
    else:
        print("{0}{1}".format("  " * indent, Python3Parser.ruleNames[tree.getRuleIndex()]))
        for child in tree.children:
            traverse(child, indent + 1)


def check_method_call(tree, token):
    if tree.getText() == "<EOF>":
        return
    elif isinstance(tree, TerminalNode):
        if tree.getText() == token and tree.getParent().getChild(0).getText() == '.':
            return True
    else:
        for child in tree.children:
            check_method_call(child, token)


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
            #traverse(ctx)

            abstract_class_methods['abstract'] = []
            abstract_class_methods['concrete'] = []

            class_name = ctx.getChild(1).getText()
            
            class_arglist_tree = walks(ctx, 'arglist')

            matrix_inherit[class_name] = []

            if class_arglist_tree:
                for arglist_child in class_arglist_tree.getChildren():
                    if isinstance(arglist_child, Python3Parser.ArgumentContext):
                        for i in range(arglist_child.getChildCount()):
                            if arglist_child.getChild(i).getText() == 'metaclass' and arglist_child.getChild(i+1).getText() == '=' and arglist_child.getChild(i+2).getText() == 'ABCMeta':
                                template_class = class_name
                                print('Classe template é:', class_name, 'com o argumento', arglist_child.getText())

                print('Arglist ->', arglist_child.getText())
                #matrix_inherit[class_name].append(argument_child.getText())

            if template_class == class_name:
                suite_tree = walks(ctx, 'suite')
                
                for suite_child in suite_tree.getChildren():
                    decorated_tree = walks(suite_child, 'decorated')
                    
                    if decorated_tree:                       
                        decorator_tree = walks(decorated_tree, 'decorator')

                        if decorator_tree and decorator_tree.getChild(1).getText() == 'abstractmethod':
                            funcdef_tree = walks(suite_child, 'funcdef')

                            if funcdef_tree:
                                print('Funcao com decorator ->\n', funcdef_tree.getText())
                                abstract_class_methods['abstract'].append(funcdef_tree.getChild(1).getText())

                        print('Filho suite ->\n', suite_child.getText())

                    else:
                       funcdef_tree = walks(suite_child, 'funcdef')
                       if funcdef_tree and funcdef_tree.getChild(1).getText() != '__init__':
                           print('Funcao sem decorator ->\n', funcdef_tree.getText())
                           abstract_class_methods['concrete'].append(funcdef_tree.getChild(1).getText())

                print('Metodos classe abstrata:', abstract_class_methods)

                for method in abstract_class_methods['concrete']:
                    if check_template_method(method, suite_tree):
                        print('Existe um método template:', method, 'da classe:', class_name)


def check_template_method(method, suite_tree):
    for suite_child in suite_tree.getChildren():
        funcdef_tree = walks(suite_child, 'funcdef')

        if funcdef_tree:
            func_name = funcdef_tree.getChild(1).getText()
            
            if func_name == method:
                for abstract_class_method in [*list(abstract_class_methods.values())[0], *list(abstract_class_methods.values())[1]]:       
                    if abstract_class_method != method:
                        if check_method_call(funcdef_tree, abstract_class_method) == False:
                            return False
                        else:
                            print('O método', method, 'possui chamada ao método:', abstract_class_method)

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
        run(RuleListener)
        
        print('\nMatriz de herança:', matrix_inherit)
        
        abstract_class_childs = []
        for class_name in matrix_inherit:
            for parent_class in matrix_inherit[class_name]:
                if parent_class == template_class:
                    abstract_class_childs.append(class_name)
                    
        print('\nClasses filhas da classe abstrata', abstract_class_childs)
                

    except OSError:
        print('Algum erro aconteceu')
