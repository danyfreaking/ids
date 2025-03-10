# monitor.py
import scapy.all as scapy
from scanner import detect_port_scan, detect_ping

# Función para obtener las interfaces de red activas
def get_active_interface():
    interfaces = scapy.get_if_list()  # Obtiene una lista de todas las interfaces de red
    for iface in interfaces:
        if iface.lower() in ['ethernet', 'wi-fi', 'en0', 'eth0']:  # Nombres comunes de interfaces
            return iface
    return None  # Si no se encuentra ninguna, retorna None

# Monitorear tráfico de red en una interfaz específica
def sniff_traffic_iface(iface):
    print(f"\n[🔍] Monitoreando tráfico de red en la interfaz {iface}...\n")
    scapy.sniff(filter="", prn=process_packet, store=False, iface=iface, timeout=10)  # Filtrado sin restricciones, captura todo

# Procesar cada paquete y pasarlo a la detección
def process_packet(packet):
    detect_port_scan(packet)  # Detectar escaneo de puertos
    detect_ping(packet)       # Detectar pings ICMP
