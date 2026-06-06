-- Docker init: SYS ejecuta estas lineas automaticamente.
-- Ejecucion manual (SQL Developer como POLI001): omitir las 2 lineas ALTER SESSION siguientes.
ALTER SESSION SET CONTAINER = XEPDB1;
ALTER SESSION SET CURRENT_SCHEMA = POLI001;

INSERT INTO PAISES (pais_nombre) VALUES ('Colombia');
INSERT INTO PAISES (pais_nombre) VALUES ('Chile');
INSERT INTO PAISES (pais_nombre) VALUES ('España');
INSERT INTO PAISES (pais_nombre) VALUES ('Argentina');
INSERT INTO PAISES (pais_nombre) VALUES ('Mexico');

INSERT INTO CARGOS (cargo_nombre, cargo_sueldo_minimo, cargo_sueldo_maximo)
VALUES ('Desarrolador web', 3000000, 10000000);
INSERT INTO CARGOS (cargo_nombre, cargo_sueldo_minimo, cargo_sueldo_maximo)
VALUES ('Contador', 2500000, 5000000);
INSERT INTO CARGOS (cargo_nombre, cargo_sueldo_minimo, cargo_sueldo_maximo)
VALUES ('Analista de sistemas', 2500000, 4500000);
INSERT INTO CARGOS (cargo_nombre, cargo_sueldo_minimo, cargo_sueldo_maximo)
VALUES ('Auxiliar administrativo', 1700000, 2500000);
INSERT INTO CARGOS (cargo_nombre, cargo_sueldo_minimo, cargo_sueldo_maximo)
VALUES ('Gerente de area', 5500000, 11500000);

INSERT INTO CIUDADES (ciud_pais_ID, ciud_nombre) VALUES (1, 'Bogota');
INSERT INTO CIUDADES (ciud_pais_ID, ciud_nombre) VALUES (2, 'Santiago de Chile');
INSERT INTO CIUDADES (ciud_pais_ID, ciud_nombre) VALUES (3, 'Madrid');
INSERT INTO CIUDADES (ciud_pais_ID, ciud_nombre) VALUES (4, 'Buenos Aires');
INSERT INTO CIUDADES (ciud_pais_ID, ciud_nombre) VALUES (5, 'Guadalajara');

INSERT INTO LOCALIZACIONES (localiz_ciudad_ID, localiz_direccion)
VALUES (1, 'Calle 72 #10-34, Chapinero');
INSERT INTO LOCALIZACIONES (localiz_ciudad_ID, localiz_direccion)
VALUES (2, 'Av. Providencia 1234, Providencia');
INSERT INTO LOCALIZACIONES (localiz_ciudad_ID, localiz_direccion)
VALUES (3, 'Calle de Alcala 45, Madrid Centro');
INSERT INTO LOCALIZACIONES (localiz_ciudad_ID, localiz_direccion)
VALUES (4, 'Av. Corrientes 1450, CABA');
INSERT INTO LOCALIZACIONES (localiz_ciudad_ID, localiz_direccion)
VALUES (5, 'Av. Vallarta 2501, Zona Minerva');

INSERT INTO DEPARTAMENTOS (dpto_localiz_ID, dpto_nombre) VALUES (1, 'Marketing');
INSERT INTO DEPARTAMENTOS (dpto_localiz_ID, dpto_nombre) VALUES (2, 'Desarrollo');
INSERT INTO DEPARTAMENTOS (dpto_localiz_ID, dpto_nombre) VALUES (3, 'Finanzas');
INSERT INTO DEPARTAMENTOS (dpto_localiz_ID, dpto_nombre) VALUES (4, 'Tecnologia');
INSERT INTO DEPARTAMENTOS (dpto_localiz_ID, dpto_nombre) VALUES (5, 'Administracion');

INSERT INTO EMPLEADOS (
    empl_cargo_ID, empl_gerente_ID, empl_dpto_ID, empl_localiz_ID,
    empl_primer_nombre, empl_segundo_nombre, empl_email,
    empl_fecha_nac, empl_sueldo, empl_comision
) VALUES (
    5, NULL, 2, 2, 'Esteban', 'Daniel', 'edaniel@gmail.com',
    DATE '1990-05-19', 9800000, 2.50
);

INSERT INTO EMPLEADOS (
    empl_cargo_ID, empl_gerente_ID, empl_dpto_ID, empl_localiz_ID,
    empl_primer_nombre, empl_segundo_nombre, empl_email,
    empl_fecha_nac, empl_sueldo, empl_comision
) VALUES (
    2, NULL, 3, 3, 'Sarah', 'Milena', 'smile@gmail.com',
    DATE '1995-01-28', 4500000, 1.00
);

INSERT INTO EMPLEADOS (
    empl_cargo_ID, empl_gerente_ID, empl_dpto_ID, empl_localiz_ID,
    empl_primer_nombre, empl_segundo_nombre, empl_email,
    empl_fecha_nac, empl_sueldo, empl_comision
) VALUES (
    4, NULL, 5, 5, 'Andrea', 'Alejandra', 'aaleja@gmail.com',
    DATE '2003-01-09', 2000000, NULL
);

INSERT INTO EMPLEADOS (
    empl_cargo_ID, empl_gerente_ID, empl_dpto_ID, empl_localiz_ID,
    empl_primer_nombre, empl_segundo_nombre, empl_email,
    empl_fecha_nac, empl_sueldo, empl_comision
) VALUES (
    1, 1, 2, 2, 'Luis', 'Fernando', 'lfernan@gmail.com',
    DATE '1998-06-12', 6500000, 1.50
);

INSERT INTO EMPLEADOS (
    empl_cargo_ID, empl_gerente_ID, empl_dpto_ID, empl_localiz_ID,
    empl_primer_nombre, empl_segundo_nombre, empl_email,
    empl_fecha_nac, empl_sueldo, empl_comision
) VALUES (
    3, 1, 4, 4, 'Juan', 'Felipe', 'jfelipe@gmail.com',
    DATE '2001-10-11', 3700000, NULL
);

INSERT INTO HISTORICO (emphist_empl_ID, emphist_cargo_ID, emphist_dpto_ID, emphist_fecha_retiro)
VALUES (2, 1, 2, DATE '2025-04-28');

INSERT INTO HISTORICO (emphist_empl_ID, emphist_cargo_ID, emphist_dpto_ID, emphist_fecha_retiro)
VALUES (3, 2, 3, DATE '2026-06-04');

INSERT INTO HISTORICO (emphist_empl_ID, emphist_cargo_ID, emphist_dpto_ID, emphist_fecha_retiro)
VALUES (4, 3, 4, DATE '2023-03-21');

INSERT INTO HISTORICO (emphist_empl_ID, emphist_cargo_ID, emphist_dpto_ID, emphist_fecha_retiro)
VALUES (5, 4, 5, DATE '2022-11-19');

INSERT INTO HISTORICO (emphist_empl_ID, emphist_cargo_ID, emphist_dpto_ID, emphist_fecha_retiro)
VALUES (1, 5, 2, DATE '2026-02-14');

COMMIT;
