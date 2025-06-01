import socket
import sys
from concurrent.futures import ThreadPoolExecutor

def banner_grabbing(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((ip, port))
            s.send(b"\n")
            banner = s.recv(1024).decode().strip()
            return banner if banner else "Nenhum banner recebido."
    except Exception:
        return "Não foi possível capturar o banner."

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            result = s.connect_ex((ip, port))
            if result == 0:
                banner = banner_grabbing(ip, port)
                print(f"[+] Porta {port} aberta - Banner: {banner}")
    except Exception:
        pass

def scan_ports(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(f"\n🌐 Escaneando: {domain} ({ip})\n")
        with ThreadPoolExecutor(max_workers=100) as executor:
            for port in range(20, 1025):
                executor.submit(scan_port, ip, port)
    except socket.gaierror:
        print("❌ Domínio inválido ou fora do ar.")
    except KeyboardInterrupt:
        print("\n⛔ Varredura interrompida pelo usuário.")
        sys.exit()

if __name__ == "__main__":
    dominio = input("Digite o domínio para escanear (ex: globo.com): ").strip()
    scan_ports(dominio)
