-- Inserto los TiposProductos
INSERT INTO `gestionproductos2022db`.`sistemadecompra_tipoproducto`
	(`nombre`)
VALUES
	('Bebida'),
    ('Comida'),
	('Bazar'),
    ('Comestico')

-- Inserto los EstadosPedidos
INSERT INTO `gestionproductos2022db`.`sistemadecompra_estadopedido`
	(`nombre`)
VALUES
	('Creado'),
    ('Confirmado'),
	('Entregado'),
    ('Cancelado'),
    ('Cambio Fecha');

-- Inserto los Metodos de Pago
INSERT INTO `gestionproductos2022db`.`sistemadecompra_metododepago`
	(`nombre`)
VALUES
	('Uala'),
    ('Visa');

-- Inserto algunos usuarios

INSERT INTO `gestionproductos2022db`.`auth_user`
	(`password`, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
VALUES
	('monitor2022', 0, 'fedeproveedor', 'Federico', 'Liborio', 'federico-l-@hotmail.com', 0, 1, now()),
    ('monitor2022', 0, 'ricardocliente', 'Ricardo', 'Rocha', 'rocha_095@hotmail.com', 0, 1, now());