import requests

def obtener_datos_usuario(usuario):
    try:
        respuesta = requests.get(f"https://api.github.com/users/{usuario}")
        datos = respuesta.json()
        if respuesta.status_code == 200:
            return {
                "nombre": datos["name"] or "Sin nombre",
                "bio": datos["bio"] or "Sin bio",
                "seguidores": datos["followers"],
                "repositorios": datos["public_repos"]
            }
        else:
            return None
    except Exception as e:
        print("Error:", e)
        return None

def comparar_usuarios():
    usuarios = []
    
    for i in range(3):
        nombre = input(f"Escribe el usuario {i+1} de GitHub: ")
        datos = obtener_datos_usuario(nombre)
        if datos:
            usuarios.append({"usuario": nombre, **datos})
        else:
            print("Usuario no encontrado, saltando...")

    print("\n--- COMPARATIVA ---")
    for u in usuarios:
        print(f"\n👤 {u['usuario']}")
        print(f"   Nombre: {u['nombre']}")
        print(f"   Seguidores: {u['seguidores']}")
        print(f"   Repositorios: {u['repositorios']}")

    print("\n--- GANADORES ---")
    mejor_seguidores = max(usuarios, key=lambda x: x["seguidores"])
    mejor_repos = max(usuarios, key=lambda x: x["repositorios"])
    
    print(f"Más seguidores: {mejor_seguidores['usuario']} con {mejor_seguidores['seguidores']}")
    print(f"Más repositorios: {mejor_repos['usuario']} con {mejor_repos['repositorios']}")

comparar_usuarios()