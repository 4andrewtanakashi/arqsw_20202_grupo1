# Generated from Python3.g4 by ANTLR 4.7.2
from antlr4 import *
import re

if __name__ is not None and "." in __name__:
    from .Python3Parser import Python3Parser
else:
    from Python3Parser import Python3Parser

# This class defines a complete listener for a parse tree produced by Python3Parser.
class Python3Listener(ParseTreeListener):


    # Enter a parse tree produced by Python3Parser#funcdef.
    def enterFuncdef(self, ctx:Python3Parser.FuncdefContext):
        # funcdef = ctx.getChild(1)
        # if ( (funcdef != None) and (re.fullmatch("^_?[a-z]+[\da-z]*(_[\da-z]+)*$", funcdef.getText()) == None)):
        #     print("Está fora do padrão lower_snake_case", funcdef.getText(), "Line: {}".format(str(funcdef.getSymbol().line)))
        pass


    # Enter a parse tree produced by Python3Parser#typedargslist.
    def enterTypedargslist(self, ctx:Python3Parser.TypedargslistContext):
        # funcdef = ctx.getChild(1)
        # if ((funcdef != None) and ((re.fullmatch("(   ^_?[A-Z]+[\dA-Z]*(_[\dA-Z]+)*$ |  ^_?[a-z]+[\da-z]*(_[\da-z]+)*$  )", funcdef.getText()) == None))):
        #     print("Está não está em padrão lower_snake_case ou UPPER_SNAKE_CASE", funcdef.getText(), "Line: {}".format(str(funcdef.getSymbol().line)))
        pass


    # Enter a parse tree produced by Python3Parser#classdef.
    def enterClassdef(self, ctx:Python3Parser.ClassdefContext):
        # classDef = ctx.getChild(1)
        # if ((classDef != None) and (re.fullmatch("^_?[A-Z][\da-z]*(_[A-Z][\da-z]*)*$", classDef.getText()) == None)):
        #     print("Está fora do padrão Upper_Snake_Camel_Case", classDef.getText(), "Line: {}".format(str(classDef.getSymbol().line)))
        pass
