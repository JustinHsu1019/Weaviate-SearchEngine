import requests
import time
import subprocess

def check_service():
    url = "http://localhost/api/"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            restart_service()
    except requests.RequestException:
        restart_service()

def restart_service():
    print("Service is down. Restarting service...")
    subprocess.run(["nohup", "python3", "Backend/api_docs.py", "&"])

if __name__ == "__main__":
    while True:
        check_service()
        time.sleep(600)
