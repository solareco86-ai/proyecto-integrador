# Guía de Laboratorio: Capítulo 4 - De Script de Consola a Servicio Web con FastAPI

**Trayecto Formativo:** Procesamiento y Aprendizaje Automático (Nivel 0 — Nivelación)  
**Slug:** `procesamiento-aprendizaje-automatico-inicial`  
**Carga Horaria:** 5 horas (Práctica y Evaluación)  

---

## 4. Ejercicio 4.2: Tu Primer Endpoint de Cálculo `POST /operar` con OpenCode

En este ejercicio construirás un endpoint que reciba dos números y la operación a realizar en un cuerpo JSON (`POST`), utilizando **OpenCode** para generar las estructuras tipadas con Pydantic y el manejo de errores HTTP.

### Paso 1: Petición a OpenCode
Ejecuta el asistente **OpenCode** en la terminal para solicitar la implementación:

```bash
opencode "Agrega un endpoint 'POST /operar' en main.py usando FastAPI y Pydantic. Debe recibir 'operando_a' (float), 'operando_b' (float) y 'operacion' (str: 'suma', 'resta', 'multiplicacion', 'division'). Retorna el resultado estructurado en JSON con tipos explícitos."
```

### Paso 2: Código Esperado en `main.py`

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

class OperacionRequest(BaseModel):
    operando_a: float = Field(..., description="Primer número")
    operando_b: float = Field(..., description="Segundo número")
    operacion: str = Field(..., description="Tipo de operación: suma, resta, multiplicacion, division")

class OperacionResponse(BaseModel):
    operando_a: float
    operando_b: float
    operacion: str
    resultado: float

@app.post("/operar", response_model=OperacionResponse)
def operar(peticion: OperacionRequest):
    op = peticion.operacion.lower()
    a = peticion.operando_a
    b = peticion.operando_b

    if op == "suma":
        res = a + b
    elif op == "resta":
        res = a - b
    elif op == "multiplicacion":
        res = a * b
    elif op == "division":
        if b == 0:
            raise HTTPException(status_code=400, detail="No se puede dividir por cero.")
        res = a / b
    else:
        raise HTTPException(status_code=400, detail=f"Operación '{peticion.operacion}' no soportada.")

    return OperacionResponse(
        operando_a=a,
        operando_b=b,
        operacion=op,
        resultado=res
    )
```

### Paso 3: Verificación con cURL
Prueba el endpoint desde la terminal ejecutando:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/operar' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "operando_a": 15.5,
  "operando_b": 4.5,
  "operacion": "multiplicacion"
}'
```
Salida esperada:
```json
{
  "operando_a": 15.5,
  "operando_b": 4.5,
  "operacion": "multiplicacion",
  "resultado": 69.75
}
```
