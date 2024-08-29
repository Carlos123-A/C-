import docker
import time

CONTAINER_NAME = "op"
CHECK_INTERVAL = 20

def monitor_container(container_name):
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
        stats = container.stats(stream=False)

        cpu_usage = stats['cpu_stats']['cpu_usage']['total_usage']
        prev_cpu_usage = stats['precpu_stats']['cpu_usage']['total_usage']

        delta_cpu_usage = cpu_usage - prev_cpu_usage
        cpu_percentage = (delta_cpu_usage / (stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage'])) * 100 if stats['cpu_stats']['system_cpu_usage'] > stats['precpu_stats']['system_cpu_usage'] else 0

        memory_usage = stats['memory_stats']['usage']
        memory_limit = stats['memory_stats']['limit']

        print("-------------------------------------")
        print(f"Consumo de CPU del contenedor: {cpu_percentage:.2f}%")
        print(f"Uso de Memoria del contenedor: {memory_usage} bytes")
        print(f"Límite de Memoria del contenedor: {memory_limit} bytes")
        print("-------------------------------------")
         
    except docker.errors.NotFound:
        print(f"Contenedor '{container_name}' no encontrado.")
    except KeyError as e:
        print(f"Clave faltante en las estadísticas: {e}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    while True:
        monitor_container(CONTAINER_NAME)
        time.sleep(CHECK_INTERVAL)
