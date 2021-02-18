package com.cadastropessoas;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import com.cadastropessoas.Pessoa;

@Repository
public interface PessoaRepository extends CrudRepository<Pessoa, Long> {


}
