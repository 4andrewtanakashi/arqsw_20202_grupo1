import os
import sys
import io


from antlr4 import *
from antlr4.error.ErrorListener import *
from g4_python.Python3Lexer import Python3Lexer
from g4_python.Python3Parser import Python3Parser
from g4_python.Python3Listener import Python3Listener


class LCOM1(Python3Listener):
    def __init__(self, file_path):
        self.file_path = file_path
        self.use_class_variables = {}
        self.class_name = ''
        self.p = 0
        self.q = 0
        self.result = 0


    def enterEveryRule(self, ctx):
        if isinstance(ctx, Python3Parser.ClassdefContext):
            self.class_name = ctx.getChild(1).getText()
            suite_tree = self.walks(ctx, 'suite')

            for suite_child in suite_tree.getChildren():
                funcdef_tree = self.walks(suite_child, 'funcdef')
                
                if funcdef_tree:
                    method_name = funcdef_tree.getChild(1).getText()

                    if method_name != '__init__':
                        self.use_class_variables[method_name] = set()
                        suite_func_tree = self.walks(funcdef_tree, 'suite')

                        for suite_func_child in suite_func_tree.getChildren():
                            self.get_methods_self_variables(suite_func_child, self.use_class_variables[method_name])

            print('\nUtilização variáveis da classe', self.class_name + ':', self.use_class_variables, '\n')
    

    def input_read(self):        
        input = FileStream(self.file_path, "UTF-8")
        lexer = Python3Lexer(input)
        stream = CommonTokenStream(lexer)

        stream.fill()

        parser = Python3Parser(stream)
        tree = parser.file_input()
        listener = self
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

            
    def get_methods_self_variables(self, tree, method_self_variables):
        if isinstance(tree, TerminalNode):
            pass

        elif isinstance(tree, Python3Parser.Atom_exprContext):
            class_variable = False
            for atom_expr_child in tree.getChildren():
                if atom_expr_child.getChild(0).getText() == 'self':
                    class_variable = True
                elif atom_expr_child.getChild(0).getText()[0] == 'f':
                    if '{self.' in atom_expr_child.getChild(0).getText():
                        method_self_variables.add('self.' + atom_expr_child.getChild(0).getText().split('self.')[1].split('}')[0])
                    
                if class_variable and isinstance(atom_expr_child, Python3Parser.TrailerContext):
                    method_self_variables.add(tree.getText())

            for child in tree.children:
                self.get_methods_self_variables(child, method_self_variables)
        else:
            for child in tree.children:
                self.get_methods_self_variables(child, method_self_variables)


    def walks(self, tree, goal_rule):
        if not isinstance(tree, TerminalNode):
            if Python3Parser.ruleNames[tree.getRuleIndex()] == goal_rule:
                return tree
            else:
                for child in tree.getChildren():
                    tree = self.walks(child, goal_rule)
                    if tree:
                        return tree


    def calculate(self):
        methods_name = list(self.use_class_variables.keys())
        for i in range(len(methods_name)-1):
            for j in range(i+1, len(methods_name)):
                intersec = list(set(self.use_class_variables[methods_name[i]]).intersection(self.use_class_variables[methods_name[j]]))

                if len(intersec) > 0:
                    self.q += 1
                else:
                    self.p += 1

        print('P ->', self.p)
        print('Q ->', self.q)

        self.result = (self.p - self.q) if (self.p >= self.q) else 0
        
        print('Resultado:', self.result)
    
    
    def print_result(self):
        if self.result == 0:
            print('\nA classe', self.class_name, 'está coesa, pois seu LCOM1 é', self.result)
        else:
            print('\nA classe', self.class_name, 'precisa ser divida, pois seu LCOM1 é', self.result)


    def run(self):
        self.input_read()
        self.calculate()
        self.print_result()


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

    print('Nome dos arquivos:\n', files_name)
    
    for path in files_path:
        lcom = LCOM1(path)
        lcom.run()
