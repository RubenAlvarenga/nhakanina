/*INSERT INTO aranceles_concepto (id, concepto, estado, tipo_concepto_id)
VALUES 
*/ ( 7, 'Formación docente - Especialización - Profesionalización(anual)',  't',  1),
 ( 8, 'Capacitación - Actualización - Otros',  't',  1),
 ( 9, '[*FPO] Formación docente - Especialización - Profesionalización(anual)',  't',  1),
 (10, '[*FPO] Capacitación - Actualización - Otros',  't',  1),
 (11, 'Capacitación - Actualización - Otros',  't',  2),
 (12, 'Especialización Docente',  't',  2),
 (13, 'Tecnicaturas (presencial o virtual)',  't',  2),
 (14, 'Profesionalización',  't',  2),
 (15, 'Examen ordinario o primera instancia',  't',  3),
 (16, 'Examen complementario o segunda instancia',  't',  3),
 (17, 'Examen de Regularización o tercera instancia',  't',  3),
 (18, 'Examen mesa especial',  't',  3),
 (19, 'Examen extraordinario',  't',  3),
 (20, 'Examen de admisión (por asignatura/módulo)',  't',  3),
 (21, 'Expedición de Certificado de estudios (por documento) | Formación docente inicial -Profesionalizacion  -Tecnicatura (ED)',  't',  4),
 (22, 'Expedición de Certificado de estudios (por documento) | Especialización Docente',  't',  4),
 (23, 'Expedición de constancias varias (por documento)',  't',  4),
 (24, 'Autenticación de copias de certificados de estudios y títulos (por documento)',  't',  4),
 (25, 'Expedicion de copias autenticadas de Resoluciones | Primera Página',  't',  4),
 (26, 'Expedicion de copias autenticadas de Resoluciones | Páginas adicionales',  't',  4),
 (27, 'Reconocimiento de estudio, equiparación (por asignatura)',  't',  4),
 (28, 'Programas de estudios (por asignatura)',  't',  4),
 (29, 'Expedición de diplomas y títulos (cada uno) | Formación docente inicial, capacitaciones, otros',  't',  4),
 (30, 'Expedición de diplomas y títulos (cada uno) | Especialización docente y tecnicaturas',  't',  4),
 (31, 'Licenciatura en Educación por áreas específicas | Turnos mañana y tarde (semestral)',  't',  5),
 (32, 'Licenciatura en Educación por áreas específicas | Turno noche y dias sábados (semestral)',  't',  5),
 (33, 'Licenciatura en Educación por áreas específicas | [*FPO] Turnos mañana y tarde (semestral)',  't',  5),
 (34, 'Licenciatura en Educación por áreas específicas | [*FPO] Turno noche y dias sábados (semestral)',  't',  5),
 (35, 'Curso Probatorio de admisión (Semestral)',  't',  5),
 (36, 'Licenciatura en Ciencias de la Educación | Turnos mañana y tarde - lunes a viernes  (semestral)',  't',  5),
 (37, 'Licenciatura en Ciencias de la Educación | Cursos los dias sábados (semestral)',  't',  5),
 (38, 'Licenciatura en Ciencias de la Educación | Cursos de los dias sábados y del turno noche -inicia 2015 (semestral)',  't',  5),
 (39, 'Licenciatura en Educación articuladas con la formación docente inicial | Cursos de los turnos mañana y tarde - de lunes a viernes (semestral)',  't',  5),
 (40, 'Licenciatura en Educación articuladas con la formación docente inicial | Cursos los dias sábados (semestral)',  't',  5),
 (41, 'Licenciatura en Educación por áreas específicas',  't',  6),
 (42, 'Licenciatura en Ciencias de la Educación | Curso del turno noche - de lunes a viernes - (del curso anual)',  't',  6),
 (43, 'Licenciatura en Ciencias de la Educación | Cursos de los dias sábados (curso semestral)',  't',  6),
 (44, 'Licenciatura en Ciencias de la Educación | Licenciatura pos-docente (curso semestral)',  't',  6),
 (45, 'Examen ordinario o primera instancia',  't',  7),
 (46, 'Examen complementario o segunda instancia',  't',  7),
 (47, 'Examen de regularización o tercera instancia',  't',  7),
 (48, 'Examen mesa especial',  't',  7),
 (49, 'Examen extraordinario',  't',  7),
 (50, 'Examen de admisión (por asignatura o por módulo)',  't',  7),
 (51, 'Examen primera instancia - lengua extranjera',  't',  7),
 (52, 'Examen segunda instancia - lengua extranjera',  't',  7),
 (53, 'Examen tercera instancia - lengua extranjera',  't',  7),
 (54, 'Examen extraordinario - lengua extranjera',  't',  7),
 (55, 'Defensa de tesina',  't',  7),
 (56, 'Expedicion de certificados de estudios (por documento)',  't',  8),
 (57, 'Expedición de constancia (por documentos)',  't',  8),
 (58, 'Autenticación de fotocopias de Certificados de Estudios y Títulos (por documentos)',  't',  8),
 (59, 'Resolución por reconocimiento de estudios, equiparación (por asignatura)',  't',  8),
 (60, 'Pogramas de estudios (por asignatura o módulo)',  't',  8),
 (61, 'Expedición de títulos, diplomas y otros',  't',  8),
 (62, 'Tutoría',  't',  8),
 (63, 'Especialización',  't',  9),
 (64, 'Maestria',  't',  9),
 (65, 'Especialización',  't', 10),
 (66, 'Maestria',  't', 10),
 (67, 'Examen ordinario o de primera instancia | Especialización',  't', 11),
 (68, 'Examen ordinario o de primera instancia | Maestria',  't', 11),
 (69, 'Examen complementario o de segunda instancia | Especialización',  't', 11),
 (70, 'Examen complementario o de segunda instancia | Maestria',  't', 11),
 (71, 'Examen de regularización o de tercera instancia | Especialización',  't', 11),
 (72, 'Examen de regularización o de tercera instancia | Maestria',  't', 11),
 (73, 'Examen mesa especial y extraordinario | Especialización',  't', 11),
 (74, 'Examen mesa especial y extraordinario | Maestria',  't', 11),
 (75, 'Defensa de tesis de maestria',  't', 11),
 (76, 'Expedicion de certificado de estudios (por documento) | Especialización',  't', 12),
 (77, 'Expedicion de certificado de estudios (por documento) | Maestria',  't', 12),
 (78, 'Autenticacion de copias de certificados de estudios y títulos (por documento)',  't', 12),
 (79, 'Expedicion de constancias de cursos de postgrado (por documento)',  't', 12),
 (80, 'Resoluciones de reconocimiento de estudios, equiparacion y otros (por asiganaturas o módulos) | Especialización',  't', 12),
 (81, 'Resoluciones de reconocimiento de estudios, equiparacion y otros (por asiganaturas o módulos) | Maestria',  't', 12),
 (82, 'Programas de estudios (por asignatura o módulo) | Especialización',  't', 12),
 (83, 'Programas de estudios (por asignatura o módulo) | Maestria',  't', 12),
 (84, 'Expedicion de títulos y diplomas (por documento) | Especialización',  't', 12),
 (85, 'Expedicion de títulos y diplomas (por documento) | Maestria',  't', 12),
 (86, 'Salon Auditorio (por dia)',  't', 13),
 (87, 'Aulas de clase (por dia)',  't', 13),
 (88, 'Por cada equipo audiovisual (por dia)',  't', 13),
 (89, 'Multa por devolución tardía de materiales didacticos (por dia)',  't', 13),
 (90, 'Por reposicion de carnet de Biblioteca (cada uno)',  't', 13),
 (91, 'Venta de libros u otros materiales impresos que cuenta con el patrocinio del ISE | Folletos, revistas y otros materiales impresos',  't', 13),
 (92, 'Venta de libros u otros materiales impresos que cuenta con el patrocinio del ISE | Libros',  't', 13),
 (93, 'Consultorio médico Odontológico | Servicios de asistencia primaria (anual)',  't', 13),
 (94, 'Consultorio médico Odontológico | Consulta Odontológica (por consulta)',  't', 13),
 (95, 'Consultorio médico Odontológico | Extracciones', 't', 13);

