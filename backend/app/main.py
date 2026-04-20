from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from backend.app.core.database import engine, Base
from backend.app.api import auth, personas, mascotas, clinica, billing

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Clínica Veterinaria API", version="1.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local testing, allow all. In production, restrict this.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(personas.router)
app.include_router(mascotas.router)
app.include_router(clinica.router)
app.include_router(billing.router)

# Serve Frontend
app.mount("/ui", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def read_root():
    return RedirectResponse(url="/ui/index.html")
