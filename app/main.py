from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI(title="Modulo RRHH - ERP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

# --- REVISA TU AZURE ---
# Ve a la pestaña 'Consume' en Azure ML y pega los datos aquí
AZURE_URL = "xxxxx"
AZURE_TOKEN = "xxxx"

class EmpleadoData(BaseModel):
    edad: int
    salario: float
    nivel_satisfaccion: int
    horas_extras: int

@app.get("/")
def home():
    return {"status": "ERP RRHH Online", "ia_connected": True}

@app.post("/analizar-fuga")
async def analizar_fuga(data: EmpleadoData):
    payload = {
        "data": [[data.edad, data.salario, data.nivel_satisfaccion, data.horas_extras]]
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AZURE_TOKEN}"
    }

    try:
        response = requests.post(AZURE_URL, json=payload, headers=headers)
        resultado = response.json()
        riesgo = "ALTO" if resultado[0] == 1 else "BAJO"
        return {"riesgo": riesgo, "detalle": "Analizado por Azure ML"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))