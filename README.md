# 🔒 Vent Vault

> *Desahógate. Todo es anónimo. Todo desaparece.*

**Vent Vault** es una aplicación web minimalista diseñada como un buzón de catarsis anónimo de 24 horas. Los usuarios pueden escribir y desahogarse sabiendo que su mensaje será encriptado de inmediato y destruido físicamente de la base de datos tras cumplirse un ciclo de un día.

---

## ⚡ Características Principales

- **100% Anónimo:** Sin registro, sin cookies, sin tokens ni almacenamiento de datos de identificación o IP.
- **Auto-destrucción física (24h):** Uso de **índices TTL (Time-To-Live)** nativos de MongoDB que eliminan físicamente los documentos **86,400 segundos** después de ser creados.
- **Cifrado en memoria:** Los textos se cifran antes de persistirse mediante **AES-256 (Fernet / criptografía simétrica)**. La llave existe únicamente en las variables de entorno del servidor.
- **Protección contra abusos:**
  - **Rate Limiting:** Máximo de **3 peticiones por hora por IP** utilizando `slowapi`.
  - **Payload restringido:** Validación con **Pydantic**, limitando las entradas a **5,000 caracteres** para evitar abusos de memoria.
- **Arquitectura ultraligera:** Frontend en **HTML, CSS y JavaScript Vanilla**, servido directamente por FastAPI mediante `StaticFiles`, reduciendo el consumo de recursos frente a una SPA tradicional.

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/) (Python 3.11) + Uvicorn |
| **Base de Datos** | [MongoDB Atlas](https://www.mongodb.com/atlas) (Motor AsyncIO) |
| **Seguridad** | `cryptography` (Fernet / AES-256) + `slowapi` |
| **Frontend** | HTML5, CSS3, JavaScript Vanilla (ES6+) |
| **Contenerización** | Docker + Docker Compose |
| **Despliegue** | [Render](https://render.com/) |

---

## 🔄 Flujo de Datos y Seguridad

1. El usuario escribe un mensaje y presiona **"Sellar en la bóveda"**.
2. Se envía una petición `POST /api/vent` al backend.
3. FastAPI recibe el texto y lo cifra inmediatamente en memoria mediante **Fernet**.
4. El mensaje cifrado se almacena en la colección `vents` de MongoDB junto con el campo `createdAt` en UTC.
5. El índice **TTL** de MongoDB elimina automáticamente y de forma irreversible el documento cuando supera las **24 horas**.

---

# 🚀 Instalación y Ejecución Local

## Prerrequisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## 1. Clonar el repositorio

```bash
git clone https://github.com/PJimenezDev/vent-vault.git
cd vent-vault
```

## 2. Configurar las variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
MONGO_URI=mongodb://localhost:27017
ENCRYPTION_KEY=TuLlaveFernetGeneradaEnBase64=
```

Para generar una llave Fernet válida ejecuta:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

## 3. Levantar los contenedores

```bash
docker-compose up --build
```

## 4. Acceder a la aplicación

Abre tu navegador en:

```
http://localhost:8000
```

---

# 📁 Estructura del Proyecto

```text
vent-vault/
├── backend/
│   ├── frontend/
│   │   ├── app.js          # Lógica del cliente
│   │   ├── index.html      # Interfaz principal
│   │   └── style.css       # Estilos de la aplicación
│   ├── Dockerfile          # Imagen Docker del backend
│   ├── main.py             # API FastAPI y configuración
│   └── requirements.txt    # Dependencias de Python
├── .gitignore              # Archivos ignorados por Git
└── docker-compose.yml      # Orquestación de FastAPI + MongoDB
```

---

# 🔑 Variables de Entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `MONGO_URI` | Cadena de conexión a MongoDB (local o Atlas) | `mongodb+srv://user:pass@cluster.mongodb.net` |
| `ENCRYPTION_KEY` | Llave Fernet codificada en Base64 | `B-x3abc123DEF456ghi789jkl...=` |

---

# 🛡️ Seguridad

- No se almacenan cuentas de usuario.
- No existen sesiones persistentes.
- No se guardan tokens de autenticación.
- Los mensajes permanecen cifrados en la base de datos.
- La eliminación de mensajes se realiza mediante índices TTL nativos de MongoDB.

---

# 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**.

---

# ⚠️ Descargo de Responsabilidad

Este proyecto fue desarrollado como un **MVP funcional** con fines educativos y como demostración de prácticas de seguridad, cifrado y eliminación automática de datos.

Aunque los mensajes son eliminados automáticamente tras 24 horas mediante índices TTL de MongoDB, **no se garantiza la disponibilidad, respaldo ni recuperación de la información**. Evita utilizar esta aplicación para almacenar información crítica o sensible.
