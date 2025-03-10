# /app.py
from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', scan_output="Esperando el escaneo...")

@app.route('/monitor', methods=['POST'])
def monitor():
    # Aquí deberías implementar la lógica para el monitoreo de tráfico
    # Este es solo un ejemplo de cómo capturar la salida y redirigir.
    return render_template('index.html', scan_output="Monitoreo de tráfico iniciado.")

@app.route('/scan', methods=['POST'])
def scan():
    try:
        target_ip = request.form['target_ip']
        interval = int(request.form['interval'])

        # Ejecutamos el escaneo de puertos usando subprocess
        output = subprocess.run(["nmap", "-p", "1-1000", target_ip], capture_output=True, text=True)
        
        # Pasamos la salida del escaneo al frontend
        return render_template('index.html', scan_output=output.stdout)
    except Exception as e:
        return render_template('index.html', scan_output=f"Error al realizar el escaneo: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
