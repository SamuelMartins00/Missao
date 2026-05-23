create database igreja_db;
use igreja_db;

create table agradecimentos (
	id_agr int auto_increment primary key,
    titulo_agr varchar(252),
    motivos_agr text,
    data_agr date
);

create table avisos (
	id_avi int auto_increment primary key,
    titulo_avi varchar(252),
    descricao_avi text,
    data_avi date
);

create table pedidos (
	id_ped int auto_increment primary key,
	nome_ped varchar(252),
	motivo_ped text,
	data_ped date
);

create table visitantes (
	id_vis int auto_increment primary key,
    nome_vis varchar(252),
    descricao_vis text,
    data_vis date
);	