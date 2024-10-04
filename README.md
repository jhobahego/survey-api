# Proyecto de Encuesta

Este proyecto es una API para gestionar encuestas. A continuación, se detallan los pasos necesarios para arrancar la API y las consideraciones importantes para su correcto funcionamiento.

## Requisitos

- Python 3.8 o superior
- Base de datos (PostgreSQL, MySQL)

## Instalación

1. Clona el repositorio:

    ```sh
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_REPOSITORIO>
    ```

2. Crea y activa un entorno virtual:

    ```sh
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. Instala las dependencias:

    ```sh
    pip install -r requirements.txt
    ```

4. Configura las variables de entorno. Crea un archivo `.env` en la raíz del proyecto y añade las siguientes variables:

    ```env
    DB_USERNAME=<tu-db-username>
    DB_PASSWORD=<tu-db-password>
    DB_HOST=<tu-db-host>
    DB_PORT=<tu-db-port>
    DB_DATABASE=<tu-db-name>
    SECRET_KEY=<a-secret-key-to-encoded>
    ADMIN_EMAILS=<admin@email.com,correoadmin1@test.com,correoadmin2@test.com>
    ```

## Ejecución

Para arrancar la API, ejecuta el siguiente comando:

```sh
uvicorn main:app --reload
```

Al arrancar te manda a la documentación de la API, que está hecha usando swagger.