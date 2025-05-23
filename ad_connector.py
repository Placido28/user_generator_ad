# ad_connector.py

from ldap3 import Server, Connection, SIMPLE, ALL
import config

def conectar_ad(usuario, clave):
    usuario_bind = f"{usuario}@{config.AD_DOMAIN}"

    server = Server(config.AD_SERVER, get_info=ALL)
    conn = Connection(
        server,
        user=usuario_bind,                # asisthelp2.ldap@prymera.local
        password=clave,
        authentication=SIMPLE,
        auto_bind=True
    )
    return conn

def usuario_existe_ad(conn, username):
    filtro = f"(sAMAccountName={username})"
    conn.search(config.BASE_DN, filtro, attributes=["sAMAccountName"])
    return len(conn.entries) > 0

