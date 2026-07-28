import os
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorClient
from cryptography.fernet import Fernet
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Variables de entorno
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

if not ENCRYPTION_KEY:
    raise ValueError("ENCRYPTION_KEY is required in production environment.")

fernet = Fernet(ENCRYPTION_KEY.encode())

# Rate Limiting
limiter = Limiter(key_func=get_remote_address)
db_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_client
    db_client = AsyncIOMotorClient(MONGO_URI)
    db = db_client.ventvault
    
    await db.vents.create_index(
        "createdAt", 
        expireAfterSeconds=86400,
        name="vent_ttl_index"
    )
    yield
    db_client.close()

app = FastAPI(lifespan=lifespan)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

class VentRequest(BaseModel):
    text: str = Field(..., max_length=5000)

@app.post("/api/vent")
@limiter.limit("3/hour")
async def create_vent(request: Request, vent: VentRequest):
    try:
        encrypted_text = fernet.encrypt(vent.text.encode()).decode()
        
        db = db_client.ventvault
        await db.vents.insert_one({
            "encrypted_text": encrypted_text,
            "createdAt": datetime.now(timezone.utc) 
        })
        
        return {"status": "success", "message": "Bóveda cerrada. Se destruirá en 24 horas."}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Servir el frontend visual
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")