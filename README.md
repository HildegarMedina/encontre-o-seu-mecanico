# Encontre o seu mecánico

![Badge](https://img.shields.io/static/v1?label=Backend&message=Python%20(FastApi)&color=rgb(60,150,100)&style=for-the-badge&logo=%3CLOGO%3E) ![Badge](https://img.shields.io/static/v1?label=Frontend&message=Vue.js%20(Nuxt)&color=rgb(87,95,207)&style=for-the-badge&logo=%3CLOGO%3E)

## Tecnologías utilizadas en el desarrollo

### Backend
- Python
- FastApi

### Frontend
- Vue.js
- Nuxt.js
- Bulma Components (Styles)

### Configurando el backend

> python -m venv .venv

> sourve .venv/bin/activate

> cd server

> cp config/config.sample.py config/config.py

> pip install -r requirements

> cd ..

### Configurando la base de datos

Debes crear dos bases de datos en postgres, para eso debes usar:

> sudo -u postgres psql

> CREATE DATABASE encontre_o_seu_mecanico;

> CREATE DATABASE encontre_o_seu_mecanico_test;

Ademas, debes configurar el nombre de la base de datos y las credenciales en el archivo config/config.py

La base de datos 'encontre_o_seu_mecanico_test' se usar solo para pruebas unitarias.

### Ejecutando el seeder


> ./run script seed


### Iniciando el servidor


> ./run server

## Anotaciones

En la carpeta server del proyecto se encuentra un carpeta llamada "insomnia", la cual contiene un archivo JSON con todas las configuraciones y rutas disponibles en la API.


## Errores comúnes

En algunos casos al cambiar la estructura de los modelos, puede que no actualicen en Postgres, por lo tanto
debes eliminar la base de datos y crearla de nuevo con:

> DROP DATABASE encontre_o_seu_mecanico;

> DROP DATABASE encontre_o_seu_mecanico_test;

> CREATE DATABASE encontre_o_seu_mecanico;

> CREATE DATABASE encontre_o_seu_mecanico_test;