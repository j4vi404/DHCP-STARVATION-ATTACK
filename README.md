# DHCP Starvation Attack
Network Security Tool  

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
<img width="1618" height="867" alt="Screenshot 2026-02-10 215617" src="https://github.com/user-attachments/assets/d15c4ac2-4eb8-469b-a3b4-6a0081bf4457" />

---
- **Pool DHCP antes del ataque**
<img width="1077" height="327" alt="image" src="https://github.com/user-attachments/assets/c32b5303-e3dc-456a-afa1-4031aadc56b1" />

---

- **Ejecución del ataque DHCP Starvation**
 <img width="766" height="340" alt="image" src="https://github.com/user-attachments/assets/360c5d27-d2b8-4f22-b392-7086b02a83a3" />
 
---
- **Pool DHCP agotado (100% usado)**
<img width="1056" height="384" alt="image" src="https://github.com/user-attachments/assets/de6d7bf1-2a2d-4d60-8a9c-ca39f390b05a" />

---

- **Tráfico DHCP masivo en Wireshark**
<img width="847" height="559" alt="image" src="https://github.com/user-attachments/assets/d2ab6bde-7b3e-4a8b-8c57-f1d3b10715af" />

---
- **Cliente sin poder obtener IP**
<img width="796" height="172" alt="image" src="https://github.com/user-attachments/assets/b5da3bbc-18e2-4613-a61e-ef2ba0bdd876" />

---

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
git clone https://github.com/j4vi404/DHCP-STARVATION-ATTACK.git
cd DHCP-Starvation
chmod +x  DHCP_Starvation.py
sudo python3 DHCP_Starvation.py
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

**FASE 1: DETECCIÓN **
- Alerta: Pool >80%
- Verificar: `show ip dhcp snooping statistics`

**FASE 2: CONTENCIÓN **
- Shutdown puerto atacante
- Preservar evidencia

**FASE 3: ERRADICACIÓN **
- `clear ip dhcp binding *`
- Desconectar atacante

**FASE 4: RECUPERACIÓN (15-30 min)**
- Renovar DHCP en clientes
- Monitoreo intensivo

**FASE 5: MEJORAS **
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

*Última actualización: Febrero 2026*
