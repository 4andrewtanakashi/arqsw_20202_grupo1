#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

# """
# ***
#
# Obs.: Este programa pode gerar documentação com seguinte comando (no Linux):
#     python3 -m pydoc -w analisador
#
#     Para visualização no terminal: python3 -m pydoc analisador
# """
# __author__ = "Andrew Takeshi and Gabriel Amorim"
# __copyright__ = "Copyright 2020, Por nós"
# __credits__ = ["Desenvolvido para disciplina de Arquitetura de Software"]
# __devs__ = "@4andrewtanakashi & @ghamorim"
# __status__ = "Production"
#
#
# import os
# import sys
# import io
# import ast
# import astor



# p1 = getPoint(0, 0)
# p2 = getPoint(1, 0)
# r.add(START.get().getBounds(p1, p2))
#
#
#
# p2 = getPoint(1, 0)
# r.add(START.get().getBounds(p1, p2))
#
#
#
# r.add(START.get().getBounds(p1, p2))



def getFigureDrawBounds():
    r = super.getFigDrawBounds()
    if getNodeCount() > 1:
        if START.get() != None:
            p1 = getPoint(0, 0)
            p2 = getPoint(1, 0)
            r.add(START.get().getBounds(p1, p2))
        if END.get() != None:
            p1 = getPoint(getNodeCount()-1, 0)
            p2 = getPoint(getNodeCount()-2, 0)
            r.add(END.get().getBounds(p1, p2))
    return r


# def analyser(directory):
#     # Pegando classes modelos
#     model_file_path = directory + 'models.py'
#     with open(model_file_path, "r") as file:
#         tree = ast.parse(file.read())
#
#     model_classes = []
#     for node in tree.body:
#         if isinstance(node, ast.ClassDef):
#             class_name = node.name
#             for class_args in node.bases:
#                 if class_args.value.id == 'models' and class_args.attr == 'Model':
#                     model_classes.append(class_name)
#

    # # Criando arquivo serializers.py
    # serializers_file_path = directory + 'serializers.py'
    # with open(serializers_file_path, "w+") as file:
    #     serializers_file_tree = ast.parse(file.read())
    # file.close()
    #
    # import_from_node1 = ast.ImportFrom\
    #         (module='rest_framework',\
    #         names=[ast.alias(name='serializers', asname=None)],\
    #         level=0)
    #
    # import_from_node2 = ast.ImportFrom\
    #         (module='models',\
    #         names=[(ast.alias(name=class_name, asname=None)) for class_name in model_classes],\
    #         level=1)
    #
    # serializers_file_tree.body.append(import_from_node1)
    # serializers_file_tree.body.append(import_from_node2)
    #
    # for class_name in model_classes:
    #     class_node = ast.ClassDef\
    #             (name=class_name+'Serializer',\
    #             bases=[ast.Attribute(value=ast.Name(id='serializers', ctx=ast.Load()),\
    #                     attr='ModelSerializer', ctx=ast.Load())],\
    #             keywords=[],\
    #             body=[ast.ClassDef(name='Meta', bases=[], keywords=[],\
    #                     body=[ast.Assign(targets=[ast.Name(id='model', ctx=ast.Store())],\
    #                             value=ast.Name(id=class_name, ctx=ast.Load())),\
    #                             ast.Assign(targets=[ast.Name(id='fields', ctx=ast.Store())],\
    #                             value=ast.Str(s='__all__'))],\
    #                     decorator_list=[])],\
    #             decorator_list=[])
    #
    #     serializers_file_tree.body.append(class_node)
    #
    # source_code = astor.to_source(serializers_file_tree)
    # serializers_file = open(serializers_file_path, 'w')
    # serializers_file.writelines(source_code)
    # serializers_file.close()
    # print('Arquivo de serialização criado')
    #
    #
    # # Modificando arquivo views.py
    # views_file_path = directory + 'views.py'
    # with open(views_file_path, "r") as file:
    #     views_file_tree = ast.parse(file.read())
    # file.close()
    #
    # forms_imports = []
    # model_imports = []
    # for node in views_file_tree.body:
    #     if isinstance(node, ast.ImportFrom):
    #         if node.module == 'forms':
    #             for alias_node in node.names:
    #                 forms_imports.append(alias_node.name)
    #             views_file_tree.body.remove(node)
    #         elif node.module == 'models':
    #             for alias_node in node.names:
    #                 model_imports.append(alias_node.name)
    #
    #
    # import_from_node1 = ast.ImportFrom\
    #         (module='rest_framework.response',\
    #         names=[ast.alias(name='Response', asname=None)],\
    #         level=0)
    #
    # import_from_node2 = ast.ImportFrom\
    #         (module='serializers',\
    #         names=[(ast.alias(name=class_name+'Serializer', asname=None)) for class_name in model_classes],\
    #         level=1)
    #
    # import_from_node3 = ast.ImportFrom\
    #         (module='rest_framework.decorators',\
    #         names=[ast.alias(name='api_view', asname=None)],\
    #         level=0)
    #
    # views_file_tree.body.insert(0, import_from_node1)
    # views_file_tree.body.insert(1, import_from_node2)
    # views_file_tree.body.insert(2, import_from_node3)
    #
    # for node in views_file_tree.body:
    #     delete_attr = False
    #     if isinstance(node, ast.FunctionDef):
    #         for func_child in node.body:
    #             if isinstance(func_child, ast.Assign):
    #                 if not isinstance(func_child.value.func, ast.Attribute):
    #                     if func_child.value.func.id in forms_imports:
    #                         node.decorator_list.append(ast.Call\
    #                                 (func=ast.Name(id='api_view',\
    #                                 ctx=ast.Load()), args=[ast.List(elts=[ast.Str(s='POST')], ctx=ast.Load())],\
    #                                 keywords=[]))
    #                 elif func_child.value.func.value.value.id in model_imports:
    #                     if func_child.value.func.attr == 'all':
    #                         node.decorator_list.append(ast.Call\
    #                                 (func=ast.Name(id='api_view',\
    #                                 ctx=ast.Load()), args=[ast.List(elts=[ast.Str(s='GET')], ctx=ast.Load())],\
    #                                 keywords=[]))
    #                         index_insert_serializer = node.body.index(func_child) + 1
    #                         node.body.insert(index_insert_serializer, ast.Assign\
    #                                 (targets=[ast.Name(id='serializer', ctx=ast.Store())],
    #                                 value=ast.Call(func=ast.Name(id='ProductSerializer', ctx=ast.Load()),
    #                                 args=[ast.Name(id='products', ctx=ast.Load())],
    #                                 keywords=[ast.keyword(arg='many', value=ast.NameConstant(value=True))])))
    #
    #                     elif func_child.value.func.attr == 'get':
    #                         stmt = func_child.targets[0].id
    #                         for node_child in ast.walk(node):
    #                             if isinstance(node_child, ast.Call):
    #                                 for call_node_child in ast.walk(node_child):
    #                                     if isinstance(call_node_child, ast.Attribute):
    #                                         for attribute_node_child in ast.walk(call_node_child):
    #                                             if isinstance(attribute_node_child, ast.Name):
    #                                                 if attribute_node_child.id == stmt and call_node_child.attr == 'delete':
    #                                                     node.decorator_list.append(ast.Call\
    #                                                             (func=ast.Name(id='api_view',\
    #                                                             ctx=ast.Load()), args=[ast.List(elts=[ast.Str(s='DELETE')], ctx=ast.Load())],\
    #                                                             keywords=[]))
    #                                                     index_insert_delete = node.body.index(func_child) + 1
    #                                                     node.body.insert(index_insert_delete, ast.Expr\
    #                                                             (value=ast.Call(func=ast.Attribute(value=ast.Name(id=stmt, ctx=ast.Load()),\
    #                                                             attr='delete', ctx=ast.Load()), args=[], keywords=[])))
    #
    #                                                     delete_attr = True
    #
    #             if isinstance(func_child, ast.Return):
    #                 func_child.value = ast.Call\
    #                         (func=ast.Name(id='Response', ctx=ast.Load()),\
    #                         args=[ast.Attribute(value=ast.Name(id='serializer', ctx=ast.Load()), attr='data', ctx=ast.Load())],\
    #                         keywords=[])
    #
    #         if delete_attr:
    #             for node_child in ast.walk(node):
    #                 if isinstance(node_child, ast.If):
    #                     node.body.remove(node_child)
    #
    #                 if isinstance(node_child, ast.Return):
    #                     node_child.value = ast.Call\
    #                             (func=ast.Name(id='Response', ctx=ast.Load()),\
    #                             args=[ast.Str(s='Product has been deleted')],\
    #                             keywords=[])
    #
    #
    # source_code = astor.to_source(views_file_tree)
    # views_file = open(views_file_path, 'w')
    # views_file.writelines(source_code)
    # views_file.close()
    # print('Arquivo de visão modificado')
    #
    # print('Aplicação alterada para o padrão REST')

# if __name__ == '__main__':
#     directory = os.path.join(os.getcwd(), sys.argv[1])
#
#     try:
#         analyser(directory)
#
#     except OSError:
#         print('Algum erro aconteceu')
