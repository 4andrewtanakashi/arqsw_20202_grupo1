package Presenter;

import Model.Escola;
import Model.Estudante;
import View.EstudanteView;


public class EstudantePresenter {

	
	private Estudante estudanteModel;
	private EstudanteView estudanteView;
	
	public EstudantePresenter(Estudante estudanteModel, EstudanteView estudanteView){
		this.estudanteModel = estudanteModel;
		this.estudanteView = estudanteView;	
	}
	
	public void setEscola(Escola escola) {
		estudanteModel.setEscola(escola);
	}

	public String getEscola() {
		return estudanteModel.getEscola().getNome();
	}
	
	public String getNome(){
		return estudanteModel.getNome();
	}
	
	public String getAnoEscolar(){
		return Integer.toString(estudanteModel.getAnoEscolar());
	}
	
	
	public void printEstudanteDetalhe(){
		estudanteView.printProfessorDetalhe(this.getNome(), this.getEscola(), this.getAnoEscolar());	
	}
}
