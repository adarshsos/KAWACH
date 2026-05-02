import platform
import psutil
import subprocess

def scan_device() -> dict:
    """
    Advanced Device & Network Scanner for KAWACH.
    Performs REAL scans on the host operating system (Windows/Linux/Mac).
    """
    risks = 0
    risk_details = []
    
    os_system = platform.system()
    os_release = platform.release()
    system_update = f"{os_system} {os_release}"
    dev_mode = "Disabled"
    current_wifi = "Ethernet / Unknown"
    malicious_apps = 0
    interfaces = []

    # 1. Developer Mode Check (Windows Registry)
    if os_system == "Windows":
        import winreg
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock")
            value, _ = winreg.QueryValueEx(key, "AllowDevelopmentWithoutDevLicense")
            if value == 1:
                dev_mode = "Enabled"
                risks += 1
                risk_details.append("Windows Developer Mode is Enabled (Potential Security Risk)")
            winreg.CloseKey(key)
        except Exception:
            pass # Key doesn't exist, meaning it's disabled

    # 2. Network Interfaces & Wi-Fi Security Protocol Check
    try:
        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            for addr in interface_addresses:
                if str(addr.family) == 'AddressFamily.AF_INET':
                    interfaces.append({"name": interface_name, "ip": addr.address})
    except Exception:
        pass

    if os_system == "Windows":
        try:
            output = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces'], stderr=subprocess.STDOUT).decode('utf-8', errors='ignore')
            for line in output.split('\n'):
                if "Authentication" in line and "Network type" not in line:
                    auth_type = line.split(':')[1].strip()
                    current_wifi = auth_type
                    if auth_type == "Open":
                        risks += 2
                        risk_details.append("Unsafe Network Protocol Detected: Open/Unencrypted Wi-Fi")
                    break
        except Exception:
            pass

    # 3. Running Process Scan (Checking for active packet sniffers/hacking tools)
    try:
        suspicious_processes = ['wireshark.exe', 'nmap.exe', 'netcat.exe', 'nc.exe', 'cain.exe']
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] and proc.info['name'].lower() in suspicious_processes:
                malicious_apps += 1
                risks += 1
                risk_details.append(f"Suspicious network analysis tool running: {proc.info['name']}")
    except Exception:
        pass

    # 4. Unsecured Open Ports Check
    try:
        connections = psutil.net_connections(kind='inet')
        # Check for FTP(21), Telnet(23), HTTP(80) listening/established
        unsecured_ports = [conn.laddr.port for conn in connections if conn.laddr.port in (21, 23, 80)]
        if unsecured_ports:
            unique_ports = list(set(unsecured_ports))
            risks += len(unique_ports)
            risk_details.append(f"Detected open unsecured protocol ports: {unique_ports}")
    except Exception:
        pass
        
    return {
        "device_risks": risks,
        "risk_details": risk_details,
        "network_secure": "Open" not in current_wifi,
        "advanced_metrics": {
            "dev_mode": dev_mode,
            "system_update": system_update,
            "apps_scanned": len(psutil.pids()), # Number of running processes
            "malicious_apps": malicious_apps,
            "wifi_protocol": current_wifi,
            "active_interfaces": interfaces
        }
    }
