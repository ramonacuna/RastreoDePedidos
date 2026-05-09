import os
import re
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Mock database of packages
mock_packages = {
    "TRK12345": {
        "status": "En reparto",
        "origin": "Bogotá, COL",
        "destination": "Medellín, COL",
        "estimatedDelivery": "2026-05-03",
        "events": [
            {"date": "2026-05-02 08:30", "location": "Medellín", "description": "El paquete está en reparto."},
            {"date": "2026-05-01 14:15", "location": "Bogotá", "description": "El paquete salió del centro de distribución."},
            {"date": "2026-04-30 09:00", "location": "Bogotá", "description": "Paquete recibido en la agencia de origen."}
        ]
    },
    "TRK98765": {
        "status": "En tránsito",
        "origin": "Cali, COL",
        "destination": "Barranquilla, COL",
        "estimatedDelivery": "2026-05-05",
        "events": [
            {"date": "2026-05-02 10:00", "location": "Pereira", "description": "En tránsito hacia destino."},
            {"date": "2026-05-01 18:45", "location": "Cali", "description": "El paquete salió del centro de distribución."},
            {"date": "2026-05-01 08:30", "location": "Cali", "description": "Paquete documentado en origen."}
        ]
    },
    "TRK11111": {
        "status": "Entregado",
        "origin": "Cartagena, COL",
        "destination": "Cartagena, COL",
        "estimatedDelivery": "2026-05-01",
        "events": [
            {"date": "2026-05-01 16:20", "location": "Cartagena", "description": "Paquete entregado al destinatario."},
            {"date": "2026-05-01 09:10", "location": "Cartagena", "description": "En reparto."},
            {"date": "2026-04-30 14:00", "location": "Cartagena", "description": "Recibido en centro logístico local."}
        ]
    },
    "TRK00001": {
        "status": "En tránsito",
        "origin": "Manizales, COL",
        "destination": "Santa Marta, COL",
        "estimatedDelivery": "2026-05-06",
        "events": [
            {"date": "2026-05-02 15:00", "location": "Manizales", "description": "En procesamiento."},
            {"date": "2026-05-02 12:00", "location": "Manizales", "description": "Paquete recibido en origen."},
            {"date": "2026-05-02 09:00", "location": "Manizales", "description": "Guía creada electrónicamente."}
        ]
    },
    "TRK00002": {
        "status": "En reparto",
        "origin": "Bucaramanga, COL",
        "destination": "Cúcuta, COL",
        "estimatedDelivery": "2026-05-02",
        "events": [
            {"date": "2026-05-02 09:30", "location": "Cúcuta", "description": "En reparto local."},
            {"date": "2026-05-02 07:00", "location": "Cúcuta", "description": "Llegada a oficina de destino."},
            {"date": "2026-05-01 19:45", "location": "Bucaramanga", "description": "Saliendo de centro de acopio."}
        ]
    },
    "TRK00003": {
        "status": "Entregado",
        "origin": "Pereira, COL",
        "destination": "Armenia, COL",
        "estimatedDelivery": "2026-04-28",
        "events": [
            {"date": "2026-04-28 14:00", "location": "Armenia", "description": "Entregado satisfactoriamente."},
            {"date": "2026-04-28 09:30", "location": "Armenia", "description": "En reparto en la ciudad de destino."},
            {"date": "2026-04-27 18:00", "location": "Pereira", "description": "Saliendo del centro de acopio de origen."}
        ]
    },
    "TRK00004": {
        "status": "En tránsito",
        "origin": "Ibagué, COL",
        "destination": "Villavicencio, COL",
        "estimatedDelivery": "2026-05-07",
        "events": [
            {"date": "2026-05-02 14:30", "location": "Bogotá", "description": "En tránsito por punto de control principal."},
            {"date": "2026-05-01 22:15", "location": "Ibagué", "description": "Paquete procesado en centro logístico."},
            {"date": "2026-05-01 11:00", "location": "Ibagué", "description": "Saliendo de origen."}
        ]
    },
    "TRK00005": {
        "status": "En reparto",
        "origin": "Neiva, COL",
        "destination": "Florencia, COL",
        "estimatedDelivery": "2026-05-02",
        "events": [
            {"date": "2026-05-02 08:00", "location": "Florencia", "description": "Asignado a mensajero."},
            {"date": "2026-05-01 20:45", "location": "Florencia", "description": "Recibido en instalación de entrega."},
            {"date": "2026-05-01 07:30", "location": "Neiva", "description": "Despachado desde sucursal de origen."}
        ]
    },
    "TRK00006": {
        "status": "En tránsito",
        "origin": "Sincelejo, COL",
        "destination": "Montería, COL",
        "estimatedDelivery": "2026-05-04",
        "events": [
            {"date": "2026-05-02 11:10", "location": "Sahagún", "description": "En tránsito hacia destino final."},
            {"date": "2026-05-01 16:00", "location": "Sincelejo", "description": "En bodega central."},
            {"date": "2026-05-01 09:20", "location": "Sincelejo", "description": "Recibido en punto de admisión."}
        ]
    },
    "TRK00007": {
        "status": "Entregado",
        "origin": "Pasto, COL",
        "destination": "Ipiales, COL",
        "estimatedDelivery": "2026-04-30",
        "events": [
            {"date": "2026-04-30 11:30", "location": "Ipiales", "description": "Recibido por el portero."},
            {"date": "2026-04-30 08:00", "location": "Ipiales", "description": "En ruta de entrega local."},
            {"date": "2026-04-29 17:45", "location": "Pasto", "description": "Despachado de centro de distribución."}
        ]
    },
    "TRK00008": {
        "status": "En tránsito",
        "origin": "Quibdó, COL",
        "destination": "Medellín, COL",
        "estimatedDelivery": "2026-05-08",
        "events": [
            {"date": "2026-05-03 08:15", "location": "Ciudad Bolívar", "description": "En tránsito terrestre."},
            {"date": "2026-05-02 21:00", "location": "Quibdó", "description": "Procesado y listo para despacho."},
            {"date": "2026-05-02 14:00", "location": "Quibdó", "description": "Recogido en domicilio."}
        ]
    },
    "TRK00009": {
        "status": "En reparto",
        "origin": "Tunja, COL",
        "destination": "Sogamoso, COL",
        "estimatedDelivery": "2026-05-02",
        "events": [
            {"date": "2026-05-02 10:15", "location": "Sogamoso", "description": "En camioneta de entrega."},
            {"date": "2026-05-02 06:30", "location": "Sogamoso", "description": "Llegada a terminal de distribución."},
            {"date": "2026-05-01 19:20", "location": "Tunja", "description": "Salida de terminal de origen."}
        ]
    },
    "TRK00010": {
        "status": "En tránsito",
        "origin": "Riohacha, COL",
        "destination": "Valledupar, COL",
        "estimatedDelivery": "2026-05-05",
        "events": [
            {"date": "2026-05-03 10:40", "location": "Maicao", "description": "En tránsito por punto intermedio."},
            {"date": "2026-05-02 16:50", "location": "Riohacha", "description": "Enviado hacia destino."},
            {"date": "2026-05-02 09:00", "location": "Riohacha", "description": "Paquete documentado."}
        ]
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/track/<tracking_number>', methods=['GET'])
def track_package(tracking_number):
    tracking_number = tracking_number.strip().upper()
    
    # Input sanitization and validation
    if not re.match(r'^[A-Z0-9]{5,15}$', tracking_number):
        return jsonify({"success": False, "message": "Formato de número de guía inválido."}), 400
        
    package_info = mock_packages.get(tracking_number)
    
    if package_info:
        return jsonify({"success": True, "data": package_info})
    else:
        return jsonify({"success": False, "message": "Número de guía no encontrado."}), 404

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
