-- SQLBook: Code
/*  martinez gonzalez jesus antonio */
create table roles (
 id_rol Serial Primary key,
 Nombre Varchar(20),
 Descripcion TEXT
 );

/* Kevin Giovanni Barraza Andalon  */
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
  puntos INTEGER DEFAULT 0,
  id_rol INTEGER,
  CONSTRAINT fk_rol FOREIGN KEY (id_rol) REFERENCES Roles(id_rol)
 );

/* */
 CREATE TABLE retos(
	codigo SERIAL PRIMARY KEY,
	Titulo VARCHAR(30),
	descripcion TEXT
 );
 
 /* tambien modificada en caso de que este mal la modifican y avisan */
  /* America lara */
 
 CREATE TABLE recompensas (
	codigo SERIAL PRIMARY KEY,
    nombre VARCHAR(30),
    descripcion TEXT,
    clave_reto INTEGER,
    puntos_requeridos INTEGER DEFAULT 50,
    FOREIGN KEY (clave_reto) REFERENCES retos(codigo)
 );

/*  */
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

/*  */
CREATE TABLE usuarios_retos (
    id_usuario INTEGER,
    id_reto INTEGER,
    fecha_inicio DATE,
    fecha_fin DATE,
    PRIMARY KEY (id_usuario, id_reto),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_reto) REFERENCES retos(codigo)
);

--America Lara
CREATE TABLE contenido_educativo (
    codigo SERIAL PRIMARY KEY,
    titulo VARCHAR(100),
    descripcion TEXT,
    id_usuario_ce INTEGER,
    imagen VARCHAR(100),
    videos VARCHAR(200),
    video_local VARCHAR(100),
    FOREIGN KEY (id_usuario_ce) REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);
--------Campos nuevos a la tabla Contenido_educativo
ALTER TABLE contenido_educativo
ADD COLUMN imagen VARCHAR(1000);--------Se guarda solo la ruta del archivo, por eso usamos VARCHAR(
ALTER TABLE contenido_educativo
ADD COLUMN videos VARCHAR(200);

ALTER TABLE contenido_educativo
ADD COLUMN video_local VARCHAR(1000);

/* Martinez GonzaLez Jesus Antonio  */
CREATE TABLE publicaciones (
	clave_publicacion SERIAL PRIMARY KEY,
	titulo VARCHAR(30),
	contenido TEXT,
	id_usuario_p INTEGER,
	FOREIGN KEY (id_usuario_p) REFERENCES usuarios(id_usuario)
);
/*  */
CREATE TABLE tipo_material_reciclable (
    id_tmr SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,	
    tiempo_descomposicion VARCHAR(100),
    imagen VARCHAR(100)
);

/*  */
CREATE TABLE material_reciclable(
	id_material SERIAL PRIMARY KEY,
	nombre VARCHAR(100),
	descripcion TEXT,
	tipo_reciclaje INTEGER,
	FOREIGN KEY (tipo_reciclaje) REFERENCES tipo_material_reciclable(id_tmr)
);

/* Arista Pérez Graciela */
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

/* Arista Pérez Graciela */
CREATE TABLE puntos_reciclaje (
    id_punto SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    ubicacion TEXT,
    telefono VARCHAR(15),
    horario_entrada TIME,
    horario_salida TIME,
    extras VARCHAR(100),
	ciudad VARCHAR(50),
    id_recicladora INTEGER,
    descripcion TEXT,
    longitud FLOAT,
    latitud FLOAT,
    FOREIGN KEY (id_recicladora) REFERENCES recicladoras(codigo_recicladora)
);
/* Arista Pérez Graciela */
 --Nueva tabla M:N 
 --Material aceptado por los puntos de reciclaje
CREATE TABLE material_aceptado (
    id_ma SERIAL PRIMARY KEY,
    id_punto INTEGER NOT NULL,
    id_tipo_material INTEGER NOT NULL,
    FOREIGN KEY (id_punto) REFERENCES puntos_reciclaje(id_punto),
    FOREIGN KEY (id_tipo_material) REFERENCES tipo_material_reciclable(id_tmr)
);

/* Kevin Giovanni Barraza Andalon */
CREATE TABLE entregas(
	id_entrega SERIAL PRIMARY KEY,
	fecha_entrega TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	id_usuario_e INTEGER,
	punto_entrega INTEGER,
    confirmada BOOLEAN DEFAULT FALSE,
	FOREIGN KEY (id_usuario_e) REFERENCES usuarios(id_usuario),
	FOREIGN KEY (punto_entrega) REFERENCES puntos_reciclaje(id_punto)
);

/*  */
CREATE TABLE entrega_material_reciclado(
	id_entrega_material SERIAL PRIMARY KEY,
	id_entrega INTEGER,
	id_material INTEGER,
	cantidad INTEGER, 
	condiciones_entrega TEXT,
	FOREIGN KEY (id_entrega) REFERENCES entregas(id_entrega),  
	FOREIGN KEY (id_material) REFERENCES material_reciclable(id_material)
);

-- FUNCIONES
CREATE OR REPLACE FUNCTION sumar_puntos_entrega()
RETURNS TRIGGER AS $$
DECLARE
    usuario_id INTEGER;
    puntos_actuales INTEGER;
    recompensa RECORD;
BEGIN
    -- Obtener el ID del usuario que hizo la entrega
    SELECT id_usuario_e INTO usuario_id
    FROM entregas
    WHERE id_entrega = NEW.id_entrega;

    -- Sumar los puntos entregados al usuario
    UPDATE usuarios
    SET puntos = COALESCE(puntos, 0) + COALESCE(NEW.cantidad, 0)
    WHERE id_usuario = usuario_id;

    -- Obtener el total actualizado de puntos
    SELECT puntos INTO puntos_actuales
    FROM usuarios
    WHERE id_usuario = usuario_id;

    -- Buscar recompensas alcanzables que el usuario aún no tiene
    FOR recompensa IN
        SELECT codigo
        FROM recompensas r
        WHERE r.puntos_requeridos <= puntos_actuales
          AND NOT EXISTS (
              SELECT 1
              FROM usuarios_recompensas ur
              WHERE ur.id_usuario = usuario_id
                AND ur.id_recompensa = r.codigo
          )
    LOOP
        -- Insertar la recompensa alcanzada
        INSERT INTO usuarios_recompensas (id_usuario, id_recompensa, fecha_canjeo)
        VALUES (usuario_id, recompensa.codigo, CURRENT_DATE);
    END LOOP;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

---
CREATE OR REPLACE FUNCTION restar_puntos_entrega()
RETURNS TRIGGER AS $$
DECLARE
    usuario_id INTEGER;
BEGIN
    -- Obtener el ID del usuario que hizo la entrega
    SELECT id_usuario_e INTO usuario_id
    FROM entregas
    WHERE id_entrega = OLD.id_entrega;

    -- Restar la cantidad entregada de los puntos del usuario
    UPDATE usuarios
    SET puntos = GREATEST(0, COALESCE(puntos, 0) - COALESCE(OLD.cantidad, 0))
    WHERE id_usuario = usuario_id;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- TRIGGERS
CREATE TRIGGER trg_sumar_puntos
AFTER INSERT ON entrega_material_reciclado
FOR EACH ROW
EXECUTE FUNCTION sumar_puntos_entrega();

---
CREATE TRIGGER trg_restar_puntos
BEFORE DELETE ON entrega_material_reciclado
FOR EACH ROW
EXECUTE FUNCTION restar_puntos_entrega();

--roles
INSERT INTO roles (nombre, descripcion) VALUES 
('Administrador', 'Gestiona el sistema y publica retos y contenido.'),
('Usuario', 'Participa en retos, realiza entregas y publica comentarios.'),
('Recicladora', 'Publica puntos de reciclaje y confirma entregas.');

--Usuarios
INSERT INTO usuarios (nombre, ap_paterno, ap_materno, correo, contrasena, fecha_nacimiento, total_recompensas, id_rol) VALUES 
--Administrador
('David', 'Torres', 'Hernández', 'admin@correo.com', 'admin123', '1985-05-30', 0, 1),
-- RECICLADORA
('Beatriz', 'Navarro', 'Salas', 'recicladora1@correo.com', 'rec321', '2000-03-30', 0, 3), 
('Isabel', 'Luna', 'Domínguez', 'isabel@correo.com', 'isa789', '1995-12-03', 0, 3),
('Manuel', 'Ortega', 'Fuentes', 'manuel@correo.com', 'man789', '1988-07-22', 15, 3),
('Raúl', 'Pineda', 'Castillo', 'raul@correo.com', 'raul456', '1985-04-10', 0, 3),
('Rosa', 'Camacho', 'Nieto', 'rosa@correo.com', 'rosa123', '1990-06-12', 0, 3),
('Tomás', 'Vargas', 'Silva', 'tomas@correo.com', 'tom654', '1988-02-25', 0, 3),
('Gabriela', 'Campos', 'Mejía', 'gabriela@correo.com', 'gab321', '1993-09-18', 0, 3),
('Andrés', 'Velasco', 'Reyes', 'andres@correo.com', 'and123', '1987-01-15', 0, 3),
('Cecilia', 'Rosales', 'Soto', 'cecilia@correo.com', 'cec987', '1991-12-01', 0, 3),
('Jorge', 'Medina', 'Acosta', 'jorge@correo.com', 'jor456', '1984-08-21', 0, 3),
('Verónica', 'Suárez', 'Ríos', 'veronica@correo.com', 'vero321', '1995-03-05', 0, 3),
--RECICLADOR 
('Patricia', 'Gallardo', 'Cruz', 'patricia@correo.com', 'pat123', '1990-03-15', 0, 2),
('Héctor', 'Núñez', 'Serrano', 'hector@correo.com', 'hec456', '1988-07-22', 0, 2),
('Ricardo', 'Peña', 'Aguilar', 'ricardo@correo.com', 'ric321', '1985-04-10', 0, 2),
('Leticia', 'Carrillo', 'Bautista', 'leticia@correo.com', 'let789', '1990-06-12', 0, 2),
('Samuel', 'Cortés', 'Valdez', 'samuel@correo.com', 'sam654', '1988-02-25', 0, 2),
('Daniela', 'Ramos', 'Molina', 'daniela@correo.com', 'dan111', '1993-09-18', 0, 2),
('Ernesto', 'Blanco', 'Esquivel', 'ernesto@correo.com', 'ern789', '1987-01-15', 0, 2);

--retos
INSERT INTO retos (titulo, descripcion) VALUES 
('Recicla 5 botellas de plástico', 'Participa entregando al menos 5 botellas PET.'),
('Limpieza de parques', 'Entrega residuos recolectados en parques locales.'),
('Recicla vidrio', 'Lleva al menos 3 frascos de vidrio a un punto de reciclaje.');

--Recompensas
INSERT INTO recompensas (nombre, descripcion, clave_reto) VALUES 
('Descuento 10%', '10% en productos ecológicos', 1),
('EcoPuntos', 'Puntos acumulables para premios', 2),
('Bolsa reutilizable', 'Bolsa con diseño ecológico', 3);

-- Recompensas con puntos
INSERT INTO recompensas (nombre, descripcion, clave_reto, puntos_requeridos) VALUES 
('Medalla Bronce', 'Medalla por alcanzar 100 puntos reciclando.', NULL, 100),
('Medalla Plata', 'Medalla por alcanzar 200 puntos reciclando.', NULL, 200),
('Medalla Oro', 'Medalla por alcanzar 300 puntos reciclando.', NULL, 300);

--contenido educativo
INSERT INTO contenido_educativo (titulo, descripcion, id_usuario_ce, imagen, videos, video_local) VALUES
('Beneficios del reciclaje',
 'El reciclaje ayuda a reducir la cantidad de residuos en el planeta, conservando recursos naturales y energía.',
 1,null,
 'https://www.youtube.com/watch?v=5q2HSdgO7CA',
 null),
('Cómo Separar los Residuos',
 'Aprende a clasificar correctamente los residuos en orgánicos, reciclables e inorgánicos no reciclables.',
 1,
 null,
 'https://www.youtube.com/watch?v=yBpxKb_rCyk',
 null),
('Tipos de Plástico y su Reciclaje',
 'Conoce los diferentes tipos de plástico y cómo se deben reciclar según su clasificación.',
 1,
 null,
 'https://www.youtube.com/watch?v=0hRmAeqQTB8',
 null),
('Reciclaje de Papel y Cartón',
 'Consejos prácticos para reciclar papel y cartón en casa o en la oficina.',
 1,
 null,
 'https://www.youtube.com/watch?v=sx1QLGGR5Gk',
 null),
('Reciclaje en tu Comunidad',
 'Descubre cómo puedes participar en programas de reciclaje comunitarios y su impacto positivo.',
 1,
 null,
 'https://www.youtube.com/watch?v=cvakvfXj0KE',
 null);

--publicaciones
INSERT INTO publicaciones (titulo, contenido, id_usuario_p) VALUES 
('Mi primer entrega', 'Entregué mis primeras 5 botellas y me siento genial.', 16),
('Limpieza en mi casa', 'Hice limpieza profunda en mi casa y decidi llevarlo a un lugar donde pueda servir más.', 17),
('Reciclar es fácil', 'Solo necesitas separar tus residuos y llevarlos al punto más cercano.', 18);

--tipo material
INSERT INTO tipo_material_reciclable (nombre, descripcion, tiempo_descomposicion, imagen) VALUES
('Metales', 'Materiales como aluminio, acero y cobre comúnmente reciclados por su valor y durabilidad.', '200-500 años', 'clasificacion/metal_AOeT0PQ.jpeg' ),
('Electrónicos', 'Dispositivos eléctricos como celulares, computadoras y electrodomésticos, que contienen metales y componentes peligrosos.', '1 millón de años (componentes no biodegradables)', 'clasificacion/electronico.jpeg'),
('Baterías', 'Acumuladores de energía como pilas y baterías recargables, que pueden contener sustancias tóxicas.', '100-1000 años','clasificacion/baterias.jpeg'),
('Papel', 'Material de origen vegetal usado en impresión, embalaje y escritura. Altamente reciclable.', '2-6 semanas','clasificacion/papel.jpeg'),
('Cartón', 'Derivado del papel, utilizado comúnmente para embalajes. Biodegradable y reciclable.', '2 meses','clasificacion/carton_Z3Nsfg5.jpeg'),
('Plástico', 'Material sintético derivado del petróleo, muy usado en envases y productos diarios.', '100-1000 años','clasificacion/plastico.jpeg'),
('Vidrio', 'Material inorgánico usado en botellas, frascos y ventanas. Reciclable infinitamente.', '1 millón de años','clasificacion/vidrio.jpeg'),
('Madera', 'Material orgánico usado en muebles y construcción. Biodegradable bajo condiciones naturales.', '1-3 años','clasificacion/madera.jpeg'),
('Materiales Peligrosos', 'Residuos con componentes tóxicos o reactivos como solventes, aceites, químicos industriales.', 'Depende del tipo, algunos son indefinidamente tóxicos','clasificacion/materialpeligroso.jpeg');


--materiales
INSERT INTO material_reciclable(nombre, descripcion, tipo_reciclaje) VALUES
('Lata de aluminio', 'Envase metálico ligero y resistente, muy común en bebidas.', 1),
('Celular viejo', 'Dispositivo electrónico usado, contiene metales y componentes reciclables.', 2),
('Caja de cartón', 'Batería pequeña usada en dispositivos portátiles, contiene sustancias tóxicas.', 3),
('Periódico', 'Papel impreso usado para información diaria, reciclable fácilmente.', 4),
('Caja de cartón', 'Embalaje usado para transportar productos, biodegradable y reciclable.', 5),
('Botella de plástico PET', 'Envase plástico para bebidas, reciclable en muchas plantas.', 6),
('Frasco de vidrio', 'Envase de vidrio para alimentos o medicinas, reciclable infinitamente.', 7),
('Madera de pallets', 'Material usado en embalajes y construcción, biodegradable.', 8),
('Aceite usado', 'Residuos de aceites usados en motores, considerados material peligroso.', 9),
('Cargador electrónico', 'Accesorio para dispositivos, contiene componentes electrónicos reciclables.', 2);


--recicladoras
INSERT INTO recicladoras (nombre, calle, numero_int, colonia, codigo_postal, ciudad, numero_telefonico, aprobada, detalles, propietario) VALUES
('Eco Recycling', 'Blvd. Cucapah', 3674, 'Granjas Familiares del Matamoros', 22203, 'Tijuana', '6642882222', true, 'Empresa dedicada a la compra y venta de autopartes usadas, así como materiales ferrosos y no ferrosos.', 2),
('Solimar', NULL, NULL, 'Valle Del Sur 2', 22637, 'Tijuana', '6646376750', true, 'Centro de reciclaje enfocado en materiales domésticos y electrónicos, con servicio comunitario.', 3),
('Recuperada Baja', NULL, NULL, 'La Morita', 22245, 'Tijuana', '6648998948', true, 'Recicladora comprometida con la recuperación de materiales plásticos y metálicos.',4),
('Recolectora', 'De Los Ejidatarios', 705, 'Altiplano', 22204, 'Tijuana', '6646296668', true, 'Ofrece servicios de recolección y separación de residuos para empresas y particulares.',4),
('Metales De Baja California S de RL de CV', 'Loma Bonita 2', NULL, 'Lomas Verdes', 22105, 'Tijuana', '6649020896', true, 'Especializada en reciclaje industrial, con enfoque en metales y materiales de construcción.', 5),
('Materiales Expro', 'Pso De Los Taxistas', NULL, 'Infonavit la Mesa', 22226, 'Tijuana', '6644390337', true, 'Centro de acopio y separación de residuos sólidos urbanos y comerciales.', 6),
('Hyperplastics', 'And Vecinal', 10259, 'Quintas Campestres El Florido', 22710, 'Tijuana', '6644390337', true, 'Recicladora especializada en plásticos de alta y baja densidad.',7),
('Ewally', 'Río Colorado', 9470, 'Marron', 22015, 'Tijuana', '6645697984', true, 'Planta recicladora que promueve la economía circular a través del reciclaje tecnológico.', 8),
('Corporativo Ambiental', 'Asfalto', 10, 'Río Tijuana 3a. Etapa', 22225, 'Tijuana', '6646259387', true, 'Corporación dedicada al manejo integral de residuos peligrosos y no peligrosos.', 9),
('Centro De Acopio', 'Ruta Mariano Matamoros', 9234, 'Mariano Matamoros', 22234, 'Tijuana', '6644090457', true, 'Centro comunitario que recibe residuos reciclables como papel, cartón, plástico y vidrio.', 10),
('Arjamex', 'Buena Vista', 3471, 'Anexa 20 de Noviembre', 22100, 'Tijuana', '6646222290', true, 'Empresa recicladora que ofrece soluciones para el manejo adecuado de residuos sólidos.', 11),
('Bansus Internacional Recovery De Mexico S de RL de CV', 'Blvd. Díaz Ordaz', 12415, 'El Paraiso', 22106, 'Tijuana', '6646891141', true, 'Recicladora internacional que se especializa en recuperación de metales y componentes electrónicos.', 11),
('Alan Recycling S.A de C.V', 'Camino Vecinal', 10152, 'Colonia Valle Redondo', 22226, 'Tijuana', '6646268035', true, 'Empresa local dedicada al reciclaje de materiales industriales, plásticos y metales.', 12);


--puntos de reciclaje
INSERT INTO puntos_reciclaje(nombre, ubicacion, telefono, horario_entrada, horario_salida, extras, id_recicladora, descripcion, longitud, latitud,  ciudad) VALUES
('Eco recycling', 'Blvd. Cucapah 3674, Ex-Ejido Mariano Matamoros, Granjas Familiares del Matamoros, 22203 Tijuana, B.C.', '6642882222', '07:30', '05:00', 'compra material', 1, 'Centro especializado en compra y reciclaje de materiales metálicos y electrónicos, con atención personalizada y horarios amplios.', -116.8854, 32.51389, 'Tijuana'),
('Solimar', 'San Antonio De Los Buenos, Valle Del Sur 2, 22637 Tijuana, B.C.', '6646376750', '09:00', '05:00', NULL, 2, 'Punto de reciclaje que recibe diversos materiales reciclables, incluyendo plásticos y papel, con servicio de acopio para la comunidad.', -117.03533, 32.47562, 'Tijuana'),
('Recuperada baJa JK', 'La Morita, 22245 Tijuana, B.C.', '6648998948', '08:00', '05:00', 'compra material', 3, 'Recicladora dedicada a la compra de materiales reciclables como metales y plásticos, con atención amable y ubicación accesible.', -116.83386, 32.47272, 'Tijuana'),
('RECICLADORA DL', 'De Los Ejidatarios 705, Altiplano, 22204 Tijuana, B.C.', '6645733410', '07:00', '05:00', NULL, 4, 'Centro de acopio para materiales reciclables, con horarios flexibles para facilitar la entrega de residuos.', -116.84913, 32.52241 , 'Tijuana'),
('RECICLADORA LA CATORCE', 'Blvd. Héctor Terán Terán 2636, Jardín Dorado, 22200 Tijuana, B.C.', '6642486048', '08:00', '05:00', 'centro de acopio', 4, 'Centro de acopio y reciclaje que atiende principalmente materiales metálicos y electrónicos, con servicio para empresas y particulares.', -116.890142, 32.52310668, 'Tijuana'),
('RECICLADORA AB', 'Madrid 27, Libramiento, 22225 Tijuana, B.C.', '6641036875', '08:00', '05:00', NULL, 4, 'Recicladora que recibe materiales variados, enfocados en metales y papel, ofreciendo precios competitivos y servicio rápido.', -116.9232966, 32.4727198, 'Tijuana'),
('Metales De Baja California S de RL de CV', 'Loma Bonita 2, La Mesa, Lomas Verdes, 22105 Tijuana, B.C.', '6646296668', '08:00', '05:00', 'compra material', 5, 'Empresa dedicada a la compra y reciclaje de metales, con amplia experiencia en el manejo responsable de residuos.', -116.9381068, 32.4764405, 'Tijuana'),
('Materiales expro', 'Pso De Los Taxistas, Infonavit la Mesa, 22226 Tijuana, B.C.', '6649020896', '08:00', '05:00', 'compra material', 6, 'Punto de compra de materiales reciclables, principalmente metales y plásticos, con atención personalizada.', -116.9561285, 32.50119538, 'Tijuana'),
('Hyperplastics Tijuana', 'And Vecinal 10259 Colonia Valle Redondo, Quintas Campestres El Florido, 22710 Tijuana, B.C.', '6644390337', '08:00', '05:00', NULL, 7, 'Recicladora especializada en plásticos industriales y domésticos, ofreciendo soluciones para la reutilización y reciclaje.', -116.789598, 32.46683387, 'Tijuana'),
('Ewally', 'Río Colorado 9470, Marron, 22015 Tijuana, B.C.', '6645697984', '08:00', '05:00', NULL, 8, 'Centro de reciclaje para materiales diversos, incluyendo plásticos y electrónicos, con atención rápida y eficiente.', -117.023251, 32.5233953, 'Tijuana'),
('Eco Recycling Salvatierra', 'Libramiento Flores Magón 3507, Salvatierra, La Cueva, 22607 Tijuana, B.C.', '6647009539', '08:00', '05:00', 'compra material', 1, 'Sucursal de Eco Recycling con servicios de compra y acopio de materiales reciclables, enfocada en metales y plásticos.', -117.0763087, 32.48400476, 'Tijuana'),
('Eco Recycling Tecolote', 'Calle Miguel Hidalgo 7951, El Tecolote, 22644 Tijuana, B.C.', '6646260202', '08:00', '05:00', 'compra material', 1, 'Sucursal de Eco Recycling con atención para compra de materiales reciclables, con horario accesible para clientes.', -116.9930286, 32.453755, 'Tijuana'),
('Eco Recycling Terrazas Del Valle', 'Blvd. Olivas, Terrazas Del Valle, 22246 Tijuana, B.C.', '6642882224', '08:00', '05:00', 'compra material', 1, 'Sucursal de Eco Recycling enfocada en la compra de materiales reciclables, atendiendo a la comunidad local.', -116.8244498, 32.47903528, 'Tijuana'),
('Corporativo Ambiental', 'Meseta Del Chema, Asfalto 10, Río Tijuana 3a. Etapa, 22225 Tijuana, B.C.', '6646259387', '08:00', '05:00', NULL, 9, 'Empresa dedicada al manejo ambiental y reciclaje, con servicios para recepción de materiales peligrosos y reciclables.', -116.9033501, 32.45732652, 'Tijuana'),
('Centro De Acopio Lopez', 'Ruta Mariano Matamoros 9234, Mariano Matamoros, 22234 Tijuana, B.C.', '6644090457', '08:00', '05:00', 'compra material', 10, 'Centro de acopio que recibe materiales reciclables y ofrece compra de residuos, con atención rápida y eficiente.', -116.8813571, 32.47421541, 'Tijuana'),
('Arjamex 20 De Noviembre', 'Buena Vista 3471, Anexa 20 de Noviembre, 22100 Tijuana, B.C.', '6646222290', '08:00', '05:00', 'compra material', 11, 'Punto de compra y reciclaje de materiales variados, incluyendo metales, plásticos y papel.', -116.9814881, 32.51390265, 'Tijuana'),
('Bansus Internacional Recovery De Mexico S de RL de CV', 'Blvd. Díaz Ordaz #12415, El paraiso, 22106 Tijuana, B.C.', '6646891141', '08:00', '05:00', 'compra material', 12, 'Empresa especializada en recuperación y reciclaje de materiales industriales y metálicos.', -116.9311974, 32.46987916, 'Tijuana'),
('Alan Recycling S.A de C.V', 'Camino Vecinal, Valle Redondo 10152, Colonia, 22226 Tijuana, B.C.', '6646268035', '08:00', '05:00', 'centro de acopio', 13, 'Centro de acopio y reciclaje con enfoque en materiales metálicos y electrónicos, ofreciendo servicios a empresas y particulares.', -116.7867065, 32.46492804, 'Tijuana'),
('Eco Recycling La Presa', 'Derecho De Vía 22123, La Presa, Paseo Los Reyes, 22123 Tijuana, B.C.', '6649726601', '08:00', '05:00', 'compra material', 1, 'Sucursal de Eco Recycling que ofrece compra y acopio de materiales reciclables, con atención eficiente y precios competitivos.', -116.9221419, 32.45755048, 'Tijuana'),
('Eco Recycling Las Torres', 'C. Granizo 660, Las Torres, 22470 Tijuana, B.C.', '6642506329', '08:00', '05:00', 'compra material', 1, 'Sucursal de Eco Recycling que recibe diversos materiales reciclables, enfocada en servicio comunitario.', -116.9001046, 32.54278122, 'Tijuana'),
('Eco Recycling Maclovio', 'Esq. Ave. Jaime Pujol y Calle 2 De Julio, Valle Redondo, 22720 Tijuana, B.C.', '6649032241', '08:00', '05:00', 'compra material', 1, 'Sucursal de Eco Recycling que ofrece servicios de compra y reciclaje de materiales, con atención personalizada.', -116.7945691, 32.47187047, 'Tijuana'),
('Eco Recycling Matamoros', 'Benito Juárez 349, Planicie, Ejido Matamoros, 22204 Tijuana, B.C.', '6641034106', '08:00', '05:00', 'compra material', 1, 'Sucursal de Eco Recycling especializada en compra y reciclaje de materiales, con amplia experiencia en la región.', -116.862128, 32.52240863, 'Tijuana');

--Material aceptado por los puntos de reciclaje
INSERT INTO material_aceptado (id_punto, id_tipo_material) VALUES
(2, 6),
(2, 7),
(4, 4),
(4, 5),
(4, 6),
(5, 2),
(5, 6),
(6, 1),
(6, 6),
(7, 6),
(7, 2),
(7, 7),
(8, 1),
(8, 5),
(8, 4),
(9, 1),
(9, 2), 
(9, 5),
(10, 1), 
(10, 6),
(10, 2),
(11, 2),
(11, 7),
(12, 1),
(12, 4),
(12, 5),
(12, 6),
(13, 1),
(13, 4),
(13, 5),
(13, 6),
(14, 2),
(14, 4),
(14, 6),
(14, 9),
(15, 1),
(15, 4),
(15, 5),
(15, 6),
(16, 1),
(16, 4),
(16, 6),
(16, 7),
(17, 1),
(17, 2),
(17, 5),
(17, 6),
(18, 1),
(18, 2),
(18, 6),
(18, 7),
(19, 2),
(19, 7),
(20, 2),
(20, 5),
(20, 6),
(20, 9),
(21, 1),
(21, 5),
(21, 6),
(21, 7),
(22, 1),
(22, 4),
(22, 5),
(22, 6),
(1, 2),
(1, 4),
(1, 6),
(1, 7);

--entregas
INSERT INTO entregas (id_usuario_e, punto_entrega, confirmada)
VALUES 
(16, 1, true),
(17, 2, true),
(18, 3, true),
(13, 4, true);

--material_entregado
INSERT INTO entrega_material_reciclado (id_entrega, id_material, cantidad, condiciones_entrega)
VALUES 
(1, 1, 5, 'Botellas limpias y sin etiquetas.'),
(1, 1, 25, 'Botellas con etiquetas.'),
(2, 2, 1, 'Celular quebrado y sin bateria.'),
(2, 1, 15, 'Botellas con tapa.'),
(3, 3, 3, 'Cartón seco y sin grasa.'),
(4, 1, 35, 'Botellas limpias y sin etiquetas.'),
(4, 3, 80, 'Cartón seco y sin grasa.'),
(4, 2, 5, 'Celular sin pantalla y sin bateria.');

--usuarios retos
INSERT INTO usuarios_retos (id_usuario, id_reto, fecha_inicio, fecha_fin)
VALUES 
(16, 1, '2025-06-01', '2025-06-10'),
(17, 2, '2025-06-02', '2025-06-11'),
(18, 3, '2025-06-03', '2025-06-15');

-- Dejar comentado, las recompensas se calcularan automaticamente segun los puntos del usuario
--usuarios recompensas
-- INSERT INTO usuarios_recompensas (id_usuario, id_recompensa, fecha_canjeo)
-- VALUES 
-- (16, 1, '2025-06-10'),
-- (17, 2, '2025-06-11'),
-- (18, 3, '2025-06-15');