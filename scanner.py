# scanner.py
import time
import subprocess
import scapy.all as scapy

# Función para detectar un escaneo de puertos
def detect_port_scan(packet):
    if packet.haslayer(scapy.IP) and packet.haslayer(scapy.TCP):
        src_ip = packet[scapy.IP].src
        dst_ip = packet[scapy.IP].dst
        src_port = packet[scapy.TCP].sport
        dst_port = packet[scapy.TCP].dport

        # Lógica para detectar un escaneo de puertos
        if packet[scapy.TCP].flags == "S":  # Si el paquete tiene bandera SYN (inicio de conexión)
            print("\n" + "="*50)
            print("🚨🚨🚨  ¡ALERTA! Posible escaneo de puertos detectado  🚨🚨🚨")
            print("="*50)
            print(f"📍 Origen: {src_ip}:{src_port}   ➜   📍 Destino: {dst_ip}:{dst_port}")
            print("="*50 + "\n")

# Función para detectar pings ICMP
def detect_ping(packet):
    if packet.haslayer(scapy.IP) and packet.haslayer(scapy.ICMP):
        src_ip = packet[scapy.IP].src
        dst_ip = packet[scapy.IP].dst
        print("\n" + "="*50)
        print("🚨🚨🚨  ¡ALERTA! Posible ataque de Ping detectado  🚨🚨🚨")
        print("="*50)
        print(f"📍 Origen: {src_ip}   ➜   📍 Destino: {dst_ip}")
        print("="*50 + "\n")

# Función para escanear puertos con un límite de intentos
def scan_ports(target_ip, interval, max_attempts=5):
    attempts = 0  # Contador de intentos
    result = {"status": "success", "message": ""}
    
    while attempts < max_attempts:
        print(f"\n🔍 Escaneando puertos de {target_ip} (Intento {attempts + 1}/{max_attempts})...")
        try:
            scan_result = subprocess.run(["nmap", "-p", "1-1000", target_ip], capture_output=True, text=True)
            print(scan_result.stdout)

            # Verifica si encontró puertos abiertos
            if "open" in scan_result.stdout:
                result["message"] = "Puertos abiertos detectados:\n" + scan_result.stdout
            else:
                result["message"] = "No se encontraron puertos abiertos."
        except FileNotFoundError:
            result["status"] = "error"
            result["message"] = "Nmap no está instalado. Instálalo antes de ejecutar esta opción."
            break
        
        attempts += 1
        time.sleep(interval)
    
    return result
