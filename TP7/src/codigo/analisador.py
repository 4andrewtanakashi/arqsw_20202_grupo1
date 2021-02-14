#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

"""
***

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
import ast
import astor
from copy import deepcopy, copy


classes_methods = {}


def walks(tree, block_list):
    if hasattr(tree, 'body'):
        block_list.append(tree.body)
        for child in tree.body:
            walks(child, block_list)


def subset(block, start, end):
    candidate = []
    if start == end:
        candidate.append(block[start])
    else:
        for i in range(start, end+1):
            candidate.append(block[i])
    return candidate


def isValid(block, candidate):
    if len(candidate) == 1:
        return False
    for stmt in candidate:
        if isinstance(stmt, ast.Return):
            return False
        if isinstance(stmt, ast.Assign):
            for block_stmt in block:
                if not block_stmt in candidate:
                    for node in ast.walk(block_stmt):
                        if isinstance(node, ast.Name):
                            if hasattr(stmt.targets[0], 'id') and stmt.targets[0].id == node.id:
                                return False
    return True


def coefficient_calc(first_dep, second_dep):
    intersect = []
    second_dep_copy = copy(second_dep)
    for i in range(len(first_dep)):
        if first_dep[i] in second_dep_copy:
            intersect.append(first_dep[i])
            second_dep_copy.remove(first_dep[i])

    a = len(intersect)
    b = len(first_dep)
    c = len(second_dep)
    d = len(first_dep) + len(second_dep)

    num = 1.63*a + 0.08*d
    denom = a + 9.93*b + 0.03*c + 1.48*d

    return num / denom if denom != 0 else 0


def dist_calc(first_dep, second_dep):
    return 1 - coefficient_calc(first_dep, second_dep)


def candidate_score_calc(candidate_deps, method_deps):
    score = dist_calc(candidate_deps['var'], method_deps['var'])/3 +\
            dist_calc(candidate_deps['method'], method_deps['method'])/3 +\
            dist_calc(candidate_deps['type'], method_deps['type'])/3

    return score


def analyser(directory):
    with open(directory, "r") as file:
        tree = ast.parse(file.read())

    tree_copy = deepcopy(tree)
    tree_copy.body = []

    for child_tree in ast.walk(tree):
        block_list = []
        block_statements = []
        candidates_scores = []

        if isinstance(child_tree, ast.FunctionDef):
            # Pegar todos os blocos da função
            walks(child_tree, block_list)

            # Pegar todos os candidatos à extração da função
            candidates = []
            for block in block_list:
                n = len(block)
                for i in range(n):
                    for j in range(i, n):
                        candidate = subset(block, i, j)
                        if isValid(block, candidate):
                            candidates.append(candidate)

            cont = 1
            for candidate in candidates:
                print('\nCandidato', cont)
                for candidate_stmt in candidate:
                    print(ast.dump(candidate_stmt, annotate_fields=True, include_attributes=False))
                cont += 1

            # Classificar candidatos por sua pontuação de baixa similaridade (maior distância)
            candidates_score = []
            for candidate in candidates:
                cand_depend = {'var': [], 'method': [], 'type': []}
                function_tree_copy = deepcopy(child_tree)

                # Pegar dependências do candidato
                for candidate_stmt in candidate:
                    for node in ast.walk(candidate_stmt):
                        for child in ast.iter_child_nodes(node):
                            if isinstance(child, ast.Name):
                                if not isinstance(node, ast.Call):
                                    cand_depend['var'].append(child.id)
                                    child.parent = node
                                if hasattr(child, 'id') and child.id in classes_methods.keys():
                                    cand_depend['type'].append(child.id)
                            if isinstance(child, ast.Call):
                                for call_child in ast.iter_child_nodes(child):
                                    if isinstance(call_child, ast.Attribute) and hasattr(child.func, 'attr'):
                                        cand_depend['method'].append(child.func.attr)

                    for node in ast.walk(function_tree_copy):
                        for child in ast.iter_child_nodes(node):
                            child_string = ast.dump(child, annotate_fields=True, include_attributes=False)
                            candidate_stmt_string = ast.dump(candidate_stmt, annotate_fields=True, include_attributes=False)
                            if child_string == candidate_stmt_string:
                                node.body.remove(child)

                # Pegar dependências do método sem o candidato
                mod_method_depend = {'var': [], 'method': [], 'type': []}
                for node in ast.walk(function_tree_copy):
                    for child in ast.iter_child_nodes(node):
                        if isinstance(child, ast.Name):
                            if not isinstance(node, ast.Call):
                                mod_method_depend['var'].append(child.id)
                                child.parent = node
                            if hasattr(child, 'id') and child.id in classes_methods.keys():
                                mod_method_depend['type'].append(child.id)
                        if isinstance(child, ast.Call):
                            for call_child in ast.iter_child_nodes(child):
                                if isinstance(call_child, ast.Attribute) and hasattr(child.func, 'attr'):
                                    mod_method_depend['method'].append(child.func.attr)

                score = candidate_score_calc(cand_depend, mod_method_depend)
                candidates_scores.append((score, candidate))

            candidate_scores_sort = sorted(candidates_scores, reverse=True, key=lambda tup: tup[0])
            # score, top_candidate = candidate_scores_sort[0]

            # print()
            # # print(score)
            # for score, cand in candidate_scores_sort:
            #     print(score)
            #     for stmt in cand:
            #         print(ast.dump(stmt, annotate_fields=True, include_attributes=False))
            #     print()
            # sys.exit()


            # Criação do nó de marcação de extração para cada candidato
            extract_cont = 1
            for score, top_candidate in candidate_scores_sort:
                # Marcação de início de extração
                start_line = None
                first_candidate_stmt = top_candidate[0]
                extract_string_start = 'Recomendação: Início da extração ' + str(extract_cont)
                start_line = first_candidate_stmt
                start_appointment = ast.Expr(value=[(ast.Str(extract_string_start))])

                # Marcação de fim de extração
                end_line = None
                last_candidate_stmt = top_candidate[len(top_candidate)-1]
                extract_string_end = 'Recomendação: Fim da extração ' + str(extract_cont)
                for node in ast.walk(child_tree):
                    for child in ast.iter_child_nodes(node):
                        string_last_candidate_stmt_stmt = ast.dump(last_candidate_stmt, annotate_fields=True, include_attributes=False)
                        string_child = ast.dump(child, annotate_fields=True, include_attributes=False)
                        if string_child == string_last_candidate_stmt_stmt:
                            end_line = child
                            end_appointment = ast.Expr(value=[(ast.Str(extract_string_end))])

                extract_cont += 1

                # Inserção da marcação na árvore da função
                method_index = tree.body.index(child_tree)
                tree.body.remove(child_tree)
                for node in ast.walk(child_tree):
                    if hasattr(node, 'body'):
                        pos_body = 0
                        for child in node.body:
                            if ast.dump(child, annotate_fields=True, include_attributes=False) == ast.dump(start_line, annotate_fields=True, include_attributes=False):
                                node.body.insert(pos_body, start_appointment)
                                break
                            pos_body += 1
                        pos_body = 0
                        for child in ast.iter_child_nodes(node):
                            if ast.dump(child, annotate_fields=True, include_attributes=False) == ast.dump(end_line, annotate_fields=True, include_attributes=False):
                                node.body.insert(pos_body, end_appointment)
                            pos_body += 1

                tree.body.insert(method_index, child_tree)

    source_code = astor.to_source(tree)
    result_file = open('examples/other_example/result_file.py', 'w')
    result_file.writelines(source_code)
    result_file.close()
    print('\nArquivo modificado')


def getClassMethods():
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

    for path in files_path:
        with open(path, "r") as file:
            tree = ast.parse(file.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                classes_methods[class_name] = []
                for child in ast.iter_child_nodes(node):
                    if isinstance(child, ast.FunctionDef) and child.name != '__init__':
                        classes_methods[class_name].append(child.name)

    print('Aqui:\n', classes_methods)

if __name__ == '__main__':
    getClassMethods()
    directory = 'examples/other_example/analisador_test.py'

    try:
        analyser(directory)

    except OSError:
        print('Algum erro aconteceu')
