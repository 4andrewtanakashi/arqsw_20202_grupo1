import os
import sys
import io


from antlr4 import *
from antlr4.error.ErrorListener import *
from g4_python.Python3Lexer import Python3Lexer
from g4_python.Python3Parser import Python3Parser
from g4_python.Python3Listener import Python3Listener
from g4_python.Python3Visitor import Python3Visitor


matrix_inherit = {}
classes_methods = {}


class RuleListener(Python3Listener):
    def enterEveryRule(self, ctx):
        global matrix_inherit
        global classes_methods

        if isinstance(ctx, Python3Parser.ClassdefContext):
            class_name = ctx.getChild(1).getText()
            classes_methods[class_name] = []
            matrix_inherit[class_name] = []            
            
            for i in range(ctx.getChildCount()):
                if isinstance(ctx.getChild(i), Python3Parser.ArglistContext):
                    if ctx.getChild(i).getText():
                        class_args = ctx.getChild(i).getText().split(',')
                        matrix_inherit[class_name] = [arg for arg in class_args]            
                    
                if isinstance(ctx.getChild(i), Python3Parser.SuiteContext):
                    for child_ctx in ctx.getChildren():
                        for j in range(child_ctx.getChildCount()):
                            if isinstance(child_ctx.getChild(j), Python3Parser.StmtContext):
                                stmt = child_ctx.getChild(j)
                                for child_stmt in stmt.getChildren():
                                    if isinstance(child_stmt, Python3Parser.Compound_stmtContext):
                                        for child_compound in child_stmt.getChildren():
                                            if isinstance(child_compound, Python3Parser.FuncdefContext):
                                                if child_compound.getChild(1):
                                                  if isinstance(child_compound.getChild(1), TerminalNode):
                                                      if child_compound.getChild(1).getText() != '__init__':                                                            
                                                          classes_methods[class_name].append(child_compound.getChild(1).getText())
           
            print('Nome da classe:', class_name)
            print('Matriz de herança:', matrix_inherit)
            print('Metodos da classe:', classes_methods, '\n')


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
        for path in files_path:
            input = FileStream(path)
            lexer = Python3Lexer(input)
            stream = CommonTokenStream(lexer)

            stream.fill()

            parser = Python3Parser(stream)
            tree = parser.file_input()
            listener = RuleListener()
            walker = ParseTreeWalker()
            walker.walk(listener, tree)
        
        for class_name in matrix_inherit:
            print('Pais da classe', class_name, '->', matrix_inherit[class_name])
            if len(matrix_inherit[class_name]) > 1:            
                print('\nExiste heranca multipla da classe', class_name, 'com as classes', matrix_inherit[class_name], '\n')
                
                # Verifica ambiguidade de heranca multipla
                parents_class = matrix_inherit[class_name]
                ambig_inherit_classes = {}
                for i in range(len(parents_class) - 1):
                    for j in range(i+1, len(parents_class)):
                        ambig_methods = list(set(classes_methods[parents_class[i]]).intersection(classes_methods[parents_class[j]]))
                        #print('Metodos ambiguos:', metodos_ambiguos)
                        if len(ambig_methods) > 0:
                            for metodo in ambig_methods:
                                #print('Classes heranca ambigua:', classes_heranca_ambigua)
                                if metodo in ambig_inherit_classes.keys():
                                    if parents_class[i] not in ambig_inherit_classes[metodo]:
                                        ambig_inherit_classes[metodo].append(parents_class[i])
                                    if parents_class[j] not in ambig_inherit_classes[metodo]:
                                        ambig_inherit_classes[metodo].append(parents_class[j])
                                else:
                                    ambig_inherit_classes[metodo] = [parents_class[i], parents_class[j]]

                                print('Existe ambiguidade de heranca multipla entre as classes', parents_class[i], 'e', parents_class[j], 'com os metodos', ambig_methods)
                          
                print('\nClasses com heranca ambigua ->', ambig_inherit_classes, '\n')
                
                # Verifica problema do diamante
                for method in ambig_inherit_classes:
                    intermediate_classes = ambig_inherit_classes[method]
                    for i in range(len(intermediate_classes) - 1):
                        for j in range(i+1, len(intermediate_classes)):
                            common_inheritance = list(set(matrix_inherit[intermediate_classes[i]]).intersection(matrix_inherit[intermediate_classes[j]]))
                            if len(common_inheritance) > 0:
                                print('Problema do diamante encontrado na classe', class_name, 'herdada de', [intermediate_classes[i], intermediate_classes[j]], 'que herdam de', common_inheritance)
                    print()

    except OSError:
        print('Algum erro aconteceu')


















