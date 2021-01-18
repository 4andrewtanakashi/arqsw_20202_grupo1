#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

"""
Este programa indica erros no padrão arquitetural MTV no projeto

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
template_exist = False


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


class RuleListener(Python3Listener):
    def enterEveryRule(self, ctx):
        """ enterEveryRule: este método faz a coleta de dados faz verificações de erros da classe abstrata.
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

        if isinstance(ctx, Python3Parser.Dotted_nameContext):
            if ctx.getChild(2) and (ctx.getChild(2).getText() == 'views' or ctx.getChild(2).getText() == 'http'):
                if isinstance(ctx.parentCtx, Python3Parser.Import_fromContext):
                    for ctx_child in ctx.parentCtx.getChildren():
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

def resultado_analise():
    """
        resultado_analise: este método exibe se há erros ou avisos.
    """

    view_exist = False
    model_exist = False

    for file_path in files_dict:
        print('\n', file_path)
        print('  ', 'Importação viewers:', files_dict[file_path]['django_viewer_imports'])
        print('  ', 'Classes viewers:', files_dict[file_path]['parents_viewer_classes'])
        print('  ', 'Funções viewers:', files_dict[file_path]['file_viewer_functions'])
        print('  ', 'Importação models:', files_dict[file_path]['django_model_imports'])
        print('  ', 'Classes models:', files_dict[file_path]['parents_model_classes'])

        if (len(files_dict[file_path]['django_viewer_imports']) > 0):
            notEmpty = False
            elem_dict = files_dict[file_path]['parents_viewer_classes']
            for classe in elem_dict:
                if (len(elem_dict[classe]) > 0):
                    notEmpty = True

            elem_dict = files_dict[file_path]['file_viewer_functions']

            for function in elem_dict:
                if (len(elem_dict[function]) > 0):
                    notEmpty = True


            if (not notEmpty):
                print("[WARNING] Importação de view sem uso {}".format(str(files_dict[file_path]['django_viewer_imports'])))
                print("[ERROR] Não há acesso a templates neste arquivo view")
            else:
                if (len(files_dict[file_path]['django_model_imports']) > 0):
                    if (len(files_dict[file_path]['parents_model_classes']) > 0):
                        for key_classe_model in files_dict[file_path]['parents_model_classes']:
                            for elem_list in files_dict[file_path]['django_model_imports']:
                                if (files_dict[file_path]['parents_model_classes'][key_classe_model].__contains__(elem_list)):
                                    print("[WARNING] Implementações de model no mesmo arquivo de views, recomenda-se separar para outro arquivo")
                else:
                    print("[ERROR] Não há importação de modelos no arquivo de view. É obrigatório o uso de pelo menos um modelo")
            view_exist = True

        if (len(files_dict[file_path]['django_model_imports']) > 0):
            model_exist = True

    if (template_exist) and (not model_exist) and (not view_exist):
        print("[ERROR] Violação de padrão arquitetural (MTV) não há model e view no projeto")
    elif (model_exist) and (not template_exist) and (not view_exist):
        print("[ERROR] Violação de padrão arquitetural (MTV) não há template e view no projeto")
    elif (view_exist) and (not model_exist) and (not template_exist):
        print("[ERROR] Violação de padrão arquitetural (MTV) não há template e model no projeto")
    elif (not view_exist) and (not model_exist) and (not template_exist):
        print("[ERROR] Não está padrão arquitetural MTV (sem Model, Template e View)")
    else:
        if (not model_exist):
            print("[ERROR] Violação de padrão arquitetural (MTV) não há model no projeto")
        elif (not view_exist):
            print("[ERROR] Violação de padrão arquitetural (MTV) não há view no projeto")
        elif (not template_exist):
            print("[ERROR] Violação de padrão arquitetural (MTV) não há template no projeto")


if __name__ == '__main__':
    global current_path
    directory = os.path.join(os.getcwd(), sys.argv[1])

    files_name = []
    files_path = []

    dict_templates = {}

    for root, dirs, files in os.walk(directory):
        for name in files:
            if name.endswith(".py"):
                files_name.append(name)
                file_path = os.path.join(root, name)
                files_path.append(file_path)
            if name.endswith(".html"):
                file_path = os.path.join(root, "")
                aux = file_path.split("/")
                if not aux[len(aux)-2] in dict_templates.keys(): #Colhendo apenas o diretório correspondente
                    dict_templates[aux[len(aux)-2]] = True
                if dict_templates[aux[len(aux)-2]]:
                    for file in os.listdir(file_path):
                        if not file.endswith(".html"):
                            print("[WARNING] Arquivo não é de template {}, recomenda-se movê-lo para outro diretório".format(str(file)))
                    dict_templates[aux[len(aux)-2]] = False
                template_exist = True



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

        resultado_analise()

    except OSError:
        print('Algum erro aconteceu')
