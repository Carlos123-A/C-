import requests
import time

URL = "http://localhost:3000/" 
CHECK_INTERVAL = 60  

def monitor_website(url):
    while True:
        try:
            response = requests.get(url)
            status_code = response.status_code
            
            print(f"El sitio web {url} respondió con un código de estado {status_code}.")
        
        except requests.RequestException as e:
            print(f"Error al intentar acceder al sitio web {url}: {e}")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_website(URL)
