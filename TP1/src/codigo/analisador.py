import os
import sys
from antlr4 import *
from g4_python.Python3Lexer import Python3Lexer
from g4_python.Python3Parser import Python3Parser

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


def main2(argv):
    input = FileStream(argv[1])
    lexer = Python3Lexer(input)
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)
    tree = parser.classdef()
    print(tree.toStringTree())


if __name__ == '__main__':
    main2(sys.argv)