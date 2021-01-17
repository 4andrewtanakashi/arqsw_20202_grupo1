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


files_dict = {}


def check_token(tree, token):
    """ check_method_call: este método percorre os nodos para saber se existe o token na derivação

        entrada:
            tree: Árvore de derivação do nodo.
            token: token esperado.
    """
    if tree.getText() == "<EOF>":
        return False
    elif isinstance(tree, TerminalNode):
        if tree.getText() == token and tree.getParent().getChild(0).getText() == '.':
            return True
    else:
        for child in tree.children:
            log_tmp = check_token(child, token)
            if log_tmp == True:
                return True
            elif log_tmp == False:
                return False


def walks(tree, goal_rule):
    """ walks: este método percorre a AST para chegar em uma determinada regra.

        entrada:
            tree: Árvore de derivação do nodo.
            goal_rule: regra de chegada.
    """
    if not isinstance(tree, TerminalNode):
        if Python3Parser.ruleNames[tree.getRuleIndex()] == goal_rule:
            return tree
        else:
            for child in tree.getChildren():
                tree = walks(child, goal_rule)
                if tree:
                    return tree


def traverse(tree, indent = 0):
    if tree.getText() == "<EOF>":
        return
    elif isinstance(tree, TerminalNode):
        print("{0}TOKEN='{1}'".format("  " * indent, tree.getText()))
    else:
        print("{0}{1}".format("  " * indent, Python3Parser.ruleNames[tree.getRuleIndex()]))
        for child in tree.children:
            traverse(child, indent + 1)


class RuleListener(Python3Listener):
    def enterEveryRule(self, ctx):
        """ enterEveryRule: este método faz a coleta de dados w faz verificações de erros da classe abstrata.
            * Nome da Classes
                * Nome dos atributos (instanciados e da classe)
                * Nome dos métodos
                * Nome dos parâmetros dos métodos

            entrada: ctx: São as regras da gramática, geradas por meio do árvore do Parse.
        """

        if isinstance(ctx, Python3Parser.Import_fromContext):
            dotted_name_tree = walks(ctx, 'dotted_name')
            if isinstance(dotted_name_tree, Python3Parser.Dotted_nameContext):
                last_child_dotted = dotted_name_tree.getChild(dotted_name_tree.getChildCount()-1).getText()
                import_as_names_tree = walks(ctx, 'import_as_names')
                if last_child_dotted == 'models':
                    if isinstance(import_as_names_tree, Python3Parser.Import_as_namesContext):
                        for import_as_name in import_as_names_tree.getChildren():
                            if import_as_name.getText() != ',':
                                files_dict[current_path]['django_model_imports'].append(import_as_name.getText())
                elif ctx.getChild(ctx.getChildCount()-1).getText() == 'models':
                    files_dict[current_path]['django_model_imports'].append(ctx.getChild(ctx.getChildCount()-1).getText())

        # traverse(ctx)
        if isinstance(ctx, Python3Parser.Dotted_nameContext):
            #print(ctx.getText());
            if ctx.getChild(2) and (ctx.getChild(2).getText() == 'views' or ctx.getChild(2).getText() == 'http'):
                #print(ctx.parentCtx.getText());
                if isinstance(ctx.parentCtx, Python3Parser.Import_fromContext):
                    for ctx_child in ctx.parentCtx.getChildren():
                        #print(ctx_child.getText())
                        if isinstance(ctx_child, Python3Parser.Import_as_namesContext):
                            for import_as_name in ctx_child.getChildren():
                                if import_as_name.getText() != ',':
                                    files_dict[current_path]['django_viewer_imports'].append(import_as_name.getText())

        if isinstance(ctx, Python3Parser.ClassdefContext):
            class_name = ctx.getChild(1).getText()
            files_dict[current_path]['parents_viewer_classes'][class_name] = []
            files_dict[current_path]['parents_model_classes'][class_name] = []

            for class_child in ctx.getChildren():
                if isinstance(class_child, Python3Parser.ArglistContext):
                    for arglist_child in class_child.getChildren():
                        if isinstance(arglist_child, Python3Parser.ArgumentContext):
                            for i in range(arglist_child.getChildCount()):
                                arg = arglist_child.getChild(i).getText()

                                if arg in files_dict[current_path]['django_viewer_imports']:
                                    files_dict[current_path]['parents_viewer_classes'][class_name].append(arglist_child.getText())
                                elif arg in files_dict[current_path]['django_model_imports']:
                                    files_dict[current_path]['parents_model_classes'][class_name].append(arglist_child.getText())
                                else:
                                    atom_tree = walks(arglist_child, 'atom')
                                    if isinstance(atom_tree, Python3Parser.AtomContext) and (atom_tree.getText() == 'models'):
                                        files_dict[current_path]['parents_model_classes'][class_name].append(atom_tree.getText())

        if isinstance(ctx, Python3Parser.FuncdefContext):
            if not isinstance(ctx.parentCtx.parentCtx.parentCtx, Python3Parser.SuiteContext):
                function_name = ctx.getChild(1).getText()
                files_dict[current_path]['file_viewer_functions'][function_name] = []
                return_stmt_tree = walks(ctx, 'return_stmt')

                if isinstance(return_stmt_tree, Python3Parser.Return_stmtContext):
                    for return_stmt_child in return_stmt_tree.getChildren():
                        if isinstance(return_stmt_child, Python3Parser.TestlistContext):
                            for test_list_child in return_stmt_child.getChildren():
                                atom_expr_tree = walks(test_list_child, 'atom_expr')

                                if isinstance(atom_expr_tree, Python3Parser.Atom_exprContext):
                                    atom_token = atom_expr_tree.getChild(0).getText()

                                    if atom_token in files_dict[current_path]['django_viewer_imports'] or atom_token == 'render' or atom_token == 'redirect':
                                        files_dict[current_path]['file_viewer_functions'][function_name] = atom_expr_tree.getChild(0).getText()

if __name__ == '__main__':
    global current_path
    directory = os.path.join(os.getcwd(), sys.argv[1])

    files_name = []
    files_path = []

    for root, dirs, files in os.walk(directory):
        for name in files:
            if name.endswith(".py"):
                files_name.append(name)
                file_path = os.path.join(root, name)
                files_path.append(file_path)

    # path = 'examples/example_test2/core/views.py'
    print('Nome dos arquivos:\n', files_name, '\n')

    try:
        for path in files_path:
            current_path = path
            files_dict[current_path] = {}
            files_dict[current_path]['django_viewer_imports'] = []
            files_dict[current_path]['parents_viewer_classes'] = {}
            files_dict[current_path]['file_viewer_functions'] = {}
            files_dict[current_path]['django_model_imports'] = []
            files_dict[current_path]['parents_model_classes'] = {}

            input = FileStream(path, "UTF-8")
            lexer = Python3Lexer(input)
            stream = CommonTokenStream(lexer)

            stream.fill()

            parser = Python3Parser(stream)
            tree = parser.file_input()
            listener = RuleListener()
            walker = ParseTreeWalker()
            walker.walk(listener, tree)

        for file_path in files_dict:
            print('\n', file_path)
            print('  ', 'Importação viewers:', files_dict[file_path]['django_viewer_imports'])
            print('  ', 'Classes viewers:', files_dict[file_path]['parents_viewer_classes'])
            print('  ', 'Funções viewers:', files_dict[file_path]['file_viewer_functions'])
            print('  ', 'Importação models:', files_dict[file_path]['django_model_imports'])
            print('  ', 'Classes models:', files_dict[file_path]['parents_model_classes'])

    except OSError:
        print('Algum erro aconteceu')
