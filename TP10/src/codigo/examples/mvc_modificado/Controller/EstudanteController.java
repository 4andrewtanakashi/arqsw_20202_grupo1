package Controller;

import Model.Escola;
import Model.Estudante;


public class EstudanteController {

	
	private Estudante estudanteModel;
	
	public EstudanteController(Estudante estudanteModel){
		this.estudanteModel = estudanteModel;
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
}
