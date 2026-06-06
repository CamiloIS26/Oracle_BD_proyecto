-- Docker init: SYS ejecuta estas lineas automaticamente.
-- Ejecucion manual (SQL Developer como POLI001): omitir las 2 lineas ALTER SESSION siguientes.
ALTER SESSION SET CONTAINER = XEPDB1;
ALTER SESSION SET CURRENT_SCHEMA = POLI001;

CREATE INDEX idx_ciud_pais ON CIUDADES (ciud_pais_ID);
CREATE INDEX idx_localiz_ciudad ON LOCALIZACIONES (localiz_ciudad_ID);
CREATE INDEX idx_dpto_localiz ON DEPARTAMENTOS (dpto_localiz_ID);
CREATE INDEX idx_empl_cargo ON EMPLEADOS (empl_cargo_ID);
CREATE INDEX idx_empl_dpto ON EMPLEADOS (empl_dpto_ID);
CREATE INDEX idx_empl_localiz ON EMPLEADOS (empl_localiz_ID);
CREATE INDEX idx_empl_gerente ON EMPLEADOS (empl_gerente_ID);
CREATE INDEX idx_emphist_empl ON HISTORICO (emphist_empl_ID);
CREATE INDEX idx_emphist_cargo ON HISTORICO (emphist_cargo_ID);
CREATE INDEX idx_emphist_dpto ON HISTORICO (emphist_dpto_ID);

COMMIT;
