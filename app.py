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
