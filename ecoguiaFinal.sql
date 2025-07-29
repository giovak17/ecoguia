
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

/* CREATE TABLE tipo_material_reciclable(
	id_tipoMaterial SERIAL PRIMARY KEY,
	nombre VARCHAR(40),
	descripcion TEXT,
	Tiempo_descomposicion INTEGER
); */
CREATE TABLE tipo_material_reciclable (
    id_tmr SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    tiempo_descomposicion VARCHAR(100)
);


CREATE TABLE material_reciclable(
	id_material SERIAL PRIMARY KEY,
	nombre VARCHAR(100),
	descripcion TEXT,
	tipo_reciclaje INTEGER,
	FOREIGN KEY (tipo_reciclaje) REFERENCES tipo_material_reciclable(id_tmr)
);

CREATE TABLE recicladoras(
	codigo_recicladora SERIAL PRIMARY KEY,
	nombre VARCHAR(100),
	propietario INTEGER,
	FOREIGN KEY (propietario) REFERENCES usuarios(id_usuario),
	calle VARCHAR(100),
	codigo_postal INTEGER,
	colonia VARCHAR(100),
	numero_int INTEGER,
	ciudad VARCHAR(100),
	numero_telefonico VARCHAR(20),
    aprobada BOOLEAN DEFAULT FALSE,
	detalles TEXT
);


/* CREATE TABLE puntos_reciclaje(
	id_punto SERIAL PRIMARY KEY,
	nombre VARCHAR(50),
	ubicacion TEXT,
	horario_entrada TIME,
	horario_salida TIME,
	id_recicladora INTEGER,
	FOREIGN KEY (id_recicladora) REFERENCES recicladoras(codigo_recicladora)
); */
CREATE TABLE puntos_reciclaje (
    id_punto SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    ubicacion TEXT,
    telefono VARCHAR(15),
    horario_entrada TIME,
    horario_salida TIME,
    extras VARCHAR(100),
    id_recicladora INTEGER,
    descripcion TEXT,
    longitud FLOAT,
    latitud FLOAT,
    FOREIGN KEY (id_recicladora) REFERENCES recicladoras(codigo_recicladora)
);

 --Nueva tabla 
 --Material_aceptado por los puntos de reciclaje
CREATE TABLE material_aceptado (
    id_ma SERIAL PRIMARY KEY,
    id_punto INTEGER NOT NULL,
    id_tipo_material INTEGER NOT NULL,
    FOREIGN KEY (id_punto) REFERENCES puntos_reciclaje(id_punto),
    FOREIGN KEY (id_tipo_material) REFERENCES tipo_material_reciclable(id_tmr)
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
('David', 'Torres', 'Hernández', 'admin@correo.com', 'admin123', '1985-05-30', 0, 1),
-- RECICLADORA
('Alan', 'Sanchez', 'Perez', 'recicladora@correo.com', 'rec123', '2000-03-30', 0, 3), 
('arath', 'porcayo', 'mercado', 'arath@gmail.com', 'arath07', '2000-03-30', 0, 3); 
----mas registros para recicladoras
INSERT INTO usuarios (nombre, ap_paterno, ap_materno, correo, contrasena, fecha_nacimiento, total_recompensas, id_rol) VALUES 

('Luis', 'Herrera', 'García', 'luis@correo.com', 'pass123', '1985-04-10', 0, 2),
('Marta', 'González', 'Sánchez', 'marta@correo.com', 'pass123', '1990-06-12', 0, 2),
('Eduardo', 'Sánchez', 'Martínez', 'eduardo@correo.com', 'pass123', '1988-02-25', 0, 2),
('Ana', 'Pérez', 'Ramírez', 'ana@correo.com', 'pass123', '1993-09-18',  0, 2),
('Carlos', 'Ramírez', 'Torres', 'carlos@correo.com', 'pass123', '1987-01-15', 0, 2),
('Laura', 'Mendoza', 'Flores', 'laura@correo.com', 'pass123', '1991-12-01',  0, 2),
('Roberto', 'Díaz', 'Moreno', 'roberto@correo.com', 'pass123', '1984-08-21', 0, 2),
('Fernanda', 'López', 'Jiménez', 'fernanda@correo.com', 'pass123', '1995-03-05',0, 2),
('Maria', 'perez', 'Fernandez', 'fernandez@correo.com', 'pass123', '1995-03-05',0, 2),
('Alejandro', 'Hernandez', 'Jimenez', 'ale@correo.com', 'pass123', '1995-03-05',0, 2),
('Frida', 'Arriaga', 'Valle', 'Frida@correo.com', 'pass123', '1995-03-05',0, 2),
('Juan', 'Lara', 'Mejia', 'juan@correo.com', 'pass123', '1985-04-10', 0, 1);

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
INSERT INTO contenido_educativo (titulo, descripcion, id_usuario_ce) VALUES ('¿Por qué reciclar?', 'El reciclaje reduce la contaminación y ahorra recursos.', 3);
INSERT INTO contenido_educativo (titulo, descripcion, id_usuario_ce) VALUES ('Tipos de residuos', 'Conoce los residuos orgánicos, inorgánicos y peligrosos.', 3);
INSERT INTO contenido_educativo (titulo, descripcion, id_usuario_ce) VALUES ('Beneficios del reciclaje', 'Contribuye al medio ambiente y genera empleo.', 3);

--publicaciones
INSERT INTO publicaciones (titulo, contenido, id_usuario_p) VALUES ('Mi primer entrega', 'Entregué mis primeras 5 botellas y me siento genial.', 4);
INSERT INTO publicaciones (titulo, contenido, id_usuario_p) VALUES ('Limpieza en mi colonia', 'Nos organizamos para limpiar el parque y reciclamos mucho.', 16);
INSERT INTO publicaciones (titulo, contenido, id_usuario_p) VALUES ('Reciclar es fácil', 'Solo necesitas separar tus residuos y llevarlos al punto más cercano.', 4);

--tipo material
INSERT INTO tipo_material_reciclable (nombre, descripcion, tiempo_descomposicion) VALUES
('Metales', 'Materiales como aluminio, acero y cobre comúnmente reciclados por su valor y durabilidad.', '200-500 años'),
('Electrónicos', 'Dispositivos eléctricos como celulares, computadoras y electrodomésticos, que contienen metales y componentes peligrosos.', '1 millón de años (componentes no biodegradables)'),
('Baterías', 'Acumuladores de energía como pilas y baterías recargables, que pueden contener sustancias tóxicas.', '100-1000 años'),
('Papel', 'Material de origen vegetal usado en impresión, embalaje y escritura. Altamente reciclable.', '2-6 semanas'),
('Cartón', 'Derivado del papel, utilizado comúnmente para embalajes. Biodegradable y reciclable.', '2 meses'),
('Plástico', 'Material sintético derivado del petróleo, muy usado en envases y productos diarios.', '100-1000 años'),
('Vidrio', 'Material inorgánico usado en botellas, frascos y ventanas. Reciclable infinitamente.', '1 millón de años'),
('Madera', 'Material orgánico usado en muebles y construcción. Biodegradable bajo condiciones naturales.', '1-3 años'),
('Materiales Peligrosos', 'Residuos con componentes tóxicos o reactivos como solventes, aceites, químicos industriales.', 'Depende del tipo, algunos son indefinidamente tóxicos');


--materiales
INSERT INTO material_reciclable(nombre, descripcion, tipo_reciclaje) VALUES
('Lata de aluminio', 'Envase metálico ligero y resistente, muy común en bebidas.', 1),
('Celular viejo', 'Dispositivo electrónico usado, contiene metales y componentes reciclables.', 2),
('Pila alcalina', 'Batería pequeña usada en dispositivos portátiles, contiene sustancias tóxicas.', 3),
('Periódico', 'Papel impreso usado para información diaria, reciclable fácilmente.', 4),
('Caja de cartón', 'Embalaje usado para transportar productos, biodegradable y reciclable.', 5),
('Botella de plástico PET', 'Envase plástico para bebidas, reciclable en muchas plantas.', 6),
('Frasco de vidrio', 'Envase de vidrio para alimentos o medicinas, reciclable infinitamente.', 7),
('Madera de pallets', 'Material usado en embalajes y construcción, biodegradable.', 8),
('Aceite usado', 'Residuos de aceites usados en motores, considerados material peligroso.', 9),
('Cargador electrónico', 'Accesorio para dispositivos, contiene componentes electrónicos reciclables.', 2);

--recicladoras
INSERT INTO recicladoras (nombre, calle, numero_int, colonia, codigo_postal, ciudad, numero_telefonico, aprobada, detalles, propietario) VALUES
('Eco Recycling', 'Blvd. Cucapah', 3674, 'Granjas Familiares del Matamoros', 22203, 'Tijuana', '6642882222', true, 'Empresa dedicada a la compra y venta de autopartes usadas, así como materiales ferrosos y no ferrosos.', 5),
('Solimar', NULL, NULL, 'Valle Del Sur 2', 22637, 'Tijuana', '6646376750', true, 'Centro de reciclaje enfocado en materiales domésticos y electrónicos, con servicio comunitario.', 6),
('Recuperada Baja', NULL, NULL, 'La Morita', 22245, 'Tijuana', '6648998948', true, 'Recicladora comprometida con la recuperación de materiales plásticos y metálicos.',7),
('Recolectora', 'De Los Ejidatarios', 705, 'Altiplano', 22204, 'Tijuana', '6646296668', true, 'Ofrece servicios de recolección y separación de residuos para empresas y particulares.',8),
('Metales De Baja California S de RL de CV', 'Loma Bonita 2', NULL, 'Lomas Verdes', 22105, 'Tijuana', '6649020896', true, 'Especializada en reciclaje industrial, con enfoque en metales y materiales de construcción.', 9),
('Materiales Expro', 'Pso De Los Taxistas', NULL, 'Infonavit la Mesa', 22226, 'Tijuana', '6644390337', true, 'Centro de acopio y separación de residuos sólidos urbanos y comerciales.', 10),
('Hyperplastics', 'And Vecinal', 10259, 'Quintas Campestres El Florido', 22710, 'Tijuana', '6644390337', true, 'Recicladora especializada en plásticos de alta y baja densidad.',11),
('Ewally', 'Río Colorado', 9470, 'Marron', 22015, 'Tijuana', '6645697984', true, 'Planta recicladora que promueve la economía circular a través del reciclaje tecnológico.', 12),
('Corporativo Ambiental', 'Asfalto', 10, 'Río Tijuana 3a. Etapa', 22225, 'Tijuana', '6646259387', true, 'Corporación dedicada al manejo integral de residuos peligrosos y no peligrosos.', 1),
('Centro De Acopio', 'Ruta Mariano Matamoros', 9234, 'Mariano Matamoros', 22234, 'Tijuana', '6644090457', true, 'Centro comunitario que recibe residuos reciclables como papel, cartón, plástico y vidrio.', 2),
('Arjamex', 'Buena Vista', 3471, 'Anexa 20 de Noviembre', 22100, 'Tijuana', '6646222290', true, 'Empresa recicladora que ofrece soluciones para el manejo adecuado de residuos sólidos.', 13),
('Bansus Internacional Recovery De Mexico S de RL de CV', 'Blvd. Díaz Ordaz', 12415, 'El Paraiso', 22106, 'Tijuana', '6646891141', true, 'Recicladora internacional que se especializa en recuperación de metales y componentes electrónicos.', 14),
-- ('Alan Recycling S.A de C.V', 'Camino Vecinal', 10152, 'Colonia Valle Redondo', 22226, 'Tijuana', '6646268035', true, 'Empresa local dedicada al reciclaje de materiales industriales, plásticos y metales.', 15);
('Alan Recycling S.A de C.V', 'Camino Vecinal', 10152, 'Colonia Valle Redondo', 22226, 'Tijuana', '6646268035', true, 'Empresa local dedicada al reciclaje de materiales industriales, plásticos y metales.', 5);


--puntos de reciclaje
INSERT INTO puntos_reciclaje(nombre, ubicacion, telefono, horario_entrada, horario_salida, extras, id_recicladora, descripcion, longitud, latitud) VALUES
('eco recycling', 'Blvd. Cucapah 3674, Ex-Ejido Mariano Matamoros, Granjas Familiares del Matamoros, 22203 Tijuana, B.C.', '6642882222', '07:30', '05:00', 'compra material', 1, 'Centro especializado en compra y reciclaje de materiales metálicos y electrónicos, con atención personalizada y horarios amplios.', -116.8854, 32.51389),
('solimar', 'San Antonio De Los Buenos, Valle Del Sur 2, 22637 Tijuana, B.C.', '6646376750', '09:00', '05:00', NULL, 2, 'Punto de reciclaje que recibe diversos materiales reciclables, incluyendo plásticos y papel, con servicio de acopio para la comunidad.', -117.03533, 32.47562),
('recuperada baJa JK', 'La Morita, 22245 Tijuana, B.C.', '6648998948', '08:00', '05:00', 'compra material', 3, 'Recicladora dedicada a la compra de materiales reciclables como metales y plásticos, con atención amable y ubicación accesible.', -116.83386, 32.47272),
('RECICLADORA DL', 'De Los Ejidatarios 705, Altiplano, 22204 Tijuana, B.C.', '6645733410', '07:00', '05:00', NULL, 4, 'Centro de acopio para materiales reciclables, con horarios flexibles para facilitar la entrega de residuos.', -116.84913, 32.52241),
('RECICLADORA LA CATORCE', 'Blvd. Héctor Terán Terán 2636, Jardín Dorado, 22200 Tijuana, B.C.', '6642486048', '08:00', '05:00', 'centro de acopio', 4, 'Centro de acopio y reciclaje que atiende principalmente materiales metálicos y electrónicos, con servicio para empresas y particulares.', -116.890142, 32.52310668),
('RECICLADORA AB', 'Madrid 27, Libramiento, 22225 Tijuana, B.C.', '6641036875', '08:00', '05:00', NULL, 4, 'Recicladora que recibe materiales variados, enfocados en metales y papel, ofreciendo precios competitivos y servicio rápido.', -116.9232966, 32.4727198),
('Metales De Baja California S de RL de CV', 'Loma Bonita 2, La Mesa, Lomas Verdes, 22105 Tijuana, B.C.', '6646296668', '08:00', '05:00', 'compra material', 5, 'Empresa dedicada a la compra y reciclaje de metales, con amplia experiencia en el manejo responsable de residuos.', -116.9381068, 32.4764405),
('Materiales expro', 'Pso De Los Taxistas, Infonavit la Mesa, 22226 Tijuana, B.C.', '6649020896', '08:00', '05:00', 'compra material', 6, 'Punto de compra de materiales reciclables, principalmente metales y plásticos, con atención personalizada.', -116.9561285, 32.50119538),
('Hyperplastics Tijuana', 'And Vecinal 10259 Colonia Valle Redondo, Quintas Campestres El Florido, 22710 Tijuana, B.C.', '6644390337', '08:00', '05:00', NULL, 7, 'Recicladora especializada en plásticos industriales y domésticos, ofreciendo soluciones para la reutilización y reciclaje.', -116.789598, 32.46683387),
('Ewally', 'Río Colorado 9470, Marron, 22015 Tijuana, B.C.', '6645697984', '08:00', '05:00', NULL, 8, 'Centro de reciclaje para materiales diversos, incluyendo plásticos y electrónicos, con atención rápida y eficiente.', -117.023251, 32.5233953),
('Eco Recycling Salvatierra', 'Libramiento Flores Magón 3507, Salvatierra, La Cueva, 22607 Tijuana, B.C.', '6647009539', '08:00', '05:00', 'compra material', 1, 'Sucursal de Eco Recycling con servicios de compra y acopio de materiales reciclables, enfocada en metales y plásticos.', -117.0763087, 32.48400476),
('Eco Recycling Tecolote', 'Calle Miguel Hidalgo 7951, El Tecolote, 22644 Tijuana, B.C.', '6646260202', '08:00', '05:00', 'compra material', 1, 'Sucursal de Eco Recycling con atención para compra de materiales reciclables, con horario accesible para clientes.', -116.9930286, 32.453755),
('Eco Recycling Terrazas Del Valle', 'Blvd. Olivas, Terrazas Del Valle, 22246 Tijuana, B.C.', '6642882224', '08:00', '05:00', 'compra material', 1, 'Sucursal de Eco Recycling enfocada en la compra de materiales reciclables, atendiendo a la comunidad local.', -116.8244498, 32.47903528),
('Corporativo Ambiental', 'Meseta Del Chema, Asfalto 10, Río Tijuana 3a. Etapa, 22225 Tijuana, B.C.', '6646259387', '08:00', '05:00', NULL, 9, 'Empresa dedicada al manejo ambiental y reciclaje, con servicios para recepción de materiales peligrosos y reciclables.', -116.9033501, 32.45732652),
('Centro De Acopio Lopez', 'Ruta Mariano Matamoros 9234, Mariano Matamoros, 22234 Tijuana, B.C.', '6644090457', '08:00', '05:00', 'compra material', 10, 'Centro de acopio que recibe materiales reciclables y ofrece compra de residuos, con atención rápida y eficiente.', -116.8813571, 32.47421541),
('Arjamex 20 De Noviembre', 'Buena Vista 3471, Anexa 20 de Noviembre, 22100 Tijuana, B.C.', '6646222290', '08:00', '05:00', 'compra material', 11, 'Punto de compra y reciclaje de materiales variados, incluyendo metales, plásticos y papel.', -116.9814881, 32.51390265),
('Bansus Internacional Recovery De Mexico S de RL de CV', 'Blvd. Díaz Ordaz #12415, El paraiso, 22106 Tijuana, B.C.', '6646891141', '08:00', '05:00', 'compra material', 12, 'Empresa especializada en recuperación y reciclaje de materiales industriales y metálicos.', -116.9311974, 32.46987916),
('Alan Recycling S.A de C.V', 'Camino Vecinal, Valle Redondo 10152, Colonia, 22226 Tijuana, B.C.', '6646268035', '08:00', '05:00', 'centro de acopio', 13, 'Centro de acopio y reciclaje con enfoque en materiales metálicos y electrónicos, ofreciendo servicios a empresas y particulares.', -116.7867065, 32.46492804),
('Eco Recycling La Presa', 'Derecho De Vía 22123, La Presa, Paseo Los Reyes, 22123 Tijuana, B.C.', '6649726601', '08:00', '05:00', 'compra material', 1, 'Sucursal de Eco Recycling que ofrece compra y acopio de materiales reciclables, con atención eficiente y precios competitivos.', -116.9221419, 32.45755048),
('Eco Recycling Las Torres', 'C. Granizo 660, Las Torres, 22470 Tijuana, B.C.', '6642506329', '08:00', '05:00', 'compra material', 1, 'Sucursal de Eco Recycling que recibe diversos materiales reciclables, enfocada en servicio comunitario.', -116.9001046, 32.54278122),
('Eco Recycling Maclovio', 'Esq. Ave. Jaime Pujol y Calle 2 De Julio, Valle Redondo, 22720 Tijuana, B.C.', '6649032241', '08:00', '05:00', 'compra material', 1, 'Sucursal de Eco Recycling que ofrece servicios de compra y reciclaje de materiales, con atención personalizada.', -116.7945691, 32.47187047),
('Eco Recycling Matamoros', 'Benito Juárez 349, Planicie, Ejido Matamoros, 22204 Tijuana, B.C.', '6641034106', '08:00', '05:00', 'compra material', 1, 'Sucursal de Eco Recycling especializada en compra y reciclaje de materiales, con amplia experiencia en la región.', -116.862128, 32.52240863);


--material aceptado 
INSERT INTO material_aceptado (id_punto, id_tipo_material) VALUES
(1, 1),  -- eco recycling acepta Metales
(1, 2),  -- eco recycling acepta Electrónicos
(1, 6),  -- eco recycling acepta Plástico
(1, 7),  -- eco recycling acepta Vidrio
(2, 4),  -- solimar acepta Papel
(2, 5),  -- solimar acepta Cartón
(3, 1),  -- recuperada baJa JK acepta Metales
(3, 6),  -- recuperada baJa JK acepta Plástico
(4, 1),  -- RECOLECTPRA DL acepta Metales
(5, 1),  -- RECICLADORA LA CATORCE acepta Metales
(5, 9),  -- RECICLADORA LA CATORCE acepta Materiales Peligrosos
(6, 4),  -- RECICLADORA AB acepta Papel
(6, 5),  -- RECICLADORA AB acepta Cartón
(7, 1),  -- Metales De Baja California acepta Metales
(8, 6),  -- Materiales expro acepta Plástico
(9, 6),  -- Hyperplastics acepta Plástico
(10, 7), -- Ewally acepta Vidrio
(11, 1), -- Eco Recycling Salvatierra acepta Metales
(11, 6); -- Eco Recycling Salvatierra acepta Plástico

--usuarios recompensas
INSERT INTO usuarios_recompensas (id_usuario, id_recompensa, fecha_canjeo)
VALUES 
(4, 1, '2025-06-10'),
(4, 2, '2025-06-11'),
(16, 3, '2025-06-15');

--usuarios retos
INSERT INTO usuarios_retos (id_usuario, id_reto, fecha_inicio, fecha_fin)
VALUES 
(4, 1, '2025-06-01', '2025-06-07'),
(16, 2, '2025-06-02', '2025-06-08'),
(4, 3, '2025-06-03', '2025-06-09');

--entregas
INSERT INTO entregas (id_usuario_e, punto_entrega, confirmada)
VALUES 
(16, 13, false),
(4, 13, true),
(4, 3, true);

--material_entregado
INSERT INTO entrega_material_reciclado (id_entrega, id_material, cantidad, condiciones_entrega)
VALUES 
(1, 1, 5, 'Botellas limpias y sin etiquetas.'),
(2, 2, 3, 'Vidrio limpio y sin tapa.'),
(3, 3, 7, 'Cartón seco y sin grasa.');

