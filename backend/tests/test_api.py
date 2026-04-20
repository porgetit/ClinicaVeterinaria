import pytest
from datetime import date

def test_login(client):
    response = client.post(
        "/auth/login",
        data={"username": "admin", "password": "admin123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_cliente(client, auth_header):
    cliente_data = {
        "nombre": "Juan Perez",
        "documento": "12345678",
        "telefono": "999888777",
        "email": "juan@example.com",
        "direccion": "Calle Falsa 123"
    }
    response = client.post("/personas/clientes", json=cliente_data, headers=auth_header)
    assert response.status_code == 200
    assert response.json()["nombre"] == "Juan Perez"
    return response.json()["id_cliente"]

def test_create_veterinario(client, auth_header):
    vet_data = {
        "nombre": "Dra. Smith",
        "documento": "VET001",
        "licencia": "LIC-999",
        "especialidad": "Cirugía"
    }
    response = client.post("/personas/veterinarios", json=vet_data, headers=auth_header)
    assert response.status_code == 200
    assert response.json()["licencia"] == "LIC-999"
    return response.json()["id_veterinario"]

def test_full_clinica_flow(client, auth_header):
    # 1. Create Cliente
    cliente_res = client.post("/personas/clientes", json={
        "nombre": "Maria Lopez", "documento": "87654321", "email": "maria@example.com"
    }, headers=auth_header)
    cliente_id = cliente_res.json()["id_cliente"]

    # 2. Create Veterinario
    vet_res = client.post("/personas/veterinarios", json={
        "nombre": "Dr. House", "documento": "MED001", "licencia": "L-123"
    }, headers=auth_header)
    vet_id = vet_res.json()["id_veterinario"]

    # 3. Create Mascota
    mascota_res = client.post("/mascotas/", json={
        "id_cliente": cliente_id,
        "nombre": "Firulais",
        "especie": "Perro",
        "fecha_nacimiento": "2020-01-01"
    }, headers=auth_header)
    mascota_id = mascota_res.json()["id_mascota"]
    assert mascota_res.status_code == 200

    # 4. Create Consulta
    consulta_res = client.post("/clinica/consultas", json={
        "id_veterinario": vet_id,
        "id_mascota": mascota_id,
        "fecha": str(date.today()),
        "hora": "10:00",
        "motivo": "Revisión general"
    }, headers=auth_header)
    assert consulta_res.status_code == 200
    consulta_id = consulta_res.json()["id_consulta"]

    # 5. Generate Factura
    factura_res = client.post("/facturacion/facturas", json={
        "id_cliente": cliente_id,
        "items": [
            {"concepto": "Consulta", "descripcion": "Cargo por revisión", "cantidad": 1, "precio_unitario": 50.0}
        ],
        "notas": "Prueba de sistema"
    }, headers=auth_header)
    assert factura_res.status_code == 200
    factura_id = factura_res.json()["id_factura"]
    total = factura_res.json()["total"]

    # 6. Process Payment (Polymorphism - Efectivo)
    pago_res = client.post(f"/facturacion/pagos/{factura_id}?tipo_pago=efectivo&monto={total}", json={
        "billete_mayor": 100.0,
        "vuelto": 100.0 - total,
        "numero_referencia": "REF-001"
    }, headers=auth_header)
    assert pago_res.status_code == 200
    assert pago_res.json()["tipo_pago"] == "efectivo"
