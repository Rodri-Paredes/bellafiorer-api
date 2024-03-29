CREATE DATABASE IF NOT EXISTS bellafiore;

CREATE TABLE cliente (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(30),
    direccion VARCHAR(50),
    celular VARCHAR(20),
    email VARCHAR(50),
    creado_por INT NOT NULL,
    actualizado_por INT DEFAULT NULL,
    ultima_actualizacion TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    es_activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE producto (
    id_producto INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(20),
    descripcion TEXT,
    precio FLOAT(7,2),
    stock INT,
	creado_por INT NOT NULL,
    actualizado_por INT DEFAULT NULL,
    ultima_actualizacion TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
	es_activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE usuario (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(20),
    username VARCHAR(20) UNIQUE,
    password VARCHAR(50),
    rol ENUM ("admin","vendedor"),
    creado_por INT NOT NULL,
    actualizado_por INT DEFAULT NULL,
    ultima_actualizacion TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
	es_activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE orden (
    id_orden INT PRIMARY KEY AUTO_INCREMENT,
    monto_total FLOAT(7,2) NOT NULL DEFAULT 0,
    estado ENUM("pedido","reserva","vendido","cancelado"),
    id_usuario INT,
    id_cliente INT,
	creado_por INT NOT NULL,
    actualizado_por INT DEFAULT NULL,
    ultima_actualizacion TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    es_activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);
CREATE TABLE detalle (
    id_detalle INT PRIMARY KEY AUTO_INCREMENT,
    id_orden INT,
    id_producto INT,
    cantidad INT,
    precio_unitario FLOAT(7,2) NOT NULL DEFAULT 0,
    subtotal FLOAT(7,2) NOT NULL DEFAULT 0,
    creado_por INT NOT NULL,
    actualizado_por INT DEFAULT NULL,
    ultima_actualizacion TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
	es_activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_orden) REFERENCES orden(id_orden),
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
);
CREATE TABLE orden_cancelado (
    id_orden INT PRIMARY KEY,
    motivo_cancelacion VARCHAR(50),
    FOREIGN KEY (id_orden) REFERENCES orden(id_orden)
);
CREATE TABLE orden_pedido (
    id_orden  INT PRIMARY KEY,
    fecha_entrega DATETIME,
    FOREIGN KEY (id_orden) REFERENCES orden(id_orden)
);
CREATE TABLE orden_reserva (
    id_orden INT  PRIMARY KEY,
     monto_pagado float(7,2) NOT NULL DEFAULT 0,
     metodo_pago ENUM('EFECTIVO', 'QR', 'TRANSFERENCIA'),
    FOREIGN KEY (id_orden) REFERENCES orden(id_orden)
);
CREATE TABLE orden_vendido (
    id_orden INT   PRIMARY KEY,
    fecha_venta  TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
    saldo_cancelado float(7,2) NOT NULL DEFAULT 0,
    metodo_pago ENUM('EFECTIVO', 'QR', 'TRANSFERENCIA'),
    FOREIGN KEY (id_orden) REFERENCES orden(id_orden)
);
