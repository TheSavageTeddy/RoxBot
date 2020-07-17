import sys
import subprocess
import requests


def start_server():
	minecraft_server = subprocess.Popen(["java", "-jar", "spigot-1.8.8-R0.1-SNAPSHOT-latest.jar"], cwd="/home/ronan/Server/BedWarsOnly") 
	ngrok = subprocess.Popen(["./ngrok", "tcp", "25565"], cwd="/home/ronan/")

def get_ip():
	#curl --silent http://127.0.0.1:4040/api/tunnels | jq '.tunnels[0].public_url'
    resp = requests.get(url="http://127.0.0.1:4040/api/tunnels")
    dictResp = resp.json()
    return dictResp["tunnels"][0]["public_url"].replace("tcp://", "")

if __name__ == "__main__":
	get_ip()