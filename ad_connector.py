# ad_connector.py

from ldap3 import Server, Connection, SIMPLE, ALL
import config

def conectar_ad(usuario, clave):
    usuario_bind = f"{usuario}@{config.AD_DOMAIN}"

    server = Server(config.AD_SERVER, get_info=ALL)
    conn = Connection(
        server,
        user=usuario_bind,
        password=clave,
        authentication=SIMPLE,
        auto_bind=True
    )

    # Buscar el grupo de Domain Admins
    filtro = f"(&(objectClass=user)(sAMAccountName={usuario}))"
    conn.search(config.BASE_DN, filtro, attributes=["memberOf"])
    if not conn.entries:
        raise Exception("Usuario no encontrado en el dominio.")

    grupos = []
    entry = conn.entries[0]
    if hasattr(entry, "memberOf"):
        grupos = entry.memberOf.values if isinstance(entry.memberOf.value, list) else [entry.memberOf.value]
    # El nombre del grupo puede variar, pero normalmente es "CN=Domain Admins"
    es_admin = any("CN=Admins. del dominio" in g for g in grupos)
    if not es_admin:
        raise Exception("Debe conectarse con un usuario administrador del dominio.")

    return conn

def usuario_existe_ad(conn, username):
    filtro = f"(sAMAccountName={username})"
    conn.search(config.BASE_DN, filtro, attributes=["sAMAccountName"])
    return len(conn.entries) > 0

