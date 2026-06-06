-- Docker init: SYS ejecuta estas lineas automaticamente.
-- Ejecucion manual (SQL Developer como POLI001): omitir las 2 lineas ALTER SESSION siguientes.
ALTER SESSION SET CONTAINER = XEPDB1;
ALTER SESSION SET CURRENT_SCHEMA = POLI001;

CREATE TABLE PAISES (
    pais_ID       NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    pais_nombre   VARCHAR2(50) NOT NULL
);

CREATE TABLE CIUDADES (
    ciud_ID       NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ciud_pais_ID  NUMBER NOT NULL,
    ciud_nombre   VARCHAR2(50) NOT NULL,
    CONSTRAINT ciud_pais_fk FOREIGN KEY (ciud_pais_ID) REFERENCES PAISES (pais_ID)
);

CREATE TABLE LOCALIZACIONES (
    localiz_ID         NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    localiz_ciudad_ID  NUMBER NOT NULL,
    localiz_direccion  VARCHAR2(100) NOT NULL,
    CONSTRAINT localiz_ciudad_fk FOREIGN KEY (localiz_ciudad_ID) REFERENCES CIUDADES (ciud_ID)
);

CREATE TABLE DEPARTAMENTOS (
    dpto_ID          NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    dpto_localiz_ID  NUMBER NOT NULL,
    dpto_nombre      VARCHAR2(30) NOT NULL,
    CONSTRAINT dpto_localiz_fk FOREIGN KEY (dpto_localiz_ID) REFERENCES LOCALIZACIONES (localiz_ID)
);

CREATE TABLE CARGOS (
    cargo_ID             NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    cargo_nombre         VARCHAR2(50) NOT NULL,
    cargo_sueldo_minimo  NUMBER(11, 2) NOT NULL,
    cargo_sueldo_maximo  NUMBER(11, 2) NOT NULL
);

CREATE TABLE EMPLEADOS (
    empl_ID             NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    empl_cargo_ID       NUMBER NOT NULL,
    empl_gerente_ID     NUMBER,
    empl_dpto_ID        NUMBER NOT NULL,
    empl_localiz_ID     NUMBER NOT NULL,
    empl_primer_nombre  VARCHAR2(50) NOT NULL,
    empl_segundo_nombre VARCHAR2(50),
    empl_email          VARCHAR2(100) NOT NULL,
    empl_fecha_nac      DATE NOT NULL,
    empl_sueldo         NUMBER(11, 2) NOT NULL,
    empl_comision       NUMBER(5, 2),
    empl_activo         CHAR(1) DEFAULT 'S' NOT NULL,
    CONSTRAINT empl_cargo_fk FOREIGN KEY (empl_cargo_ID) REFERENCES CARGOS (cargo_ID),
    CONSTRAINT empl_gerente_fk FOREIGN KEY (empl_gerente_ID) REFERENCES EMPLEADOS (empl_ID),
    CONSTRAINT empl_dpto_fk FOREIGN KEY (empl_dpto_ID) REFERENCES DEPARTAMENTOS (dpto_ID),
    CONSTRAINT empl_localiz_fk FOREIGN KEY (empl_localiz_ID) REFERENCES LOCALIZACIONES (localiz_ID),
    CONSTRAINT empl_activo_chk CHECK (empl_activo IN ('S', 'N'))
);

CREATE TABLE HISTORICO (
    emphist_ID           NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    emphist_empl_ID      NUMBER NOT NULL,
    emphist_cargo_ID     NUMBER NOT NULL,
    emphist_dpto_ID      NUMBER NOT NULL,
    emphist_fecha_retiro DATE,
    CONSTRAINT emphist_empl_fk FOREIGN KEY (emphist_empl_ID) REFERENCES EMPLEADOS (empl_ID),
    CONSTRAINT emphist_cargo_fk FOREIGN KEY (emphist_cargo_ID) REFERENCES CARGOS (cargo_ID),
    CONSTRAINT emphist_dpto_fk FOREIGN KEY (emphist_dpto_ID) REFERENCES DEPARTAMENTOS (dpto_ID)
);

COMMIT;
