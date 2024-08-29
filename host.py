import psutil
import time

CHECK_INTERVAL = 10  

def monitor_system():
    while True:
        cpu_percent = psutil.cpu_percent(interval=1)
        
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.used

        print(f"Uso de CPU: {cpu_percent:.2f}%")
        print(f"Uso de Memoria: {memory_usage / 1024 / 1024:.2f}MB")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_system()
