contactos = []

def agregar_contacto(nombre, telefono, email):
    contacto = {
        "nombre": nombre,
        "telefono": telefono,
        "email": email
    }
    contactos.append(contacto)
    print("✅ Contacto añadido")

def ver_contactos():
    if len(contactos) == 0:
        print("No hay contactos")
    else:
        for c in contactos:
            print("---")
            print("Nombre:", c["nombre"])
            print("Teléfono:", c["telefono"])
            print("Email:", c["email"])

def menu():
    while True:
        print("\n1. Añadir contacto")
        print("2. Ver contactos")
        print("3. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            telefono = input("Teléfono: ")
            email = input("Email: ")
            agregar_contacto(nombre, telefono, email)
        elif opcion == "2":
            ver_contactos()
        elif opcion == "3":
            print("¡Hasta mañana!")
            break
        else:
            print("Opción no válida")

menu()