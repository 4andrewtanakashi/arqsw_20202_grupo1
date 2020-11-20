import os
import sys
from antlr4 import *
from MyGrammarLexer import MyGrammarLexer
from MyGrammarParser import MyGrammarParser

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