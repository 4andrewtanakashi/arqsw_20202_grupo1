package Presenter;

import Model.Diretor;
import Model.Escola;
import View.DiretorView;

public class DiretorPresenter{

	private Diretor diretorModel;
	private DiretorView diretorView;
	
	public DiretorPresenter(Diretor diretorModel, DiretorView diretorView){
		this.diretorModel = diretorModel;
		this.diretorView = diretorView;	
	}
	
	public void setEscola(Escola escola) {
		diretorModel.setEscola(escola);
	}

	public String getEscola() {
		return diretorModel.getEscola().getNome();
	}
	
	public String getNome(){
		return diretorModel.getNome();
	}
	
	public void printDiretorDetalhe(){
		diretorView.printDiretorDetalhe(this.getNome(), this.getEscola());	
	}
	
	
	
}
