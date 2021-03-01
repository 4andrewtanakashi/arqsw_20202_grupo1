package Controller;

import View.DiretorView;

public class DiretorController{

	private Diretor diretorModel;
	private DiretorView diretorView;
	
	public DiretorController(DiretorView diretorView){
		this.diretorView = diretorView;	
	}
	
	public String getNome(){
		return "Algum nome";
	}
	
	public void printDiretorDetalhe(){
		diretorView.printDiretorDetalhe(this.getNome());	
	}
	
	
	
}
