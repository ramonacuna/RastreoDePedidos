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
            {"date": "2026-05-01 18:45", "location": "Cali", "description": "El paquete salió del centro de distribución."}
        ]
    },
    "TRK11111": {
        "status": "Entregado",
        "origin": "Cartagena, COL",
        "destination": "Cartagena, COL",
        "estimatedDelivery": "2026-05-01",
        "events": [
            {"date": "2026-05-01 16:20", "location": "Cartagena", "description": "Paquete entregado al destinatario."},
            {"date": "2026-05-01 09:10", "location": "Cartagena", "description": "En reparto."}
        ]
    },
    "TRK00001": {
        "status": "En tránsito",
        "origin": "Manizales, COL",
        "destination": "Santa Marta, COL",
        "estimatedDelivery": "2026-05-06",
        "events": [
            {"date": "2026-05-02 12:00", "location": "Manizales", "description": "Paquete recibido en origen."},
            {"date": "2026-05-02 15:00", "location": "Manizales", "description": "En procesamiento."}
        ]
    },
    "TRK00002": {
        "status": "En reparto",
        "origin": "Bucaramanga, COL",
        "destination": "Cúcuta, COL",
        "estimatedDelivery": "2026-05-02",
        "events": [
            {"date": "2026-05-02 07:00", "location": "Cúcuta", "description": "Llegada a oficina de destino."},
            {"date": "2026-05-02 09:30", "location": "Cúcuta", "description": "En reparto local."}
        ]
    },
    "TRK00003": {
        "status": "Entregado",
        "origin": "Pereira, COL",
        "destination": "Armenia, COL",
        "estimatedDelivery": "2026-04-28",
        "events": [
            {"date": "2026-04-28 14:00", "location": "Armenia", "description": "Entregado satisfactoriamente."}
        ]
    },
    "TRK00004": {
        "status": "En tránsito",
        "origin": "Ibagué, COL",
        "destination": "Villavicencio, COL",
        "estimatedDelivery": "2026-05-07",
        "events": [
            {"date": "2026-05-01 11:00", "location": "Ibagué", "description": "Saliendo de origen."}
        ]
    },
    "TRK00005": {
        "status": "En reparto",
        "origin": "Neiva, COL",
        "destination": "Florencia, COL",
        "estimatedDelivery": "2026-05-02",
        "events": [
            {"date": "2026-05-02 08:00", "location": "Florencia", "description": "Asignado a mensajero."}
        ]
    },
    "TRK00006": {
        "status": "En tránsito",
        "origin": "Sincelejo, COL",
        "destination": "Montería, COL",
        "estimatedDelivery": "2026-05-04",
        "events": [
            {"date": "2026-05-01 16:00", "location": "Sincelejo", "description": "En bodega central."}
        ]
    },
    "TRK00007": {
        "status": "Entregado",
        "origin": "Pastos, COL",
        "destination": "Ipiales, COL",
        "estimatedDelivery": "2026-04-30",
        "events": [
            {"date": "2026-04-30 11:30", "location": "Ipiales", "description": "Recibido por el portero."}
        ]
    },
    "TRK00008": {
        "status": "En tránsito",
        "origin": "Quibdó, COL",
        "destination": "Medellín, COL",
        "estimatedDelivery": "2026-05-08",
        "events": [
            {"date": "2026-05-02 14:00", "location": "Quibdó", "description": "Recogido en domicilio."}
        ]
    },
    "TRK00009": {
        "status": "En reparto",
        "origin": "Tunja, COL",
        "destination": "Sogamoso, COL",
        "estimatedDelivery": "2026-05-02",
        "events": [
            {"date": "2026-05-02 10:15", "location": "Sogamoso", "description": "En camioneta de entrega."}
        ]
    },
    "TRK00010": {
        "status": "En tránsito",
        "origin": "Riohacha, COL",
        "destination": "Valledupar, COL",
        "estimatedDelivery": "2026-05-05",
        "events": [
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
    package_info = mock_packages.get(tracking_number)
    
    if package_info:
        return jsonify({"success": True, "data": package_info})
    else:
        return jsonify({"success": False, "message": "Número de guía no encontrado."}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
