CODE = """
CREATE TABLE IF NOT EXISTS Clientes 
( 
 Id integer PRIMARY KEY, 
 Nome varchar(30) not null,  
 Cpf char(11) unique not null,  
 DataNasc date not null,  
 Email varchar(30),  
 Telefone varchar(13) not null,  

 Endereço varchar(200) 
);

CREATE TABLE IF NOT EXISTS Obras 
( 
 Id integer PRIMARY KEY,  
 Nome varchar(50) not null,  
 Status varchar(20) not null,  
 DataInicio date not null,  
 DataFim date not null,  
 Descrição varchar(200),  
 idClientes integer not null
);

CREATE TABLE IF NOT EXISTS Pessoa 
( 
 Id integer PRIMARY KEY,
 Nome varchar(50) not null, 
 Cpf char(11) unique not null,   
 DataNasc date not null,  
 Email varchar(50),
 Especialidade varchar(50) not null,    
 ValorPorHora float not null,  
 Telefone varchar(13) not null
);

CREATE TABLE IF NOT EXISTS Etapas 
( 
 Id integer PRIMARY KEY, 
 Nome varchar(50) not null,   
 Descrição varchar(200) not null,  
 Andamento varchar(200) not null,  
 DataFim date not null,  
 DataInicio date not null,  
 Anexo varchar(200),  
 idObras integer
);

CREATE TABLE IF NOT EXISTS Materiais 
( 
 Id integer PRIMARY KEY,  
 Nome varchar(50) not null,  
 Descrição varchar(200),
 Marca varchar(20) not null,
 Valor float not null
);

CREATE TABLE IF NOT EXISTS PessoaObra 
( 
 Id integer PRIMARY KEY,  
 IdObra integer not null,
 HorasExigidas integer not null,  
 HorasTrabalhadas integer not null,  
 ValorCobrado float not null
);

CREATE TABLE IF NOT EXISTS MateriaisEtapa 
( 
 Id integer PRIMARY KEY,  
 IdMaterial integer not null,
 Valor float not null,  
 Quantidade integer not null
);

ALTER TABLE Obras add foreign KEY (idClientes) REFERENCES Clientes (idClientes);
ALTER TABLE Etapas ADD FOREIGN KEY(idObras) REFERENCES Obras (idObras);
ALTER TABLE PessoaObra ADD FOREIGN KEY(IdPessoa) REFERENCES Pessoa (IdPessoa);
ALTER TABLE PessoaObra ADD FOREIGN KEY(IdObra) REFERENCES Obras (IdObra);
ALTER TABLE MateriaisEtapa ADD FOREIGN KEY(IdEtapa) REFERENCES Etapas (IdEtapa);
ALTER TABLE MateriaisEtapa ADD FOREIGN KEY(IdMaterial) REFERENCES Materiais (IdMaterial);
"""
