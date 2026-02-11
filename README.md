# DHCP Starvation Attack
🔧 Network Security Tool  
![Python](https://img.shields.io/badge/Python-3.7%2B-blue)

Herramienta automatizada para demostración de ataques DHCP Starvation en entornos de laboratorio controlados

## 📋 Tabla de Contenidos
- [Objetivo del Script](#-objetivo)
- [Capturas de Pantalla](#-capturas-de-pantalla)
- [Topología de Red](#-topología-de-red)
- [Parámetros Usados](#parámetros-usados)
- [Requisitos](#requisitos)
- [Medidas de Mitigación](#-medidas-de-mitigación)

## 🎯 Objetivo
El objetivo de este script es simular un ataque de **DHCP Starvation** para agotar el pool de direcciones IP del servidor DHCP mediante el envío masivo de solicitudes DHCP DISCOVER con MACs falsas, provocando denegación de servicio (DoS) que impide que clientes legítimos obtengan configuración de red, con fines exclusivamente educativos.

## 🖼️ Capturas de Pantalla

- **Topología de red del escenario**
  ![Topología](screenshots/topologia.png)

- **Pool DHCP antes del ataque**
  ![DHCP Before](screenshots/dhcp_pool_before.png)

- **Ejecución del ataque DHCP Starvation**
  ![Ataque](screenshots/ataque_starvation.png)

- **Pool DHCP agotado (100% usado)**
  ![Pool Exhausted](screenshots/pool_exhausted.png)

- **Tráfico DHCP masivo en Wireshark**
  ![Wireshark](screenshots/wireshark_flood.png)

- **Cliente sin poder obtener IP**
  ![Client Denied](screenshots/client_denied.png)

## DHCP Starvation - Pool Exhaustion Attack
Script de Python que utiliza Scapy para agotar el pool DHCP mediante solicitudes masivas con MACs aleatorias.


### Instalación
```bash
sudo apt update
sudo apt install python3 python3-pip -y
pip3 install scapy
```

### Uso
```bash
git clone https://github.com/tuusuario/DHCP-Starvation.git
cd DHCP-Starvation
chmod +x dhcp_starvation.py
sudo python3 dhcp_starvation.py
```

## Características
🎯 **Pool Exhaustion**: Agota todas las IPs disponibles  
🔄 **MAC Spoofing**: Genera MACs falsas únicas  
⚡ **Flood DHCP**: Envío masivo de DISCOVER  
📊 **Monitoreo**: Estadísticas en tiempo real  
🔧 **Configurable**: Velocidad y cantidad ajustables

## Cómo funciona
1. Genera MAC aleatoria única
2. Envía DHCP DISCOVER con MAC falsa
3. Servidor responde con DHCP OFFER
4. Repite hasta agotar el pool (191 IPs)
5. Clientes legítimos no pueden obtener IP (DoS)
---
## Autor
**ALEXIS JAVIER CRUZ MINYETE**

---
### Interfaces Principales

#### Kali Linux Atacante
| Interfaz | IP | Descripción |
|----------|-----|-------------|
| e0 | 15.0.7.2 | Interfaz de ataque |
| e1 | DHCP | Conexión Cloud |

#### R-SD DHCP Server
| Interfaz | IP | Pool DHCP |
|----------|-----|-----------|
| e0/0.20 | 15.0.7.1 | 15.0.7.0.2-254 |
| e0/1 | Cloud | — |

#### Switches ARISTA (SW-1, SW-2, SW-3)
| Switch | Vulnerabilidad |
|--------|----------------|
| SW-1 | ❌ Sin DHCP Snooping |
| SW-2 | ❌ Sin Rate Limiting |
| SW-3 | ❌ Sin Port Security |

---

## Parámetros Usados

### Configuración de Red
| Parámetro | Valor |
|-----------|-------|
| Red Objetivo | 15.0.7.0/24 |
| Servidor DHCP |  10.0.0.1 |
| Pool DHCP | 10.0.0.100 - 10.0.0.150 |
| Total IPs | 50 |
| Lease Time | 86400 seg (24h) |

### Parámetros del Ataque
| Parámetro | Valor |
|-----------|-------|
| Interfaz | eth0 |
| Velocidad | 100 paquetes/seg |
| Total Peticiones | 191 |
| MAC Spoofing | Aleatorio por petición |
| Puerto Origen | 68 (DHCP Client) |
| Puerto Destino | 67 (DHCP Server) |
| Protocolo | UDP |

---

### Permisos
- Privilegios root/sudo
- Interfaz en modo promiscuo
- Acceso a la red objetivo

### Preparación
```bash
# Configurar IP estática
sudo ip addr add 192.168.1.50/24 dev eth0

# Habilitar modo promiscuo
sudo ip link set eth0 promisc on
```

---

## 🛡️ Medidas de Mitigación

### Tabla de Riesgos y Controles

| ID | Riesgo | Severidad | Mitigación |
|----|--------|-----------|------------|
| R-001 | Pool Exhaustion DoS | **CRÍTICO** | DHCP Snooping + Rate Limiting (10 pkt/min) |
| R-002 | MAC Spoofing Masivo | **CRÍTICO** | Port Security (máx 3 MACs) |
| R-003 | DoS Total de Red | **CRÍTICO** | Pool reservado + DHCP redundante |
| R-004 | DHCP Flood | **ALTO** | Storm Control (10% broadcast) |
| R-005 | Falta de Detección | **ALTO** | IDS/IPS + Monitoreo pool >80% |

---

### Control 1: DHCP Snooping con Rate Limiting

**Cisco:**
```cisco
! Habilitar DHCP Snooping
Switch(config)# ip dhcp snooping
Switch(config)# ip dhcp snooping vlan 1,10,20

! Puerto trust (servidor DHCP)
Switch(config)# interface GigabitEthernet0/24
Switch(config-if)# ip dhcp snooping trust

! Puertos untrust con límite
Switch(config)# interface range GigabitEthernet0/1-23
Switch(config-if-range)# ip dhcp snooping limit rate 10
```

**Arista:**
```
switch(config)# ip dhcp snooping
switch(config)# ip dhcp snooping vlan 1,10,20
switch(config)# interface Ethernet24
switch(config-if-Et24)# ip dhcp snooping trust
switch(config)# interface Ethernet1-23
switch(config-if-Et1-23)# ip dhcp snooping limit rate 10 pps
```

---

### Control 2: Port Security

```cisco
Switch(config)# interface range GigabitEthernet0/1-23
Switch(config-if-range)# switchport port-security
Switch(config-if-range)# switchport port-security maximum 3
Switch(config-if-range)# switchport port-security violation shutdown
Switch(config-if-range)# switchport port-security mac-address sticky
```

---

### Control 3: Storm Control

```cisco
Switch(config)# interface range GigabitEthernet0/1-23
Switch(config-if-range)# storm-control broadcast level 10.00
Switch(config-if-range)# storm-control action shutdown
```

---

### Control 4: Dynamic ARP Inspection

```cisco
Switch(config)# ip arp inspection vlan 1,10,20
Switch(config)# ip arp inspection validate src-mac dst-mac ip
Switch(config)# interface GigabitEthernet0/24
Switch(config-if)# ip arp inspection trust
```

---

### Control 5: Monitoreo del Pool

**Script de monitoreo:**
```bash
#!/bin/bash
THRESHOLD=80
while true; do
    LEASES=$(grep -c "^lease" /var/lib/dhcp/dhcpd.leases)
    USAGE=$((LEASES * 100 / 191))
    echo "Pool: $USAGE%"
    [ $USAGE -ge $THRESHOLD ] && echo "⚠️ ALERT!"
    sleep 60
done
```

---

### Comandos de Verificación

```cisco
! Verificar DHCP Snooping
show ip dhcp snooping
show ip dhcp snooping binding
show ip dhcp snooping statistics

! Verificar Port Security
show port-security

! Verificar pool
show ip dhcp pool
show ip dhcp binding
```

---

### Plan de Respuesta a Incidentes

**FASE 1: DETECCIÓN (0-2 min)**
- Alerta: Pool >80%
- Verificar: `show ip dhcp snooping statistics`

**FASE 2: CONTENCIÓN (2-5 min)**
- Shutdown puerto atacante
- Preservar evidencia

**FASE 3: ERRADICACIÓN (5-15 min)**
- `clear ip dhcp binding *`
- Desconectar atacante

**FASE 4: RECUPERACIÓN (15-30 min)**
- Renovar DHCP en clientes
- Monitoreo intensivo

**FASE 5: MEJORAS (1-2 semanas)**
- Implementar todos los controles
- Capacitación del equipo

---

### Configuración Completa Recomendada

```cisco
! DHCP Snooping
ip dhcp snooping
ip dhcp snooping vlan 1,10,20

! Puerto servidor DHCP
interface GigabitEthernet0/24
 ip dhcp snooping trust
 ip arp inspection trust

! Puertos clientes
interface range GigabitEthernet0/1-23
 ip dhcp snooping limit rate 10
 switchport port-security
 switchport port-security maximum 3
 switchport port-security violation shutdown
 storm-control broadcast level 10.00
 ip verify source port-security

! DAI
ip arp inspection vlan 1,10,20
ip arp inspection validate src-mac dst-mac ip

! Logging
logging buffered informational
snmp-server enable traps port-security
```

---

**⚠️ Disclaimer**

Este proyecto es **exclusivamente para fines educativos**. El uso no autorizado es **ilegal**.

---

**📚 Referencias**
- RFC 2131 - DHCP
- Cisco DHCP Snooping Guide
- Arista EOS DHCP Snooping

**📧 Contacto:** alexis.minyete@example.com

---

*Última actualización: Febrero 2026*
