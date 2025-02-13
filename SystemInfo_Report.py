import os
import platform
import psutil
import socket
import subprocess
import wmi
import requests
import getpass, base64

# Konfigurasi Pastebin (Opsional)
PASTEBIN_API_KEY = "Pastebin Dev Key"
PASTEBIN_USERNAME = "Username"
PASTEBIN_PASSWORD = "Password"


def get_system_info():
    """ Mengambil informasi dasar sistem """
    info = {}

    # Hostname & OS
    info["Hostname"] = socket.gethostname()
    info["OS Name"] = platform.system()
    info["OS Version"] = platform.version()
    info["OS Build"] = platform.release()
    info["Architecture"] = platform.architecture()[0]
    info["System Type"] = "64-bit" if platform.architecture()[0] == "64bit" else "32-bit"

    # CPU Info
    info["Processor"] = platform.processor()
    info["CPU Cores"] = psutil.cpu_count(logical=False)
    info["Logical Processors"] = psutil.cpu_count(logical=True)

    # RAM Info
    virtual_memory = psutil.virtual_memory()
    info["Total RAM"] = f"{virtual_memory.total / (1024 ** 3):.2f} GB"
    info["Available RAM"] = f"{virtual_memory.available / (1024 ** 3):.2f} GB"

    # Storage Info
    disk_info = psutil.disk_usage('/')
    info["Total Disk"] = f"{disk_info.total / (1024 ** 3):.2f} GB"
    info["Free Disk"] = f"{disk_info.free / (1024 ** 3):.2f} GB"

    # BIOS Info (Windows Only)
    if os.name == "nt":
        c = wmi.WMI()
        bios = c.Win32_BIOS()[0]
        info["BIOS Version"] = bios.SMBIOSBIOSVersion
        info["System Manufacturer"] = c.Win32_ComputerSystem()[0].Manufacturer
        info["System Model"] = c.Win32_ComputerSystem()[0].Model

    return info


def get_network_info():
    """ Mengambil informasi jaringan & koneksi aktif """
    info = {}

    # IP Address
    info["Local IP"] = socket.gethostbyname(socket.gethostname())

    # Public IP (Gunakan API eksternal)
    try:
        info["Public IP"] = requests.get("https://api64.ipify.org?format=json").json()["ip"]
    except:
        info["Public IP"] = "Tidak dapat mengambil IP publik"

    # MAC Address
    net_info = psutil.net_if_addrs()
    for interface, addrs in net_info.items():
        for addr in addrs:
            if addr.family == psutil.AF_LINK:
                info[f"MAC {interface}"] = addr.address

    # Koneksi Aktif
    connections = psutil.net_connections(kind='inet')
    active_ports = []
    for conn in connections:
        if conn.status == "LISTEN":
            active_ports.append(f"Port {conn.laddr.port} (Listening)")

    info["Open Ports"] = ", ".join(active_ports) if active_ports else "No Open Ports"

    # Firewall Status (Windows Only)
    if os.name == "nt":
        firewall_status = subprocess.run(
            ["netsh", "advfirewall", "show", "allprofiles"], capture_output=True, text=True
        ).stdout
        info["Firewall Status"] = firewall_status.strip()

    return info


def get_process_info():
    """ Mengambil daftar proses yang sedang berjalan """
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'status']):
        processes.append(f"{proc.info['name']} (PID: {proc.info['pid']}) - {proc.info['status']}")

    return processes


def check_security():
    """ Mengecek user admin, Hyper-V, & layanan mencurigakan """
    security = {}

    # Cek apakah user memiliki akses admin (Windows)
    security["Current User"] = getpass.getuser()
    security["Is Admin"] = "Yes" if os.name == "nt" and "S-1-5-32-544" in subprocess.getoutput(
        "whoami /groups") else "No"

    # Hyper-V Requirements (Windows Only)
    if os.name == "nt":
        hyper_v = subprocess.run(["systeminfo"], capture_output=True, text=True).stdout
        if "Hyper-V Requirements" in hyper_v:
            security["Hyper-V Supported"] = "Yes"
        else:
            security["Hyper-V Supported"] = "No"

    return security


def generate_report():
    """ Menghasilkan laporan lengkap """
    report = ""

    # Tambahkan Informasi Sistem
    report += "=== SYSTEM INFO ===\n"
    for key, value in get_system_info().items():
        report += f"{key}: {value}\n"

    # Tambahkan Informasi Jaringan
    report += "\n=== NETWORK INFO ===\n"
    for key, value in get_network_info().items():
        report += f"{key}: {value}\n"

    # Tambahkan Proses yang Berjalan
    report += "\n=== RUNNING PROCESSES ===\n"
    for proc in get_process_info():
        report += f"{proc}\n"

    # Tambahkan Info Keamanan
    report += "\n=== SECURITY CHECK ===\n"
    for key, value in check_security().items():
        report += f"{key}: {value}\n"

    return report


def send_to_pastebin(title, content):
    """ Mengirim laporan ke Pastebin """
    login_url = "https://pastebin.com/api/api_login.php"
    login_data = {
        "api_dev_key": PASTEBIN_API_KEY,
        "api_user_name": PASTEBIN_USERNAME,
        "api_user_password": PASTEBIN_PASSWORD
    }

    login_response = requests.post(login_url, data=login_data)
    api_user_key = login_response.text

    encoded_contents = base64.b64encode(content.encode('utf-8')).decode('utf-8')

    if "Bad API request" in api_user_key:
        print(f"Login gagal: {api_user_key}")
        return

    paste_data = {
        "api_paste_name": title,
        "api_paste_code": encoded_contents,
        "api_dev_key": PASTEBIN_API_KEY,
        "api_user_key": api_user_key,
        "api_option": 'paste',
        "api_paste_private": 1,  # 0 = Public, 1 = Unlisted, 2 = Private
    }

    paste_response = requests.post("https://pastebin.com/api/api_post.php", data=paste_data)
    if paste_response.status_code == 200:
        print(f"Laporan berhasil diunggah ke Pastebin: {paste_response.text}")
    else:
        print(f"Gagal mengunggah laporan: {paste_response.status_code}")


# Eksekusi Skrip
report = generate_report()
print(report)

# Kirim ke Pastebin (Opsional)
send_to_pastebin("System Report", report)
