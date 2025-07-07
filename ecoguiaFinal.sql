create table roles (
 id_rol Serial Primary key,
 Nombre Varchar(20),
 Descripcion TEXT
 );

 CREATE TABLE usuarios (
  id_usuario Serial PRIMARY KEY,
  nombre VARCHAR(50),
  ap_paterno VARCHAR(25),
  ap_materno VARCHAR(25),
  correo VARCHAR(100),
  contrasena VARCHAR(20),
  fecha_nacimiento DATE, 
  fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  total_recompensas INTEGER,
  id_rol INTEGER,
  CONSTRAINT fk_rol FOREIGN KEY (id_rol) REFERENCES Roles(id_rol)
 );

 CREATE TABLE retos(
 codigo SERIAL PRIMARY KEY,
 Titulo VARCHAR(30),
 descripcion TEXT
 );
 
 CREATE TABLE recompensas (
	codigo SERIAL PRIMARY KEY,
	Nombre VARCHAR(30),
	descripcion TEXT,
	clave_reto INTEGER REFERENCES retos(codigo)
 );

CREATE TABLE usuarios_recompensas (
    id_usuario INTEGER,
    id_recompensa INTEGER,
    fecha_canjeo DATE, 
	--esto permite que ambas sean una primary key y no se pueda insertar mas de una vez la misma combinacion
    PRIMARY KEY (id_usuario, id_recompensa),
	--aqui se declaran esas llaves primarias como foraneas
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_recompensa) REFERENCES recompensas(codigo)
);

CREATE TABLE usuarios_retos (
    id_usuario INTEGER,
    id_reto INTEGER,
    fecha_inicio DATE,
    fecha_fin DATE,
    PRIMARY KEY (id_usuario, id_reto),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_reto) REFERENCES retos(codigo)
);

CREATE TABLE contenido_educativo(
	codigo SERIAL PRIMARY KEY,
	titulo VARCHAR(25),
	descripcion TEXT,
	id_usuario_ce INTEGER,
	FOREIGN KEY (id_usuario_ce) REFERENCES usuarios(id_usuario)
);

CREATE TABLE publicaciones (
	clave_publicacion SERIAL PRIMARY KEY,
	titulo VARCHAR(30),
	contenido TEXT,
	id_usuario_p INTEGER,
	FOREIGN KEY (id_usuario_p) REFERENCES usuarios(id_usuario)
);

CREATE TABLE tipo_material_reciclable(
	id_tipoMaterial SERIAL PRIMARY KEY,
	nombre VARCHAR(40),
	descripcion TEXT,
	Tiempo_descomposicion INTEGER
);

CREATE TABLE material_reciclable(
	id_material SERIAL PRIMARY KEY,
	nombre VARCHAR(50),
	descripcion TEXT,
	tipo_reciclaje INTEGER,
	FOREIGN KEY (tipo_reciclaje) REFERENCES tipo_material_reciclable(id_tipoMaterial)
);

CREATE TABLE recicladoras(
	codigo_recicladora SERIAL PRIMARY KEY,
	nombre VARCHAR(50),
	propietario INTEGER,
	FOREIGN KEY (propietario) REFERENCES usuarios(id_usuario),
	calle VARCHAR(50),
	codigo_postal INTEGER,
	colonia VARCHAR(50),
	numero_int INTEGER,
	ciudad VARCHAR(30),
	numero_telefonico VARCHAR(20),
    aprobada BOOLEAN DEFAULT FALSE
);

CREATE TABLE puntos_reciclaje(
	id_punto SERIAL PRIMARY KEY,
	nombre VARCHAR(50),
	ubicacion TEXT,
	ciudad VARCHAR(30),
	horario_entrada TIME,
	horario_salida TIME,
	id_recicladora INTEGER,
	FOREIGN KEY (id_recicladora) REFERENCES recicladoras(codigo_recicladora)
);

CREATE TABLE entregas(
	id_entrega SERIAL PRIMARY KEY,
	fecha_entrega TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	id_usuario_e INTEGER,
	punto_entrega INTEGER,
    confirmada BOOLEAN DEFAULT FALSE,
	FOREIGN KEY (id_usuario_e) REFERENCES usuarios(id_usuario),
	FOREIGN KEY (punto_entrega) REFERENCES puntos_reciclaje(id_punto)
);


CREATE TABLE entrega_material_reciclado(
	id_entrega_material SERIAL PRIMARY KEY,
	id_entrega INTEGER,
	id_material INTEGER,
	cantidad INTEGER, 
	condiciones_entrega TEXT,
	FOREIGN KEY (id_entrega) REFERENCES entregas(id_entrega),  
	FOREIGN KEY (id_material) REFERENCES material_reciclable(id_material)
);

--roles
INSERT INTO roles (nombre, descripcion) VALUES ('Administrador', 'Gestiona el sistema y publica retos y contenido.');
INSERT INTO roles (nombre, descripcion) VALUES ('Usuario', 'Participa en retos, realiza entregas y publica comentarios.');
INSERT INTO roles (nombre, descripcion) VALUES ('Recicladora', 'Publica puntos de reciclaje y confirma entregas.');

--Usuarios
INSERT INTO usuarios (nombre, ap_paterno, ap_materno, correo, contrasena, fecha_nacimiento, total_recompensas, id_rol) VALUES 
('Ana', 'García', 'López', 'ana@correo.com', 'ana123', '1990-03-15', 5, 2),
('Carlos', 'Ramírez', 'Vega', 'carlos@correo.com', 'car123', '1988-07-22', 15, 2),
('Lucía', 'Fernández', 'Pérez', 'lucia@correo.com', 'lucia456', '1995-12-03', 0, 3),
('David', 'Torres', 'Hernández', 'admin@correo.com', 'admin123', '1985-05-30', 0, 1); 

--retos
INSERT INTO retos (titulo, descripcion) VALUES ('Recicla 5 botellas de plástico', 'Participa entregando al menos 5 botellas PET.');
INSERT INTO retos (titulo, descripcion) VALUES ('Limpieza de parques', 'Entrega residuos recolectados en parques locales.');
INSERT INTO retos (titulo, descripcion) VALUES ('Recicla vidrio', 'Lleva al menos 3 frascos de vidrio a un punto de reciclaje.');

--REcompensas
INSERT INTO recompensas (nombre, descripcion, clave_reto) VALUES 
('Descuento 10%', '10% en productos ecológicos', 1),
('EcoPuntos', 'Puntos acumulables para premios', 2),
('Bolsa reutilizable', 'Bolsa con diseño ecológico', 3);

--contenido educativo
INSERT INTO contenido_educativo (titulo, descripcion, id_usuario_ce) VALUES ('¿Por qué reciclar?', 'El reciclaje reduce la contaminación y ahorra recursos.', 4);
INSERT INTO contenido_educativo (titulo, descripcion, id_usuario_ce) VALUES ('Tipos de residuos', 'Conoce los residuos orgánicos, inorgánicos y peligrosos.', 4);
INSERT INTO contenido_educativo (titulo, descripcion, id_usuario_ce) VALUES ('Beneficios del reciclaje', 'Contribuye al medio ambiente y genera empleo.', 4);

--publicaciones
INSERT INTO publicaciones (titulo, contenido, id_usuario_p) VALUES ('Mi primer entrega', 'Entregué mis primeras 5 botellas y me siento genial.', 1);
INSERT INTO publicaciones (titulo, contenido, id_usuario_p) VALUES ('Limpieza en mi colonia', 'Nos organizamos para limpiar el parque y reciclamos mucho.', 2);
INSERT INTO publicaciones (titulo, contenido, id_usuario_p) VALUES ('Reciclar es fácil', 'Solo necesitas separar tus residuos y llevarlos al punto más cercano.', 1);

--tipo material
INSERT INTO tipo_material_reciclable (nombre, descripcion, tiempo_descomposicion) VALUES ('Plástico', 'Botellas, empaques, envolturas', 400);
INSERT INTO tipo_material_reciclable (nombre, descripcion, tiempo_descomposicion) VALUES ('Vidrio', 'Frascos, botellas de vidrio', 1000);
INSERT INTO tipo_material_reciclable (nombre, descripcion, tiempo_descomposicion) VALUES ('Papel y cartón', 'Revistas, cajas, hojas', 6);

--materiales
INSERT INTO material_reciclable (nombre, descripcion, tipo_reciclaje) VALUES ('Botella PET', 'Botella de plástico transparente', 1);
INSERT INTO material_reciclable (nombre, descripcion, tipo_reciclaje) VALUES ('Frasco de vidrio', 'Frasco de mayonesa reciclado', 2);
INSERT INTO material_reciclable (nombre, descripcion, tipo_reciclaje) VALUES ('Caja de cereal', 'Caja limpia de cartón', 3);

--recicladoras
INSERT INTO recicladoras (nombre, propietario, calle, codigo_postal, colonia, numero_int, ciudad, numero_telefonico, aprobada) 
VALUES ('Recicla Consciente', 3, 'Calle Verde', 12345, 'Ecobarrio', 100, 'Ciudad Verde', '1234567890', true);
INSERT INTO recicladoras (nombre, propietario, calle, codigo_postal, colonia, numero_int, ciudad, numero_telefonico, aprobada) 
VALUES ('Recicladora de Valle', 3, 'Valle de Guadalupe', 22251, 'Lomas altas', 100, 'Tijuana', '6645889932', false);


--puntos de reciclaje
INSERT INTO puntos_reciclaje (nombre, ubicacion, ciudad, horario_entrada, horario_salida, id_recicladora) VALUES ('Punto Ecológico Centro', 'https://maps.google.com/?q=19.4326,-99.1332', 'Ciudad Verde', '08:00', '16:00', 1);
INSERT INTO puntos_reciclaje (nombre, ubicacion, ciudad, horario_entrada, horario_salida, id_recicladora) VALUES ('Punto Norte', 'https://maps.google.com/?q=19.4526,-99.1532', 'Ciudad Verde', '09:00', '17:00', 1);
INSERT INTO puntos_reciclaje (nombre, ubicacion, ciudad, horario_entrada, horario_salida, id_recicladora) VALUES ('Punto Sur', 'https://maps.google.com/?q=19.4126,-99.1132', 'Ciudad Verde', '07:30', '15:30', 1);

--usuarios recompensas
INSERT INTO usuarios_recompensas (id_usuario, id_recompensa, fecha_canjeo)
VALUES 
(1, 1, '2025-06-10'),
(2, 2, '2025-06-11'),
(2, 3, '2025-06-15');

--usuarios retos
INSERT INTO usuarios_retos (id_usuario, id_reto, fecha_inicio, fecha_fin)
VALUES 
(1, 1, '2025-06-01', '2025-06-07'),
(2, 2, '2025-06-02', '2025-06-08'),
(1, 3, '2025-06-03', '2025-06-09');

--entregas
INSERT INTO entregas (id_usuario_e, punto_entrega, confirmada)
VALUES 
(1, 1, false),
(2, 2, true),
(2, 3, true);

--material_entregado
INSERT INTO entrega_material_reciclado (id_entrega, id_material, cantidad, condiciones_entrega)
VALUES 
(1, 1, 5, 'Botellas limpias y sin etiquetas.'),
(2, 2, 3, 'Vidrio limpio y sin tapa.'),
(3, 3, 7, 'Cartón seco y sin grasa.');

