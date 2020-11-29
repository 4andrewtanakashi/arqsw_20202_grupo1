from unittest import TestCase

import os
import sys
import io

from antlr4 import *
from antlr4.error.ErrorListener import *
from g4_python.Python3Lexer import Python3Lexer
from g4_python.Python3Parser import Python3Parser
from g4_python.Python3Listener import Python3Listener
from g4_python.Python3Visitor import Python3Visitor

matrix = {}
classes_methods = {}

class Python3ErrorListener(ErrorListener):
    def __init__(self, output):
        self.output = output
        self._symbol = ''

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.output.write(msg)
        self._symbol = offendingSymbol.text
        stack = recognizer.getRuleInvocationStack()
        stack.reverse()
        print("rule stack: {}".format(str(stack)))
        print("line {} : {} at {} : {}".format(str(line),
                                               str(column),
                                               str(offendingSymbol).replace(" ", u'\u23B5'),
                                               msg.replace(" ", u'\u23B5')))

    @property
    def symbol(self):
        return self._symbol


def get_split(class_names):
    return class_names.split(',')


class RuleListener(Python3Listener):
    def enterEveryRule(self, ctx):
        global matrix
        global classes_methods

        if isinstance(ctx, Python3Parser.ClassdefContext):
            ##print('AquiClassdef: \n', ctx.getText())
            #print('Filho 2 da classe: ', ctx.getChild(1))
            class_name = ctx.getChild(1).getText()
            classes_methods[class_name] = []
            matrix[class_name] = []
            print('ClassName ', class_name)
            for i in range(ctx.getChildCount()):
                if isinstance(ctx.getChild(i), Python3Parser.ArglistContext):
                    ##print('AquiArglist: \n', ctx.getChild(i).getText())
                    if ctx.getChild(i).getText():
                        matrix[class_name] = [k for k in get_split(ctx.getChild(i).getText())]
                    print('Matriz: ', matrix)
                    
                if isinstance(ctx.getChild(i), Python3Parser.SuiteContext):
                    ##print('\nAquiSuite:', ctx.getChild(i).getText())
                    for child_ctx in ctx.getChildren():
                        for j in range(child_ctx.getChildCount()):
                            if isinstance(child_ctx.getChild(j), Python3Parser.StmtContext):
                                stmt = child_ctx.getChild(j)
                                #print('\nAquiStmt: \n', stmt.getText())
                                for child_stmt in stmt.getChildren():
                                    #print('Filhos Stmt: \n', help(child_stmt))
                                    if isinstance(child_stmt, Python3Parser.Compound_stmtContext):
                                        #print('AquiCompound: \n', child_stmt.getText())
                                        for child_compound in child_stmt.getChildren():
                                            if isinstance(child_compound, Python3Parser.FuncdefContext):
                                                ##print('AquiFuncdef: \n', child_compound.getText())
                                                if isinstance(child_compound.getChild(1), TerminalNode):
                                                    #print('Filho 2 Funcdef:', child_compound.getChild(1).getText())
                                                    if child_compound.getChild(1).getText() != '__init__':                                                            
                                                        classes_methods[class_name].append(child_compound.getChild(1).getText())
                                                print('Metodos da classe', classes_methods, "\n\n")


def setup(path):
    input = FileStream(path)
    lexer = Python3Lexer(input)
    stream = CommonTokenStream(lexer)

    # print out the token parsing
    stream.fill()
    # print("TOKENS")
    for token in stream.tokens:
        if token.text != '<EOF>':
            type_name = Python3Parser.symbolicNames[token.type]
            tabs = 5 - len(type_name) // 4
            sep = "\t" * tabs
            # print("    %s%s%s" % (type_name, sep,
            #                       token.text.replace(" ", u'\u23B5').replace("\n", u'\u2936')))
    parser = Python3Parser(stream)

    output = io.StringIO()
    error = io.StringIO()

    parser.removeErrorListeners()
    errorListener = Python3ErrorListener(error)
    parser.addErrorListener(errorListener)
    return parser


if __name__ == '__main__':
    directory = os.path.join(os.getcwd(), sys.argv[1])

    #TODO Lançar exceção quando a pasta não existir
    files_name = []
    files_path = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            if name.endswith(".py"):
                files_name.append(name)
                file_path = os.path.join(root, name)
                files_path.append(file_path)

    print(files_name)
    print(files_path)

    try:
        for path in files_path:
            parser = setup(path)
            tree = parser.file_input()
            listener = RuleListener()
            walker = ParseTreeWalker()
            walker.walk(listener, tree)
        
        print()
        
        for classe in matrix:
            if len(matrix[classe]) > 1:
                print('Existe herança multipla de', classe, 'com as classes', matrix[classe])
                
                # Teste para ambiguidade de heranca multipla
                classes_pai = matrix[classe]
                classes_heranca_ambigua = {}
                for i in range(len(classes_pai) - 1):
                    for j in range(1, len(classes_pai)):
                        metodos_ambiguos = list(set(classes_methods[classes_pai[i]]).intersection(classes_methods[classes_pai[j]]))
                        if len(metodos_ambiguos) > 0:
                            for metodo in metodos_ambiguos:
                                classes_heranca_ambigua[metodo] = [classes_pai[i], classes_pai[j]]
                                print('Existe ambiguidade de heranca multipla entre as classes', classes_pai[i], 'e', classes_pai[j], 'com os metodos', metodos_ambiguos)
                            
                print('Classes heranca ambigua ->', classes_heranca_ambigua)
                
                # Teste para ambiguidade de diamante
                for c in classes_heranca_ambigua:
                    classes_intermediarias = classes_heranca_ambigua[c]
                    for i in range(len(classes_intermediarias) - 1):
                        for j in range(1, len(classes_intermediarias)):
                            heranca_comum_intermediarias = list(set(matrix[classes_intermediarias[i]]).intersection(matrix[classes_intermediarias[j]]))
                            if len(heranca_comum_intermediarias) > 0:
                                print('Problema do diamante encontrado na classe', classe, 'herdada de', classes_intermediarias, 'que herdam de', heranca_comum_intermediarias)

            else:
                print('Classe ', classe, ' -> ', matrix[classe])

    except OSError:
        print('Algum erro aconteceu')

