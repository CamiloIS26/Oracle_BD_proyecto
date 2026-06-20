import socket
import oracledb

HOST = "127.0.0.1"
PORT = 5000


def conectar_oracle():
    return oracledb.connect(
        user="POLI001",
        password="Poli001Pass123",
        dsn="localhost:1521/XEPDB1"
    )


def procesar_comando(mensaje, conn):
    cursor = conn.cursor()

    partes = mensaje.split("|")
    comando = partes[0]

    # Comando ver datos de un empleado
    if comando == "GET_EMPLOYEE":
        id_emp = partes[1]

        cursor.execute("""
            SELECT empl_ID, empl_primer_nombre, empl_email
            FROM EMPLEADOS
            WHERE empl_ID = :id
        """, id=id_emp)

        row = cursor.fetchone()

        if row:
            return f"OK|{row[0]}|{row[1]}|{row[2]}"
        else:
            return "ERROR|Empleado no encontrado"
    
    elif comando == "SELECT":

        id_emp = partes[1]

        cursor.execute("""
            SELECT
                e.empl_ID,
                e.empl_primer_nombre,
                e.empl_segundo_nombre,
                e.empl_email,
                e.empl_sueldo,
                ci.ciud_nombre,
                l.localiz_direccion,
                e.empl_activo
            FROM EMPLEADOS e
            JOIN LOCALIZACIONES l
                ON e.empl_localiz_ID = l.localiz_ID
            JOIN CIUDADES ci
                ON l.localiz_ciudad_ID = ci.ciud_ID
            WHERE e.empl_ID = :id
        """, id=id_emp)

        row = cursor.fetchone()

        if row:
            return (
                f"\nID: {row[0]}"
                f"\nNombre: {row[1]} {row[2]}"
                f"\nEmail: {row[3]}"
                f"\nSueldo: {row[4]}"
                f"\nCiudad: {row[5]}"
                f"\nDirección: {row[6]}"
                f"\nActivo: {row[7]}"
            )

        return "Empleado no encontrado"

    # Comando para insertar datos de un nuevo empleado
    elif comando == "INSERT":
        datos = partes[1].split(",")

        cursor.execute("""
            INSERT INTO EMPLEADOS (
                empl_cargo_ID,
                empl_gerente_ID,
                empl_dpto_ID,
                empl_localiz_ID,
                empl_primer_nombre,
                empl_segundo_nombre,
                empl_email,
                empl_fecha_nac,
                empl_sueldo,
                empl_comision
            ) VALUES (
                :1,:2,:3,:4,:5,:6,:7,TO_DATE(:8,'YYYY-MM-DD'),:9,:10
            )
        """, datos)

        conn.commit()
        return "Empleado insertado correctamente"

    # actualizar datos de un empleado
    elif comando == "UPDATE_SUELDO":
        datos = partes[1].split(",")

        sueldo = datos[0]
        id_emp = datos[1]

        cursor.execute("""
            UPDATE EMPLEADOS
            SET empl_sueldo = :1
            WHERE empl_ID = :2
        """, [sueldo, id_emp])

        conn.commit()
        return "Sueldo actualizado correctamente"
    
    elif comando == "UPDATE_EMAIL":
        datos = partes[1].split(",")

        email = datos[0]
        id_emp = datos[1]

        cursor.execute("""
            UPDATE EMPLEADOS
            SET empl_email = :1
            WHERE empl_ID = :2
        """, [email, id_emp])

        conn.commit()
        return "Correo actualizado correctamente"
    
    elif comando == "UPDATE_CARGO":
        datos = partes[1].split(",")

        cargo = datos[0]
        id_emp = datos[1]

        cursor.execute("""
            UPDATE EMPLEADOS
            SET empl_cargo_ID = :1
            WHERE empl_ID = :2
        """, [cargo, id_emp])

        conn.commit()
        return "Cargo actualizado correctamente"
    
    elif comando == "UPDATE_DPTO":
        datos = partes[1].split(",")

        dpto = datos[0]
        id_emp = datos[1]

        cursor.execute("""
            UPDATE EMPLEADOS
            SET empl_dpto_ID = :1
            WHERE empl_ID = :2
        """, [dpto, id_emp])

        conn.commit()
        return "Departamento actualizado correctamente"
    
    elif comando == "UPDATE_DIRECCION":
        datos = partes[1].split(",")

        id_emp = datos[0]
        nueva_direccion = datos[1]
        nueva_ciudad = datos[2]

        cursor.execute("""
            SELECT empl_localiz_ID
            FROM EMPLEADOS
            WHERE empl_ID = :id
        """, id=id_emp)

        resultado = cursor.fetchone()

        if resultado:

            localiz_id = resultado[0]

            cursor.execute("""
                UPDATE LOCALIZACIONES
                SET localiz_direccion = :dir,
                    localiz_ciudad_ID = :ciudad
                WHERE localiz_ID = :loc
            """,
            dir=nueva_direccion,
            ciudad=nueva_ciudad,
            loc=localiz_id)

            conn.commit()

            return "Dirección y ciudad actualizadas"

        return "Empleado no encontrado"

    # Retirar empleado
    elif comando == "DELETE":
        id_emp = partes[1]

        cursor.execute("""
            INSERT INTO HISTORICO (
                emphist_empl_ID,
                emphist_cargo_ID,
                emphist_dpto_ID,
                emphist_fecha_retiro
            )
            SELECT
                empl_ID,
                empl_cargo_ID,
                empl_dpto_ID,
                SYSDATE
            FROM EMPLEADOS
            WHERE empl_ID = :id
        """, id=id_emp)

        cursor.execute("""
            UPDATE EMPLEADOS
            SET empl_activo = 'N'
            WHERE empl_ID = :id
        """, id=id_emp)

        conn.commit()

        return "Empleado retirado y enviado a histórico"


# Socket servidor 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Servidor escuchando en puerto", PORT)

conn_db = conectar_oracle()

cliente, addr = server.accept()
print("Cliente conectado:", addr)

while True:
    mensaje = cliente.recv(1024).decode()

    if mensaje == "SALIR":
        break

    respuesta = procesar_comando(mensaje, conn_db)

    cliente.send(respuesta.encode())

cliente.close()
conn_db.close()
server.close()