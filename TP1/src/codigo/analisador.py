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

import antlr_ast

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


class RuleListener(Python3Listener):
    def enterEveryRule(self, ctx):
        if isinstance(ctx, Python3Parser.ClassdefContext):
            class_names = []
            for i in range(ctx.getChildCount()):
                if isinstance(ctx.getChild(i), TerminalNode):
                   class_names.append(ctx.getChild(i).getText())
            print(class_names)

        elif isinstance(ctx, Python3Parser.FuncdefContext):
            func_names = []
            for i in range(ctx.getChildCount()):
                if isinstance(ctx.getChild(i), TerminalNode):
                   func_names.append(ctx.getChild(i).getText())
            print(func_names)


def main():
    try:
        with os.scandir('src/') as entries:
            for entry in entries:
                print(entry.name)

                try:
                    with open('src/' + entry.name, 'r') as f:
                        if (f.mode == 'r'):
                            data = f.read()
                            print(data)
                except OSError:
                    print('Erro na leitura do Arquivo')
    except OSError:
        print('Diretório não existe')

def setup(path):
    input = FileStream(path)
    lexer = Python3Lexer(input)
    stream = CommonTokenStream(lexer)

    # print out the token parsing
    stream.fill()
    print("TOKENS")
    for token in stream.tokens:
        if token.text != '<EOF>':
            type_name = Python3Parser.symbolicNames[token.type]
            tabs = 5 - len(type_name) // 4
            sep = "\t" * tabs
            print("    %s%s%s" % (type_name, sep,
                                  token.text.replace(" ", u'\u23B5').replace("\n", u'\u2936')))
    parser = Python3Parser(stream)

    output = io.StringIO()
    error = io.StringIO()

    parser.removeErrorListeners()
    errorListener = Python3ErrorListener(error)
    parser.addErrorListener(errorListener)
    return parser


def main2():
    parser = setup("./src/B.py")
    tree = parser.file_input()
    listener = RuleListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)


if __name__ == '__main__':
    main2()