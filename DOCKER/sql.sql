USE EMPRESA;

CREATE TABLE adm_users (
    id int AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(60) NOT NULL,
    cargo VARCHAR(60) NOT NULL,
    email VARCHAR(50) NOT NULL,
    senha VARCHAR(15) NOT NULL,
    data_criacao DATE NOT NULL DEFAULT (CURRENT_DATE),
    ultimo_login DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP 
);

INSERT INTO adm_users (nome,cargo,email,senha) VALUES ('Denilson', 'Administrador', 'email@email.com','Senha123');

CREATE TABLE produtos (

    id int AUTO_INCREMENT PRIMARY KEY,
    produto VARCHAR(60) NOT NULL,
    quantidade int(5) NOT NULL,
    imagem VARCHAR(60) NOT NULL,
    validade DATE NOT NULL
);

CREATE TABLE funcionarios (
    id int AUTO_INCREMENT PRIMARY KEY,
    funcionario VARCHAR(60) NOT NULL,
    cargo VARCHAR(60) NOT NULL,
    data_contratacao DATE NOT NULL,
    salario DECIMAL(10,2) NOT NULL,
    foto1 VARCHAR(60) NOT NULL,
    foto2 VARCHAR(60) NOT NULL,
    foto3 VARCHAR(60) NOT NULL,
    foto4 VARCHAR(60) NOT NULL,
    foto5 VARCHAR(60) NOT NULL
);
