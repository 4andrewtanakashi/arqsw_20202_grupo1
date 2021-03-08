package Presenter;

import Model.*;
import View.DiretorView;
import View.EscolaView;
import View.EstudanteView;
import View.ProfessorView;

public class ProjetoMVP {

	public static void main(String[] args) {

		Escola escolaModel = new Escola("Anisio Teixeira");
		EscolaView escolaView = new EscolaView();
		EscolaPresenter escolaPresenter = new EscolaPresenter(escolaModel, escolaView);
		
		escolaPresenter.printEscolaDetalhe();

		Diretor diretorModel = new Diretor("Alberto", escolaModel);
		DiretorView diretorView = new DiretorView();
		DiretorPresenter diretorPresenter = new DiretorPresenter(diretorModel, diretorView);

		diretorPresenter.printDiretorDetalhe();

		Professor professorModel = new Professor("Ana Carla", escolaModel, "Geografia");
		ProfessorView professorView = new ProfessorView();
		ProfessorPresenter professorPresenter = new ProfessorPresenter(professorModel, professorView);

		professorPresenter.printProfessorDetalhe();


		Estudante estudanteModel = new Estudante("Luis Araujo",5,escolaModel);
		EstudanteView estudanteView = new EstudanteView();
		EstudantePresenter estudantePresenter = new EstudantePresenter(estudanteModel, estudanteView);

		estudantePresenter.printEstudanteDetalhe();






	}

}
