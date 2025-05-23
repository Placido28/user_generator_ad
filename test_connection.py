from ldap3 import Server, Connection, SIMPLE, ALL
import config

def probar_conexion():
    try:
        print("🔄 Intentando conectar con Active Directory...")
        server = Server(config.AD_SERVER, get_info=ALL)
        conn = Connection(
            server,
            user=f"{config.AD_USER}@{config.AD_DOMAIN}",
            password=config.AD_PASSWORD,
            authentication=SIMPLE,
            auto_bind=True
        )
        print("✅ Conexión exitosa a Active Directory.")
        base_dn = conn.server.info.naming_contexts[0]
        
        print("🔎 Buscando usuarios con nombre y correo...")
        filtro = "(&(objectClass=user)(objectCategory=person))"
        atributos = ["sAMAccountName", "displayName", "mail"]
        
        conn.search(search_base=base_dn, search_filter=filtro, attributes=atributos)

        # Filtrar usuarios con nombre y correo
        usuarios_validos = [
            entry for entry in conn.entries
            if entry.displayName and entry.mail
        ]

        print(f"👤 Usuarios con nombre y correo: {len(usuarios_validos)}")
        for usuario in usuarios_validos:
            print(f"- {usuario.sAMAccountName} | {usuario.displayName} | {usuario.mail}")


        conn.unbind()
    except Exception as e:
        print("❌ Error al conectar al Active Directory:")
        print(str(e))

if __name__ == "__main__":
    probar_conexion()
