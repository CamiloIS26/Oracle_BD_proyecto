import socket

HOST = "127.0.0.1"
PORT = 5000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))


def menu_principal():
    print("\n====== Sistema Recursos Humanos ======")
    print("1. Consultar empleado")
    print("2. Insertar empleado")
    print("3. Actualizar empleado")
    print("4. Retirar empleado")
    print("5. Salir")


def menu_actualizar():
    print("\n--- ACTUALIZAR EMPLEADO ---")
    print("1. Sueldo")
    print("2. Correo electrónico")
    print("3. Cargo")
    print("4. Departamento")
    print("5. Dirección y ciudad")
    print("6. Volver")


while True:
    menu_principal()
    opcion = input("Seleccione opción: ")

    # Consultar datos de un empleado
    if opcion == "1":
        id_emp = input("ID empleado: ")
        mensaje = f"SELECT|{id_emp}"

        cliente.send(mensaje.encode())
        print("Servidor:", cliente.recv(1024).decode())

    # Insertar un nuevo empleado
    elif opcion == "2":
        print("\nIngrese datos separados por coma:")
        print("Cargo, Gerente, Departamento, Localización, Nombre, Segundo Nombre, Email, Fecha de Nacimiento (YYYY-MM-DD), Sueldo, Comisión")

        datos = input("Datos: ")
        mensaje = f"INSERT|{datos}"

        cliente.send(mensaje.encode())
        print("Servidor:", cliente.recv(1024).decode())

    # Actualizar datos del empleado
    elif opcion == "3":

        id_emp = input("Ingrese ID del empleado: ")

        # Validar en servidor
        cliente.send(f"GET_EMPLOYEE|{id_emp}".encode())
        respuesta = cliente.recv(1024).decode()

        if respuesta.startswith("ERROR"):
            print(respuesta)
            continue

        datos = respuesta.split("|")

        print("\nEmpleado encontrado:")
        print("ID:", datos[1])
        print("Nombre:", datos[2])
        print("Email:", datos[3])

        while True:
            menu_actualizar()
            op = input("Seleccione qué actualizar: ")

            if op == "1":
                nuevo = input("Nuevo sueldo: ")
                mensaje = f"UPDATE_SUELDO|{nuevo},{id_emp}"

            elif op == "2":
                nuevo = input("Nuevo email: ")
                mensaje = f"UPDATE_EMAIL|{nuevo},{id_emp}"

            elif op == "3":
                nuevo = input("Nuevo cargo ID: ")
                mensaje = f"UPDATE_CARGO|{nuevo},{id_emp}"

            elif op == "4":
                nuevo = input("Nuevo departamento ID: ")
                mensaje = f"UPDATE_DPTO|{nuevo},{id_emp}"

            elif op == "5":
                direccion = input("Nueva dirección: ")
                ciudad = input("Nueva ciudad ID: ")
                mensaje = f"UPDATE_DIRECCION|{id_emp},{direccion},{ciudad}"

            elif op == "6":
                break

            else:
                print("Opción inválida")
                continue

            cliente.send(mensaje.encode())
            print("Servidor:", cliente.recv(1024).decode())

    # Eliminar empleado
    elif opcion == "4":
        id_emp = input("ID empleado: ")
        mensaje = f"DELETE|{id_emp}"

        cliente.send(mensaje.encode())
        print("Servidor:", cliente.recv(1024).decode())

    # Salir del sistema
    elif opcion == "5":
        cliente.send("SALIR".encode())
        break

    else:
        print("Opción inválida")

cliente.close()