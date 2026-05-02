# Sistema de Rastreo de Envíos 📦

Aplicación web moderna y dinámica para consultar el estado y la ubicación de los envíos de paquetes. Construida con **Flask** en el backend y **HTML/CSS/JS** en el frontend para ofrecer una interfaz premium, responsiva y con modo oscuro integrado.

## Características

- 🔍 **Búsqueda Dinámica**: Ingresa el número de guía para consultar el estado.
- 🎨 **Diseño Premium**: Interfaz moderna (glassmorfismo), modo oscuro, animaciones fluidas.
- 🚚 **Animación de Progreso**: Muestra un camión moviéndose a lo largo de una barra de progreso de acuerdo al estado del paquete.
- 📱 **Responsivo**: Se adapta a dispositivos móviles y computadoras de escritorio.

## Requisitos Previos

- **Python 3.x** instalado en tu sistema.

## Instrucciones para Ejecutar Localmente

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/ramonacuna/RastreoDePedidos.git
   cd RastreoDePedidos
   ```

2. **Crear un entorno virtual (recomendado)**:
   - **En Windows**:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **En macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Instalar las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar el servidor**:
   ```bash
   python app.py
   ```

5. **Ejecutar con uv (Recomendado por velocidad)**:
   Si prefieres usar [uv](https://github.com/astral-sh/uv), puedes correr la aplicación directamente instalando las dependencias en una sola línea:
   ```bash
   uv run --with flask python app.py
   ```

6. **Acceder a la aplicación**:
   Abre tu navegador web y visita: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Datos de Prueba

Dado que actualmente la aplicación funciona con datos simulados (mock data), puedes usar los siguientes números de guía de prueba para visualizar los distintos estados:

| Número de Guía | Estado | Descripción del Flujo |
| :--- | :--- | :--- |
| **`TRK12345`** | *En reparto* | Muestra el paquete avanzando, actualmente en reparto de Bogotá a Medellín. |
| **`TRK98765`** | *En tránsito* | Muestra el paquete en ruta (a la mitad), viajando de Cali a Barranquilla. |
| **`TRK11111`** | *Entregado* | Muestra el paquete totalmente completado y entregado en Cartagena. |
| **`TRK00001`** | *En tránsito* | Manizales a Santa Marta. |
| **`TRK00002`** | *En reparto* | Bucaramanga a Cúcuta. |
| **`TRK00003`** | *Entregado* | Pereira a Armenia. |
| **`TRK00004`** | *En tránsito* | Ibagué a Villavicencio. |
| **`TRK00005`** | *En reparto* | Neiva a Florencia. |
| **`TRK00006`** | *En tránsito* | Sincelejo a Montería. |
| **`TRK00007`** | *Entregado* | Pastos a Ipiales. |
| **`TRK00008`** | *En tránsito* | Quibdó a Medellín. |
| **`TRK00009`** | *En reparto* | Tunja a Sogamoso. |
| **`TRK00010`** | *En tránsito* | Riohacha a Valledupar. |

Si ingresas cualquier otro número, la aplicación mostrará un mensaje indicando que el número de guía no fue encontrado.
