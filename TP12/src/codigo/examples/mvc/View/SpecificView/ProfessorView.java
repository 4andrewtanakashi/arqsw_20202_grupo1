package View.SpecificView;

import Model.Professor;

public class ProfessorView {

	public void printProfessorDetalhe(String nome, String escola, String disciplina, Professor prof){
		System.out.println(" \n --DADOS DO PROFESSOR--");
		System.out.println("Nome:"+nome);
		System.out.println("Professor na Escola:" + prof.getEscola());
		System.out.println("Professor de:" + prof.getDisciplina());
	}
}
