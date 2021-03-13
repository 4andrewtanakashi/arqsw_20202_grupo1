package View;

import Model.Estudante;

public class EstudanteView {
	public void printProfessorDetalhe(String nome, String escola, String anoEscolar, Estudante estudante){
		System.out.println(" \n --DADOS DO ESTUDANTE--");
		System.out.println("Nome:" + nome);
		System.out.println("Professor na Escola:" + estudante.getEscola());
		System.out.println("Ano Escolar:" + estudante.getAnoEscolar());
	}
}
