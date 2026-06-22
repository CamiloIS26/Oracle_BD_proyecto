import socket
import os

HOST = "127.0.0.1"
PORT = 5000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    cliente.connect((HOST, PORT))
except socket.error as e:
    print(f"Error al conectar con el servidor: {e}")
    print("Asegúrate de que el servidor esté en ejecución y accesible.")
    exit()

def clear_screen():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def send_and_receive(sock, message):
    """Envía un mensaje al servidor y espera una respuesta."""
    try:
        sock.sendall(message.encode('utf-8'))
        response = sock.recv(4096).decode('utf-8')
        return response
    except socket.error as e:
        print(f"Error de comunicación con el servidor: {e}")
        return "ERROR|Network issue"

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

def handle_consultar_empleado():
    id_emp = input("ID empleado: ")
    if not id_emp.isdigit():
        print("Error: El ID del empleado debe ser numérico.")
        return

    mensaje = f"SELECT|{id_emp}"
    respuesta = send_and_receive(cliente, mensaje)
    print("Servidor:", respuesta)

def handle_insertar_empleado():
    print("\n--- INSERTAR EMPLEADO ---")
    print("Por favor, ingrese los datos del nuevo empleado:")
    cargo = input("Cargo: ")
    gerente = input("Gerente (ID o Nombre): ")
    departamento = input("Departamento (ID o Nombre): ")
    localizacion = input("Localización (ID o Nombre): ")
    nombre = input("Nombre: ")
    segundo_nombre = input("Segundo Nombre (opcional): ")
    email = input("Email: ")
    fecha_nacimiento = input("Fecha de Nacimiento (YYYY-MM-DD): ")
    sueldo = input("Sueldo: ")
    comision = input("Comisión (opcional): ")

    datos = f"{cargo},{gerente},{departamento},{localizacion},{nombre},{segundo_nombre},{email},{fecha_nacimiento},{sueldo},{comision}"
    mensaje = f"INSERT|{datos}"
    respuesta = send_and_receive(cliente, mensaje)
    print("Servidor:", respuesta)

def handle_actualizar_empleado():
    id_emp = input("Ingrese ID del empleado a actualizar: ")
    if not id_emp.isdigit():
        print("Error: El ID del empleado debe ser numérico.")
        return

    respuesta = send_and_receive(cliente, f"GET_EMPLOYEE|{id_emp}")

    if respuesta.startswith("ERROR"):
        print(respuesta)
        return

    datos = respuesta.split("|")
    print("\nEmpleado encontrado:")
    print("ID:", datos[1])
    print("Nombre:", datos[2])
    print("Email:", datos[3])

    while True:
        menu_actualizar()
        op = input("Seleccione qué actualizar: ")
        
        mensaje = ""
        if op == "1":
            nuevo = input("Nuevo sueldo: ")
            if not nuevo.replace('.', '', 1).isdigit():
                print("Error: El sueldo debe ser numérico.")
                continue
            mensaje = f"UPDATE_SUELDO|{nuevo},{id_emp}"
        elif op == "2":
            nuevo = input("Nuevo email: ")
            
            if "@" not in nuevo or "." not in nuevo:
                print("Error: Formato de email inválido.")
                continue
            mensaje = f"UPDATE_EMAIL|{nuevo},{id_emp}"
        elif op == "3":
            nuevo = input("Nuevo cargo ID: ")
            if not nuevo.isdigit():
                print("Error: El ID de cargo debe ser numérico.")
                continue
            mensaje = f"UPDATE_CARGO|{nuevo},{id_emp}"
        elif op == "4":
            nuevo = input("Nuevo departamento ID: ")
            if not nuevo.isdigit():
                print("Error: El ID de departamento debe ser numérico.")
                continue
            mensaje = f"UPDATE_DPTO|{nuevo},{id_emp}"
        elif op == "5":
            direccion = input("Nueva dirección: ")
            ciudad = input("Nueva ciudad ID: ")
            if not ciudad.isdigit():
                print("Error: El ID de ciudad debe ser numérico.")
                continue
            mensaje = f"UPDATE_DIRECCION|{id_emp},{direccion},{ciudad}"
        elif op == "6":
            break
        else:
            print("Opción inválida")
            continue

        if mensaje: 
            print("Servidor:", send_and_receive(cliente, mensaje))

def handle_retirar_empleado():
    id_emp = input("ID empleado a retirar: ")
    if not id_emp.isdigit():
        print("Error: El ID del empleado debe ser numérico.")
        return

    confirmacion = input(f"¿Está seguro de que desea retirar al empleado con ID {id_emp}? (s/N): ").lower()
    if confirmacion != 's':
        print("Operación cancelada.")
        return

    mensaje = f"DELETE|{id_emp}"
    respuesta = send_and_receive(cliente, mensaje)
    print("Servidor:", respuesta)

while True:
    clear_screen()
    menu_principal()
    opcion = input("Seleccione opción: ")

    if opcion == "1":
        handle_consultar_empleado()
    elif opcion == "2":
        handle_insertar_empleado()
    elif opcion == "3":
        handle_actualizar_empleado()
    elif opcion == "4":
        handle_retirar_empleado()
    elif opcion == "5":
        print("Saliendo del sistema...")
        send_and_receive(cliente, "SALIR") 
        break
    else:
        print("Opción inválida. Intente de nuevo.")
    
    input("\nPresione Enter para continuar...") 

cliente.close()