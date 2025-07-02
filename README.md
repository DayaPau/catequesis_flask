# 🕊Sistema de Gestión de Catequesis con Flask y MongoDB

Este proyecto implementa una interfaz web para gestionar el proceso de catequesis en parroquias, permitiendo registrar catequizados, consultar información clave del sistema y visualizar parroquias, certificados, asistencias y sacramentos.

---

## Funcionalidades principales

-  Registro de catequizados (personas)
- Consulta de catequizados y parroquias
-  Reportes dinámicos (en construcción)
-  Interfaz web con Flask y HTML
-  Conexión segura con base de datos MongoDB en la nube

---

##  Tecnologías utilizadas

- [Python 3.x](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [MongoDB Atlas](https://www.mongodb.com/atlas)
- [HTML + Jinja](https://jinja.palletsprojects.com/)
- [VS Code](https://code.visualstudio.com/)
- [MongoDB Compass](https://www.mongodb.com/products/compass)

---

## ¿Por qué MongoDB Atlas?

Elegimos **MongoDB Atlas**, la plataforma en la nube de MongoDB, por varias razones clave:

- **Conexión desde cualquier entorno**: accesible desde Flask sin necesidad de instalar MongoDB localmente.
- **Seguridad y control**: se pueden crear usuarios específicos y restringir IPs.
- **Escalabilidad**: soporta crecimiento futuro del sistema sin necesidad de migrar datos.
- **Interfaz gráfica (Compass)**: fácil de administrar colecciones, consultar datos y validar estructuras.

Además, se usó el paquete `python-dotenv` para cargar la conexión de forma **segura** desde un archivo `.env` sin exponer credenciales en el repositorio.

---


