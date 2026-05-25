create database igreja_db;
use igreja_db;

create table agradecimentos (
	id_agr int auto_increment primary key,
    nome_agr varchar(252),
    motivo_agr text,
    data_agr datetime default current_timestamp 
);

create table avisos (
	id_avi int auto_increment primary key,
    titulo_avi varchar(252),
    descricao_avi text,
    data_avi datetime default current_timestamp 
);

create table pedidos (
	id_ped int auto_increment primary key,
	nome_ped varchar(252),
	motivo_ped text,
	data_ped datetime default current_timestamp 
);

create table visitantes (
	id_vis int auto_increment primary key,
    nome_vis varchar(252),
    descricao_vis text,
    data_vis datetime default current_timestamp 
);	