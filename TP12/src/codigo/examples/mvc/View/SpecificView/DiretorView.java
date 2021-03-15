package View.SpecificView;

import Model.Diretor;
import View.GeneralView.MainView;

public class DiretorView extends MainView {

	public void printDiretorDetalhe(String nome, String escola, Diretor diretor){
		System.out.println("\n --DADOS DO DIRETOR--");
		System.out.println("Nome:"+nome);
		System.out.println("Diretor na Escola:"+ diretor.getEscola());
	}
}
