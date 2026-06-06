# Oracle_BD_proyecto

Base de datos de Recursos Humanos (Entrega 2 — Semana 5) con Oracle Database XE 21c en Docker.

## Requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- (Opcional) [Oracle SQL Developer](https://www.oracle.com/database/technologies/appdev/sqldeveloper-landing.html)

En Mac con Apple Silicon (M1/M2/M3) la imagen corre en emulación `linux/amd64` (ya configurado en `docker-compose.yml`). La primera subida puede tardar varios minutos.

## Inicio rápido con Docker

```bash
cp .env.example .env
docker compose up -d
docker compose logs -f oracle-xe
```

Esperar hasta que el contenedor reporte estado `healthy` (puede tardar 2–5 minutos la primera vez).

Los scripts en `scripts/init/` se ejecutan automáticamente **solo en la primera inicialización** del volumen:

1. `01_tablespace_usuario.sql` — tablespace `DATOS`, usuario `POLI001`
2. `02_creacion_tablas.sql` — 7 tablas del modelo RRHH
3. `03_insercion_datos.sql` — 5 registros por tabla
4. `04_indices.sql` — índices sobre claves foráneas

### Reiniciar desde cero

```bash
docker compose down -v
docker compose up -d
```

## Conexión

| Parámetro | Valor |
|-----------|-------|
| Host | `localhost` |
| Puerto | `1521` (configurable en `.env`) |
| Service name | `XEPDB1` |
| Usuario aplicación | `POLI001` |
| Contraseña | `Poli001Pass123` |
| Usuario admin | `SYSTEM` |
| Contraseña admin | valor de `ORACLE_PASSWORD` en `.env` |

**SQL Developer:** nueva conexión → tipo `Basic` → hostname `localhost`, port `1521`, service name `XEPDB1`, usuario `POLI001`.

**sqlplus desde el contenedor:**

```bash
docker exec -it oracle-bd-proyecto sqlplus POLI001/Poli001Pass123@XEPDB1
```

## Ejecución manual

Conectarse como `POLI001` en `XEPDB1` (SQL Developer o sqlplus) y ejecutar en orden los scripts de `scripts/init/`:

1. `01_tablespace_usuario.sql` — solo como `SYSTEM` (tablespace y usuario)
2. `02_creacion_tablas.sql`
3. `03_insercion_datos.sql`
4. `04_indices.sql`

En los scripts `02` a `04`, **omitir las 2 primeras líneas** (`ALTER SESSION...`) si ya estás conectado como `POLI001`. Esas líneas solo las necesita Docker al ejecutar como `SYS`.

Si usaste Docker (`docker compose up`), los scripts ya corrieron automáticamente y no necesitas ejecutarlos de nuevo.

## Modelo de datos (extendido)

```
PAISES → CIUDADES → LOCALIZACIONES → DEPARTAMENTOS
                                  ↘ EMPLEADOS ← CARGOS
                                    ↓ (gerente)
                                  HISTORICO
```

Extensiones respecto al PDF del curso:

- `DEPARTAMENTOS.dpto_localiz_ID` — ubicación del departamento
- `EMPLEADOS.empl_localiz_ID` — ubicación del empleado (Entrega 3: cambio de dirección)
- `HISTORICO.emphist_empl_ID` — empleado retirado (Entrega 3: operación Delete)
- `EMPLEADOS.empl_activo` — soft delete (`S`/`N`)

## Verificación

```sql
SELECT 'PAISES' AS tabla, COUNT(*) AS total FROM PAISES
UNION ALL SELECT 'CIUDADES', COUNT(*) FROM CIUDADES
UNION ALL SELECT 'LOCALIZACIONES', COUNT(*) FROM LOCALIZACIONES
UNION ALL SELECT 'DEPARTAMENTOS', COUNT(*) FROM DEPARTAMENTOS
UNION ALL SELECT 'CARGOS', COUNT(*) FROM CARGOS
UNION ALL SELECT 'EMPLEADOS', COUNT(*) FROM EMPLEADOS
UNION ALL SELECT 'HISTORICO', COUNT(*) FROM HISTORICO;
-- Esperado: 5 en cada fila
```

Consulta JOIN de ejemplo:

```sql
SELECT e.empl_ID,
       e.empl_primer_nombre || ' ' || e.empl_segundo_nombre AS empleado,
       c.cargo_nombre,
       d.dpto_nombre,
       l.localiz_direccion,
       ci.ciud_nombre,
       p.pais_nombre
FROM EMPLEADOS e
JOIN CARGOS c ON e.empl_cargo_ID = c.cargo_ID
JOIN DEPARTAMENTOS d ON e.empl_dpto_ID = d.dpto_ID
JOIN LOCALIZACIONES l ON e.empl_localiz_ID = l.localiz_ID
JOIN CIUDADES ci ON l.localiz_ciudad_ID = ci.ciud_ID
JOIN PAISES p ON ci.ciud_pais_ID = p.pais_ID
ORDER BY e.empl_ID;
```

## Estructura del repositorio

```
├── docker-compose.yml
├── scripts/init/            # Scripts SQL (Docker init y ejecución manual)
│   ├── 01_tablespace_usuario.sql
│   ├── 02_creacion_tablas.sql
│   ├── 03_insercion_datos.sql
│   └── 04_indices.sql
└── docs/local/              # Plantilla APA y guion (NO se commitea)
```
