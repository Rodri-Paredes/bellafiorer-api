CREATE DATABASE IF NOT EXISTS bellafiore;

CREATE TABLE cliente (
     id_cliente INT PRIMARY KEY AUTO_INCREMENT,
     nombre VARCHAR(30),
     direccion VARCHAR(50),
     celular VARCHAR(20),
     creado_modificado_por VARCHAR(20),
     ultima_actualizacion TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
     es_activo BOOLEAN DEFAULT TRUE
);
CREATE TABLE producto (
    id_producto INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(20),
    descripcion TEXT,
    precio FLOAT(7,2),
    stock INT,
	creado_modificado_por VARCHAR(20),
    ultima_actualizacion TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
	es_activo BOOLEAN DEFAULT TRUE
);
CREATE TABLE usuario (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(20),
    nombre_usuario VARCHAR(20) UNIQUE,
    password VARCHAR(50),
    rol ENUM ("admin","vendedor"),
    creado_modificado_por VARCHAR(20),
    ultima_actualizacion TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
	es_activo BOOLEAN DEFAULT TRUE
);
CREATE TABLE orden (
    id_orden INT PRIMARY KEY AUTO_INCREMENT,
    fecha_entrega DATETIME,
    monto_reserva INT,
    monto_total FLOAT(7,2) NOT NULL DEFAULT 0,
    estado ENUM("pedido","reserva","vendido","cancelado"),
    id_usuario INT,
    id_cliente INT,
	creado_modificado_por VARCHAR(20),
    ultima_actualizacion TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    es_activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);
CREATE TABLE detalle (
    id_detalle INT PRIMARY KEY AUTO_INCREMENT,
    id_orden INT,
    id_producto INT,
    cantidad INT,
    precio_unitario FLOAT(7,2) NOT NULL DEFAULT 0,
    FOREIGN KEY (id_orden) REFERENCES orden(id_orden),
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto),
    creado_modificado_por VARCHAR(20),
    ultima_actualizacion TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
	es_activo BOOLEAN DEFAULT TRUE
)
