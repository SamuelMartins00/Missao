create table agradecimentos (
	id_agr        INT AUTO_INCREMENT PRIMARY KEY,
    nome_agr      VARCHAR(252),
    motivo_agr    TEXT,
    data_agr      DATETIME DEFAULT CURRENT_TIMESTAMP 
);

create table avisos (
	id_avi        INT AUTO_INCREMENT PRIMARY KEY,
    titulo_avi    VARCHAR(252),
    descricao_avi TEXT,
    data_avi      DATETIME DEFAULT CURRENT_TIMESTAMP 
);

create table pedidos (
	id_ped     INT AUTO_INCREMENT PRIMARY KEY,
	nome_ped   VARCHAR(252),
	motivo_ped TEXT,
	data_ped   DATETIME DEFAULT CURRENT_TIMESTAMP
);

create table visitantes (
	id_vis        INT AUTO_INCREMENT PRIMARY KEY,
    nome_vis      VARCHAR(252),
    descricao_vis TEXT,
    data_vis      DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE usuarios (
    id_usu  INT AUTO_INCREMENT PRIMARY KEY,
    usuario_usu VARCHAR(50)  NOT NULL UNIQUE,
    senha_usu   CHAR(64)     NOT NULL,           
    perfil_usu  ENUM('admin', 'usuario') NOT NULL DEFAULT 'usuario'
);