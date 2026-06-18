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

create table usuarios (
    id      int auto_increment primary key,
    usuario varchar(50) not null unique,
    senha   char(64) not null,
    perfil  ENUM('admin', 'usuario') not null default 'usuario',
    criado  datetime default current_timestamp
);

insert into usuarios (usuario, senha, perfil) values ('admin', SHA2('admin', 256), 'admin');