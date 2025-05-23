# username_generator.py
import unicodedata

def limpiar_texto(texto):
    if not texto:
        return ""
    # Quitar espacios y pasar a minúsculas
    texto = texto.replace(" ", "").lower()
    # Normalizar para quitar tildes y reemplazar ñ
    texto = unicodedata.normalize('NFKD', texto)
    texto = ''.join(c for c in texto if not unicodedata.combining(c))
    texto = texto.replace('ñ', 'n')
    return texto

def generar_combinaciones(nombre1, nombre2, ap_paterno, ap_materno):

    nombre1 = nombre1.strip().lower() if nombre1 else ""
    nombre2 = nombre2.strip().lower() if nombre2 else ""
    ap_paterno = limpiar_texto(ap_paterno)
    ap_materno = limpiar_texto(ap_materno)

    combinaciones = []

    if nombre1 and ap_paterno:
        combinaciones.append(f"{nombre1[0]}{ap_paterno}".lower())

    if nombre1 and nombre2 and ap_paterno:
        combinaciones.append(f"{nombre1[0]}{nombre2[0]}{ap_paterno}".lower())

    if nombre1 and ap_paterno and ap_materno:
        combinaciones.append(f"{nombre1[0]}{ap_paterno}{ap_materno[0]}".lower())

    if nombre1 and nombre2 and ap_paterno and ap_materno:
        combinaciones.append(f"{nombre1[0]}{nombre2[0]}{ap_paterno}{ap_materno[0]}".lower())

    return combinaciones


def generar_usuario_disponible(nombre1, nombre2, ap_paterno, ap_materno, existe_func):
    combinaciones = generar_combinaciones(nombre1, nombre2, ap_paterno, ap_materno)

    print(f"🔍 Probando combinaciones para {nombre1} {nombre2} {ap_paterno} {ap_materno}")

    # Probar las combinaciones iniciales
    for username in combinaciones:
        print(f"➡️ Probando: {username}")
        if not existe_func(username):
            print(f"✅ Usuario disponible: {username}")
            return username
        else:
            print(f"❌ Ya existe: {username}")

    # Si todas están ocupadas, agregar sufijos numéricos
    base = combinaciones[0] if combinaciones else f"{nombre1[0]}{ap_paterno}".lower()
    i = 1
    while True:
        nuevo_username = f"{base}{i}"
        print(f"➡️ Probando con sufijo: {nuevo_username}")
        if not existe_func(nuevo_username):
            print(f"✅ Usuario disponible: {nuevo_username}")
            return nuevo_username
        i += 1