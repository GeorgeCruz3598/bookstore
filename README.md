# LibroAmigo: Tu Tienda Online de Libros de Segunda Mano

LibroAmigo es una aplicación web de comercio electrónico desarrollada con Flask que facilita la venta de libros de segunda mano. El proyecto sigue una arquitectura Modelo-Vista-Controlador (MVC) para una mejor organización y mantenibilidad del código, y utiliza Flask-SQLAlchemy para la gestión de la base de datos, Flask-Login para la autenticación de usuarios, y Flask WTforms para el manejo de formularios y validación de datos.

## Características Principales

* **Gestión de Usuarios:** Registro, inicio de sesión y gestion de usuarios del sistema.
* **Catálogo de Libros:** Explora, busca y visualiza detalles de libros disponibles.
* **Categorías:** Organización de libros por categorías temáticas.
* **Gestión de Pedidos:** Historial de pedidos de usuarios, creacion y edicion de registros.
* **Gestión de Compras (a Proveedores):** Funcionalidad para que los administradores gestionen la adquisición de libros a proveedores.
* **Métodos de Pago:** Integración de diferentes métodos de pago.
* **Panel de Administración:** Para la gestión completa de las entidades de la aplicación (libros, categorias, usuarios proveedores, etc.).
* **Carga de Imágenes:** Sube portadas de libros para una mejor visualización.
* **Contactos:** Formulario de contacto para consultas y sugerencias de usuarios.

## Tecnologías Utilizadas

* **Backend:** Python 3.11, Flask, Flask-SQLAlchemy, Flask-Login, Werkzeug (para seguridad de contraseñas).
* **Base de Datos:** SQLite (por defecto, configurable para otras bases de datos relacionales).
* **Frontend:** HTML5, CSS3, JavaScript.

## Configuración y Ejecución

Sigue estos pasos para levantar la aplicación en tu entorno local:

1.  **Clonar el Repositorio:**
    ```bash
    git clone https://github.com/GeorgeCruz3598/bookstore.git
    cd bookstore
    ```

2.  **Crear un Entorno Virtual (Recomendado):**
    ```bash
    python -m venv venv
    ```

3.  **Activar el Entorno Virtual:**
    * **Windows:**
        ```bash
        venv\Scripts\activate
        ```
    * **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Instalar Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
    
5.  **Inicializar la Base de Datos:**
    La base de datos SQLite (`bookstore.db`) se creará automáticamente la primera vez que se ejecute la aplicación si no existe. 

6.  **Ejecutar la Aplicación:**
    ```bash
    python run.py
    ```
    La aplicación estará disponible en `http://127.0.0.1:5000/` o la dirección que Flask indique en la consola.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir al proyecto, por favor:

1.  Haz un "fork" del repositorio.
2.  Crea una nueva rama (`git checkout -b feature/nueva-caracteristica`).
3.  Realiza tus cambios y commitea (`git commit -m 'feat: Añadir nueva característica'`).
4.  Sube tus cambios (`git push origin feature/nueva-caracteristica`).
5.  Abre un "Pull Request".
