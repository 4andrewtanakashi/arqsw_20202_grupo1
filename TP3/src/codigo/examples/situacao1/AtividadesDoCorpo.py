import Relogio as rlg

class Atividades_Do_Corpo:
    varQlq = rlg.Relogio()

    def __init__(self):
        self.coracao = "cardiáco"
        self.utensilio = rlg.Relogio()

    CHECANDO_PRESSAO = 10.5
    def Andar(velocidade):
        print('Está andando ...')
        print(Atividades_Do_Corpo.CHECANDO_PRESSAO)
        print("velocidade: {}". format(velocidade))

    def ver_horas(self):
        self.utensilio.ligar()
        print(" Qualquer " + self.coracao)

x = Atividades_Do_Corpo()
x.ver_horas()
Atividades_Do_Corpo.varQlq.ligar()
