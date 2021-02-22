package Presenter;

import Model.Escola;
import View.EscolaView;

public class EscolaPresenter {
   
	private Escola escolaModel;
	private EscolaView escolaView;
	
	public EscolaPresenter(Escola escolaModel, EscolaView escolaView){
		this.escolaModel = escolaModel;
		this.escolaView = escolaView;
	}
	
	public String getNome() {
		return escolaModel.getNome();
	}

	public void setNome(String nome) {
		escolaModel.setNome(nome);
	}
	
	public void printEscolaDetalhe(){
		escolaView.printEscolaDetalhe(this.getNome());
	}
	
	
	
}
