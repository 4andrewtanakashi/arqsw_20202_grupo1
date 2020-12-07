class A:
    variavel = 'vari'
    
    def __init__(self, varA, varB):
      self.varA = varA
      self.varB = varB
      self.varF = 0
      self.varG = 1
      self.varH = 2
      self.varI = 3
      self.varJ = 4
      self.varZ = 5
    
    def m1(self):
        print('primeiro metodo de A', self.varJ)
        self.varA = 'primeiroVarB' + str(self.varG)
        s = 'The value of x is ' + repr(self.varI)
        print(s)
        print(self.varA)
        self.varZ = 5 * 10
    
    def m2(self):
        print('segundo metodo de A' + str(self.varH))
        self.varB = self.varF
        self.variavel= 'avel'
        print(f'O valor de varZ é {self.varZ}.')
        t = 'Testando'
        print(f'Teste de self.t {t}')
        
if __name__ == '__main__':
    class_a = A('initVarA', 'initVarB')
    class_a.m2()
