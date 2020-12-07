#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

"""
Este programa indica refatorações a serem feitas por meio do Move Methods

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
# from g4_python.Python3Visitor import Python3Visitor

"""
variáveis globais:
"""
classes_data = {}
count_pass = 0

#Variáveis para verificação:
attributes_instance = {}
imports_classes = []
conj = set()

def traverse(tree, indent = 0):
    """ traverse:

        entrada: tree:
                indent: 0
    """
    global conj
    if isinstance(tree, TerminalNode):
        pass
    elif isinstance(tree, Python3Parser.Import_as_nameContext):
        conj.add(tree.getText())
    elif isinstance(tree, Python3Parser.Dotted_as_nameContext):
        if tree.getText() != "import":
            for child_Dotted_as_nameContext in tree.getChildren():
                if isinstance(child_Dotted_as_nameContext, Python3Parser.Dotted_nameContext):
                    conj.add(tree.getChild(0).getText())
                else:
                    conj.add(tree.getChild(2).getText())
    else:
        #print('{0}{1}'.format('  ' * indent, Python3Parser.ruleNames[tree.getRuleIndex()]))
        for child in tree.children:
            traverse(child, indent + 1)

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
        """ enterEveryRule: este método faz a coleta de dados essênciais para a indicação de refatoração:
            * Nome da Classes
                * Nome dos atributos (instanciados e da classe)
                * Nome dos métodos
                * Nome dos parâmetros dos métodos

            entrada: ctx: São as regras da gramática, geradas por meio do árvore do Parse.
        """
        global matrix_inherit, attributes_instance, conj
        global classes_data, imports_classes

        if isinstance(ctx, Python3Parser.Import_stmtContext):
            traverse(ctx)
            
        
        if isinstance(ctx, Python3Parser.ClassdefContext):
            traverse(ctx)
            class_name = ctx.getChild(1).getText()
            classes_data[class_name] = {}
            attributes_by_class = []
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
                            #print("conj: {}".format(str(line_func )))
                            for elemConj in conj:
                                tuple_temp = sub_contains_key(instance_attributes, line_func)
                                if (elemConj in line_func) or tuple_temp[0]:
                                    tempNameAtrr = tuple_temp[1] if tuple_temp[0] == True else tempNameAtrr
                                    #Colocando na lista
                                    if instance_attributes.get(tempNameAtrr) == None:
                                        instance_attributes[tempNameAtrr] = []
                                    if not instance_attributes[tempNameAtrr].__contains__(method_name.replace(" ", "")):
                                        instance_attributes[tempNameAtrr].append(method_name.replace(" ", ""))

                        classes_data[class_name]["instance_attribute"] = instance_attributes
        

            print('Nome da classe:', class_name)
            print('Metodos da classe:', classes_data, '\n')


class MethodsListener(ParseTreeListener):
    def enterEveryRule(self, ctx):
        """ enterEveryRule (MethodsListener):
            este método faz a análise em cada método utilizando os dados obtidos do último uso da árvore de sintaxe.

            entrada: ctx: São as regras da gramática, geradas por meio do árvore do Parse.
        """
        global matrix_inherit
        global classes_data

        all_classes_use_methods = {}
        for classes in classes_data:
            all_classes_use_methods[classes] = 0

        if isinstance(ctx, Python3Parser.ClassdefContext):
            traverse(ctx)
            class_name = ctx.getChild(1).getText()
            print("Class Name: ", class_name)
            suite_tree = walks(ctx, 'suite')

            for suite_child in suite_tree.getChildren():
                funcdef_tree = walks(suite_child, 'funcdef')

                if funcdef_tree:
                    method_name = funcdef_tree.getChild(1).getText()

                    print("Method Name: ", method_name)
                    if method_name != '__init__':
                        suite_func_tree = walks(funcdef_tree, 'suite')

                        print("Linhas do método: {}, ".format(str(suite_func_tree.getChildCount()-3)))
                        print('Conteudo do método:\n', suite_func_tree.getText())
                        
                        line_cont = 1
                        for instance_key in classes_data[class_name]["instance_attribute"]:
                            method_name_list = []
                            for method_name in classes_data[class_name]["instance_attribute"][instance_key]:
                                if method_name != '__init__':
                                    method_name_list.append(method_name)

                            if len(method_name_list) == 1 and method_name == method_name_list[0]:
                                for child_suite_func_tree in suite_func_tree.getChildren():
                                    if (not child_suite_func_tree.getText().isspace()):                                        
                                    #if isinstance(child_suite_func_tree, Python3Parser.StmtContext):
                                        #Salva lista de atributos que métodos o utilizam
                                        #for instance_key in classes_data[class_name]["instance_attribute"]:
                                            #method_name_list = classes_data[class_name]["instance_attribute"][instance_key]
                                        if instance_key in child_suite_func_tree.getText():
                                            print('Nome do método que usa a instância', "'" + instance_key + "'", 'na linha', str(line_cont) + ':', method_name_list[0])
                                            print('Linha:', child_suite_func_tree.getText())
                                                
                                    #print(list((classes_data[class_name]["instance_attribute"])[i].keys()))
                                    #if list(classes_data[class_name]["instance_attribute"][i].keys())[0] in child_suite_func_tree.getChild(0).getText():
                                        #print('Krai ->', list(classes_data[class_name]["instance_attribute"][i].keys())[1])
                                        #if not list(classes_data[class_name]["instance_attribute"][i].keys())[1].__contains__(method_name):
                                            #print('Linha' get
                                        line_cont += 1
                                # Porcentagem de uso de classes no corpo do método:
                                # for


def sub_contains_key(dict_word, string_word):
    for key in dict_word:
        if key in string_word:
            return (True, key)
    return (False, "")


def run(ClassListener):
    for path in files_path:
        input = FileStream(path, "UTF-8") # É necessário colocar o segundo parametro para aceitar acentos
        lexer = Python3Lexer(input)
        stream = CommonTokenStream(lexer)

        stream.fill()

        parser = Python3Parser(stream)
        tree = parser.file_input()
        listener = ClassListener()
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
        run(MethodsListener)



    except OSError:
        print('Algum erro aconteceu')
