create database igreja_db;
use igreja_db;

create table graca (
	id_gra int auto_increment primary key,
    nome_gra varchar(252),
    motivos_gra text,
    data_gra date
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

create table vistantes (
	id_vis int auto_increment primary key,
    nome_vis varchar(252),
    descricao_vis text,
    data_vis date
);	