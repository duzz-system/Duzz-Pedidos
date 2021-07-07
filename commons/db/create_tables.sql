use `duzz-pedidos`;

create table `tipos`(
    id_tipos int primary key auto_increment,
    nome varchar(45) not null
);

create table `tamanhos`(
    id_tamanhos int primary key auto_increment,
    nome varchar(45) not null
);

create table `adicionais`(
    id_adicionais int primary key auto_increment,
    nome varchar(45) not null
);

create table `status`(
    id_status int primary key auto_increment,
    nome varchar(45) not null
);

create table `lanches`(
    id_lanches int primary key auto_increment,
    nome varchar(45) not null,
    id_tipo int,
    id_tamanho int,

    CONSTRAINT fk_tipo FOREIGN KEY (id_tipo) REFERENCES tipos (id_tipos),
    CONSTRAINT fk_tamanho FOREIGN KEY (id_tamanho) REFERENCES tamanhos (id_tamanhos)
);

create table `pedidos`(
    id_pedido int primary key auto_increment,
    lanches varchar(120),
    id_adicionais int,
    cliente varchar(60),
    momento datetime,
    observacao varchar(120),
    id_status int,
    saida varchar(30),

    CONSTRAINT fk_lanches FOREIGN KEY (id_lanches) REFERENCES lanches (id_lanches),
    CONSTRAINT fk_adicionais FOREIGN KEY (id_adicionais) REFERENCES adicionais (id_adicionais),
    CONSTRAINT fk_status FOREIGN KEY (id_status) REFERENCES status (id_status)
);


