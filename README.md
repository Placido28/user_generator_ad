# User Generator AD

**Generador automático de nombres de usuario con validación contra Active Directory.**

Este proyecto proporciona una aplicación de escritorio desarrollada en Python que permite generar nombres de usuario a partir de archivos Excel, aplicando reglas de transformación y verificando su disponibilidad en un entorno Active Directory. Es ideal para áreas de TI que deben registrar o migrar cuentas de usuario de forma masiva.

## Características

- Interfaz moderna y responsiva usando CustomTkinter
- Generación automática de nombres de usuario disponibles
- Verificación en tiempo real contra Active Directory
- Carga y limpieza de datos desde Excel
- Exclusión de códigos inactivos
- Resultados visuales y exportables

## Requisitos

- **Python 3.10 o superior**
- Active Directory accesible vía red
- Librerías:

  - `customtkinter`
  - `pandas`
  - `ldap3`
  - `Pillow`

## Instalación

1. Clona el repositorio:
```bash
git clone [https://github.com/tu_usuario/user_generator_ad.git](https://github.com/Placido28/user_generator_ad.git)
cd user_generator_ad
