# Taskify API

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-v0.95-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Taskify** es una API REST sencilla para gestionar tareas personales, construida con **Python** y **FastAPI**.  
Permite crear, listar, actualizar y eliminar tareas, y cuenta con una autenticación básica por token.

---

## 🔹 Tecnologías usadas

- Python 3.10+
- FastAPI
- Uvicorn (servidor ASGI)
- SQLAlchemy (ORM)
- SQLite (base de datos ligera)
- Pydantic (validación de datos)

---

## 📁 Estructura del proyecto

TaskifyAPI/
├─ .venv/ # Entorno virtual (no subir a Git)
├─ main.py # Código principal de la API
├─ requirements.txt # Dependencias del proyecto
└─ README.md # Este archivo


---

## ⚡ Instalación

1. Clonar el repositorio:
  git clone <URL_DEL_REPOSITORIO>
  cd TaskifyAPI

2. crear entorno virtual
  python -m venv .venv

  .\.venv\Scripts\Activate.ps1

3 instalar dependencias
  source .venv/bin/activate
  .\.venv\Scripts\Activate.ps1
  
  pip install fastapi uvicorn sqlalchemy pydantic

🚀 Ejecutar la API

    Con el entorno virtual activado:
      uvicorn main:app --reload

    La api estará disponible en "http://127.0.0.1:8000"

🔹 Endpoints principales


| Método | Ruta          | Descripción                                                              |
| ------ | ------------- | ------------------------------------------------------------------------ |
| POST   | `/login`      | Devuelve un token si las credenciales son correctas (`admin` / `secret`) |
| GET    | `/tasks`      | Lista todas las tareas (requiere token)                                  |
| POST   | `/tasks`      | Crea una nueva tarea (requiere token)                                    |
| GET    | `/tasks/{id}` | Obtiene una tarea específica (requiere token)                            |
| PUT    | `/tasks/{id}` | Actualiza una tarea completa (requiere token)                            |
| PATCH  | `/tasks/{id}` | Actualiza parcialmente una tarea (requiere token)                        |
| DELETE | `/tasks/{id}` | Elimina una tarea (requiere token)                                       |


🔹 Mejoras futuras

  Autenticación con JWT y usuarios en base de datos
  
  Paginación y filtros en listado de tareas
  
  Tests automatizados con pytest
  
  Despliegue en servidor (Heroku, Render, Railway, etc.)


