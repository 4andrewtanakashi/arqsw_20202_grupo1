package View.SpecificView;

import Model.Escola;

public class EscolaView {


	public void printEscolaDetalhe(String nome, Escola escola){
		System.out.println("\n -- DADOS DA ESCOLA --");
		System.out.println("Enviado: " + nome);
		System.out.println("Nome da Escola: " + escola.getNome());

	}
}
