import asyncio
import sqlite3

from httpx import ASGITransport, AsyncClient

from src.infrastructure.fastapi.app import app


async def run_e2e_test() -> None:
    print("🚀 Probando envío de Lead End-to-End local...")
    payload = {
        "name": "Carlos Gomez",
        "firstName": "Carlos",
        "lastName": "Gomez",
        "email": "carlos.gomez@empresa-pilar.com.ar",
        "phone": "+54 11 4433 2211",
        "company": "Industria Plástica Pilar S.A.",
        "comment": "Hola Agustín, necesitamos mantenimiento preventivo en celdas MT 13.2kV y revisión de 2 variadores Schneider Altivar en nuestra planta de Pilar.",
        "preferredContactChannel": "whatsapp",
        "pageLocation": "https://datamaq.com.ar/cobertura/pilar",
        "trafficSource": "Google Search - Mantenimiento electrico Pilar",
        "userAgent": "Mozilla/5.0 (Test E2E Runner)",
        "geographicLocation": "Pilar, Buenos Aires",
    }

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/contact", json=payload)

    print(f"Status HTTP: {response.status_code}")
    print(f"Respuesta API: {response.json()}")

    # Verificar en la base de datos SQLite data/leads.db
    conn = sqlite3.connect("data/leads.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, company, comment, created_at FROM leads ORDER BY created_at DESC LIMIT 1;")
    row = cursor.fetchone()
    conn.close()

    print("\n📦 Último Lead registrado en data/leads.db:")
    if row:
        print(f" - ID: {row[0]}")
        print(f" - Nombre: {row[1]}")
        print(f" - Email: {row[2]}")
        print(f" - Empresa: {row[3]}")
        print(f" - Consulta: {row[4]}")
        print(f" - Fecha: {row[5]}")
        print("\n✅ ¡Flujo End-to-End verificado con ÉXITO!")
    else:
        print("❌ Error: No se encontró el lead en data/leads.db")


if __name__ == "__main__":
    asyncio.run(run_e2e_test())
