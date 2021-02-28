from util.utils import save_obj_to_file
from util.B_Colors import *
from fpdf import FPDF

class Generated_rules_file:

    def rules (obj_unico_pac, obj_unico_class, obj_rules):
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_xy(0,0)
        pdf.set_font('arial', 'B', 13.0)
        pdf.ln(0.15)
        pdf.multi_cell(0, 20, txt="---------------------------------------[Regras da Arquitetura]---------------------------------------")
        pdf.ln(0.15)
        text = ""
        i = 0
        for key, content in obj_unico_pac.items():
            for key_inter, content_inter in content.items():
                for item_content in content_inter:
                    text += "R" + str(i) + ": Somente o pacote " + key + " " + key_inter + " acessar o pacote " + item_content + "\n"
                    var_aux = "R" + str(i) + ": Somente o pacote " + key + " " + key_inter + " acessar o pacote " + item_content + "\n"
                    # pdf.set_text_color(0,255,0)
                    pdf.multi_cell(0, 5, txt=var_aux)
                    pdf.ln(0.15)
                    i += 1
        for key, content in obj_unico_class.items():
            for key_inter, content_inter in content.items():
                for item_content in content_inter:
                    text += "R" + str(i) + ": Somente a classe" + key + " " + key_inter + " acessar o pacote " + item_content + "\n"
                    pdf.set_text_color(0,0,0)
                    var_aux = "R" + str(i) + ": Somente a classe" + key + " " + key_inter + " acessar o pacote " + item_content + "\n"
                    pdf.multi_cell(0, 5, var_aux)
                    pdf.ln(0.15)
                    i += 1
        for key, content in obj_rules["LigacoesDePacotes"].items():
             for key_inter, content_inter in content.items():
                 if content_inter != {}:
                    for item_content in content_inter:
                        text += "R" + str(i) + ": O pacote " + key + " " + key_inter + " acessar o pacote " + item_content + "\n"
                        pdf.set_text_color(0,0,0)
                        var_aux = "R" + str(i) + ": O pacote " + key + " " + key_inter + " acessar o pacote " + item_content + "\n"
                        pdf.multi_cell(0, 5, var_aux)
                        pdf.ln(0.15)
                        i += 1
        for key, content in obj_rules["LigacoesClassesComPacotes"].items():
             for key_inter, content_inter in content.items():
                if content_inter != {}:
                 for item_content in content_inter:
                     text += "R" + str(i) + ": A classe " + key + " " + key_inter + " acessar o pacote " + item_content + "\n"
                     pdf.set_text_color(0,0,0)
                     var_aux =  "R" + str(i) + ": A classe " + key + " " + key_inter + " acessar o pacote " + item_content + "\n"
                     pdf.multi_cell(0, 5, var_aux)
                     pdf.ln(0.15)
                     i += 1


        pdf.ln(0.15)
        pdf.multi_cell(0, 20, txt="----------------------------------------------------------------------------------------------------------")
        # pdf.multi_cell(0, 5, text)
        pdf.output("files/Regras.pdf", 'F')
        print(text)
        save_obj_to_file(text, "/files/Regras.txt")
