import paramiko
import time
import json
import requests

# Configuraciones básicas
SERVER_IP = '192.168.0.28'  
SERVER_USER = 'your_user'     
PRIVATE_KEY_PATH = '/path/to/your/private/key'  
CONTAINER_NAME = 'op'         
CHECK_INTERVAL = 20           
WEBSITE_URL = 'http://example.com'  

def execute_command(ssh, command):
    """Ejecuta un comando en el servidor remoto a través de SSH y retorna la salida."""
    try:
        stdin, stdout, stderr = ssh.exec_command(command)
        return stdout.read().decode()
    except Exception as e:
        print(f"Error al ejecutar comando '{command}': {e}")
        return ""

def get_container_stats(ssh):
    """Obtiene estadísticas del contenedor Docker."""
    command = f"docker stats --no-stream --format '{{{{json .}}}}' {CONTAINER_NAME}"
    stats = execute_command(ssh, command)
    
    if stats:
        try:
            stats_json = json.loads(stats)
            print("Estadísticas del contenedor:")
            print(f"Uso de CPU: {stats_json.get('CPUPerc', 'N/A')}")
            print(f"Uso de Memoria: {stats_json.get('MemUsage', 'N/A')}")
        except json.JSONDecodeError:
            print("Error al analizar el JSON del contenedor.")

def get_host_stats(ssh):
    """Obtiene estadísticas del servidor host (uso de CPU y memoria)."""
    command = "top -bn1 | grep 'Cpu(s)' && free -m"
    stats = execute_command(ssh, command)

    if stats:
        try:
            cpu_usage_line = [line for line in stats.splitlines() if "Cpu(s)" in line]
            cpu_usage = cpu_usage_line[0].split()[1]  

            mem_usage_line = [line for line in stats.splitlines() if "Mem:" in line]
            mem_info = mem_usage_line[0].split()

            total_memory = mem_info[1]
            used_memory = mem_info[2]
            free_memory = mem_info[3]

            print("\nEstadísticas del servidor host:")
            print(f"Uso de CPU: {cpu_usage}%")
            print(f"Memoria Total: {total_memory} MB")
            print(f"Memoria Usada: {used_memory} MB")
            print(f"Memoria Libre: {free_memory} MB")
        except IndexError:
            print("Error al extraer las estadísticas del host.")

def check_website_status():
    """Verifica el estado de la URL del sitio web."""
    try:
        response = requests.get(WEBSITE_URL)
        if response.status_code == 200:
            print(f"\nLa página {WEBSITE_URL} está disponible. Estado: 200 OK")
        else:
            print(f"\nLa página {WEBSITE_URL} devolvió el estado: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"\nError al conectar con la página {WEBSITE_URL}: {e}")

def connect_ssh():
    """Establece una conexión SSH con el servidor."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        private_key = paramiko.RSAKey.from_private_key_file(PRIVATE_KEY_PATH)
        ssh.connect(SERVER_IP, username=SERVER_USER, pkey=private_key)
        return ssh
    except Exception as e:
        print(f"Error al conectar por SSH: {e}")
        return None

def main():
    ssh = connect_ssh()
    if ssh:
        while True:
            get_container_stats(ssh)
            get_host_stats(ssh)
            check_website_status()  
            time.sleep(CHECK_INTERVAL)
        ssh.close()

if __name__ == "__main__":
    main()
