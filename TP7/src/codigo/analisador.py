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
from copy import deepcopy


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
    for stmt in candidate:
        if isinstance(stmt, ast.Return):
            return False
        if isinstance(stmt, ast.Assign):
            for block_stmt in block:
                if not block_stmt in candidate:
                    for node in ast.walk(block_stmt):
                        if isinstance(node, ast.Name):
                            if stmt.targets[0].id == node.id:
                                return False
    return True


def distance_calc(first_dep, second_dep):
    print(second_dep)
    sys.exit()

def analyser(directory):
    with open(directory, "r") as file:
        tree = ast.parse(file.read())

    for child_tree in tree.body:
        block_list = []
        block_statements = []

        if isinstance(child_tree, ast.FunctionDef):
            walks(child_tree, block_list)

            # for block in block_list:
            for statement in block_list[0]:
                print(ast.dump(statement, annotate_fields=True, include_attributes=False))
                print()
            print('--------------------------------------------')
            print('++++++++++++++++++++++++++++++++++++++++++++')

            candidates = []
            for block in block_list:
                n = len(block)
                for i in range(n):
                    # print('******************')
                    for j in range(i, n):
                        candidate = subset(block, i, j)
                        if isValid(block, candidate):
                            candidates.append(candidate)
                        #     print('Valid ->\n')
                        #     for candidate_stmt in candidate:
                        #         print(ast.dump(candidate_stmt, annotate_fields=True, include_attributes=False))
                        # print('--------------')

            cont = 1
            for candidate in candidates:
                print('\nCandidato', cont)
                for candidate_stmt in candidate:
                    print(ast.dump(candidate_stmt, annotate_fields=True, include_attributes=False))
                cont += 1

            candidates_dep = []
            candidates_score = []
            for candidate in candidates:
                dependencies = set()
                # function_tree_copy = deepcopy(child_tree)
                function_tree_copy = type(child_tree).__new__(type(child_tree))
                function_tree_copy.__dict__.update(child_tree.__dict__)
                for candidate_stmt in candidate:
                    for node in ast.walk(candidate_stmt):
                        for child in ast.iter_child_nodes(node):
                            if isinstance(child, ast.Name):
                                if not isinstance(node, ast.Call):
                                    dependencies.add(child.id)
                                    child.parent = node

                    i = 0
                    j = 0
                    for node in ast.walk(function_tree_copy):
                        for child in ast.iter_child_nodes(node):
                            if child == candidate_stmt:
                                node.body.remove(child)
                            j += 1
                        i += 1

                # mod_method_depend = set()
                # for node in ast.walk(function_tree_copy):
                #     for child in ast.iter_child_nodes(node):
                #         if isinstance(child, ast.Name):
                #             if not isinstance(node, ast.Call):
                #                 mod_method_depend.add(child.id)
                #                 child.parent = node
                #
                # score = distance_calc(dependencies, mod_method_depend)
                #
                # candidates_dep.append(dependencies)

                k = 0
                l = 0
                for candidate_stmt in candidate:
                    for node in ast.walk(function_tree_copy):
                        for child in ast.iter_child_nodes(node):
                            if k == i and l == j-1:
                                node.body.insert(k, candidate_stmt)
                            k += 1
                        l += 1

                print('\nAqui')
                print(ast.dump(child_tree, annotate_fields=True, include_attributes=False))
                sys.exit()

            print('\nDeps:')
            for cand_deps in candidates_dep:
                print(cand_deps)

            print(list(zip(candidates, candidates_dep)))

            # print('\nMethod Deps:', mod_method_depend)


if __name__ == '__main__':
    # directory = os.path.join(os.getcwd(), sys.argv[1])
    directory = 'examples/analisador_test.py'

    try:
        analyser(directory)

    except OSError:
        print('Algum erro aconteceu')
