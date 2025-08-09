# Pollinations.ai Prompt Enhancer

Un programa con interfaz gráfica de usuario (GUI) segura y robusta para mejorar prompts de texto utilizando la API de Pollinations.ai, con una interfaz de usuario dinámica basada en un archivo JSON externo.

## Características

*   **UI Dinámica:** La interfaz se genera dinámicamente a partir de un archivo `prompts.json`, permitiendo una fácil personalización de las categorías de prompts.
*   **Cliente de API Seguro:** La aplicación utiliza un cliente de API seguro que valida los certificados SSL y carga el token de la API desde un archivo `.env`.
*   **Manejo de Errores Robusto:** La aplicación cuenta con un sólido manejo de errores para gestionar problemas de red, errores de la API y otros eventos inesperados.
*   **Llamadas Asíncronas a la API:** La aplicación utiliza un grupo de hilos (thread pool) para realizar llamadas asíncronas a la API, asegurando que la GUI permanezca receptiva.
*   **Gestión de Historial y Conversación:** La aplicación mantiene un historial de los prompts mejorados y las conversaciones para cada categoría.
*   **Exportar y Copiar:** Permite exportar conversaciones y copiar los prompts mejorados al portapapeles.
*   **Inicio Maximizado:** La ventana de la aplicación se inicia maximizada para una mejor experiencia de usuario.

## Autor

*   **Creado por:** Diego Gonzalez
*   **Contacto:** diegoalgg88@gmail.com

## Instalación y Configuración

Sigue estos pasos para configurar el entorno de la aplicación.

### 1. Prerrequisitos

*   Tener Python 3 instalado.

### 2. Configurar el Token de API

Antes de ejecutar la configuración, debes proporcionar tu token de API de Pollinations.ai.

1.  En la raíz del proyecto, crea un archivo llamado `.env`.
2.  Abre el archivo `.env` y añade tu token de la siguiente manera:

    ```
    API_TOKEN=tu-token-de-api-aqui
    ```

### 3. Ejecutar el Script de Configuración

He creado un script para automatizar la creación del entorno virtual y la instalación de dependencias.

1.  Abre una terminal en el directorio raíz del proyecto.
2.  Ejecuta el siguiente comando:

    ```
    python setup.py
    ```

    Este script creará una carpeta `.venv` con el entorno virtual e instalará todas las librerías necesarias que se encuentran en `project/requirements.txt`.

## Uso

Para ejecutar la aplicación, simplemente haz doble clic en el archivo `run.bat` que se encuentra en el directorio raíz del proyecto.

Este script se encargará de:

1.  Solicitar permisos de administrador (necesarios para una correcta ejecución).
2.  Activar el entorno virtual correcto.
3.  Iniciar la aplicación.

## Estructura del Proyecto

El proyecto está organizado en varios directorios y módulos para mantener el código limpio y escalable.

-   `setup.py`: Script en la raíz del proyecto que automatiza la creación de un entorno virtual (`.venv`) y la instalación de las dependencias necesarias.
-   `run.bat`: Archivo ejecutable de Windows en la raíz que inicia la aplicación con privilegios de administrador y utilizando el entorno virtual correcto.
-   `logs/`: Directorio en la raíz que almacena los logs de ejecución de la aplicación.
-   `project/`: Contiene todo el código fuente de la aplicación.
    -   `main.py`: Punto de entrada principal que inicia la aplicación.
    -   `requirements.txt`: Lista de las librerías de Python necesarias.
    -   `config/`: Módulo encargado de la configuración.
        -   `config.ini`: Define la configuración de la API y la aplicación (URL, timeouts, dimensiones de la ventana).
        -   `prompts.json`: Archivo clave que permite definir dinámicamente las categorías y los prompts de mejora que aparecen en la interfaz.
    -   `core/`: Contiene la lógica principal de la aplicación.
        -   `gui.py`: Define toda la estructura, diseño y comportamiento de la interfaz gráfica de usuario (GUI) con Tkinter.
        -   `api_client.py`: Gestiona la comunicación segura con la API de Pollinations.ai.
    -   `utils/`: Módulo para utilidades transversales.
        -   `logger.py`: Configura el sistema de logging para registrar eventos y errores.
    -   `docs/`: Documentación adicional del proyecto.

A continuación, se muestra una representación gráfica de la estructura:

```
Enhance_Prompt/
├── .env                # (Debe ser creado por el usuario)
├── run.bat             # Script de ejecución para Windows
├── setup.py            # Script de configuración del entorno
├── logs/               # Logs de la aplicación
├── depreciated/        # Código antiguo (no utilizado)
└── project/
    ├── main.py         # Punto de entrada de la aplicación
    ├── requirements.txt
    ├── config/
    │   ├── config.ini
    │   └── prompts.json
    ├── core/
    │   ├── api_client.py
    │   └── gui.py
    ├── utils/
    │   └── logger.py
    ├── docs/
    │   ├── CONTRIBUTING.md
    │   └── LICENSE
    └── tests/
```

## Contribuciones

Por favor, lee [CONTRIBUTING.md](docs/CONTRIBUTING.md) para más detalles sobre nuestro código de conducta y el proceso para enviarnos pull requests.

## Licencia

Este proyecto está bajo la Licencia MIT - consulta el archivo [LICENSE](docs/LICENSE) para más detalles.