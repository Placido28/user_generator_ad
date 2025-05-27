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
```
2. Crea un entorno virtual (opcional):

```bash
python -m venv venv
venv\Scripts\activate  # En Windows
```
3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## USO

1. Asegúrate de haber configurado las credenciales en config.py:

```python
AD_SERVER = 'IP_SERVIDOR'
AD_DOMAIN = 'dominio'     
BASE_DN = 'DC=prymera,DC=local' # Cambiar según tu dominio
```

2. Ejecuta el programa principal:

```bash
python main.py
```

3. Inserta tu archivo Excel con la lista de codigo de usuarios(Se inserto un excel segun lógica de creación de usuario basado en el sistema microbank de la empresa).

4. Presiona "Generar" para obtener los nombres de usuario disponibles.

5. Visualiza los resultados en la ventana emergente.

## Estructura del proyecto

```arduino
user_generator_ad/
├── ad_connector.py
├── config.py
├── data/
│   └── usuarios_inactivos.csv
├── main.py
├── username_generator.py
├── ventana_resultado.py
├── requirements.txt
└── README.md
```
### Tecnologías

* Python

* Active Directory (via ldap3)

* GUI con CustomTkinter y tkinter

* Pandas y OpenPyXL para manipulación de Excel

* Pillow para manejo de imágenes

### Notas de seguridad
* No subas archivos sensibles ni credenciales reales al repositorio.

* El archivo usuarios_inactivos.csv contiene solo códigos de usuario, sin datos personales identificables.

### AUTOR
Cristopher Placido Ocaña
Desarrollador backend - Automatización TI
[GitHub]([https://github.com/Fosowl](https://github.com/Placido28?tab=repositories)) | [LinkedIn](https://www.linkedin.com/in/cristopher-placido-oca%C3%B1a/) 
