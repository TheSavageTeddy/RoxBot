import sys
import subprocess
import requests
import time


def start_server():
	minecraft_server = subprocess.Popen(["java", "-Dfile.encoding=UTF-8", "-Xmx3G", "-jar", "spigot-1.8.8.jar"], cwd="/home/ronan/Server/BedWars") #java -Dfile.encoding=UTF-8 -Xmx3G -jar 
	ngrok = subprocess.Popen(["./ngrok", "tcp", "-region", "au", "25565"], cwd="/home/ronan/")
	return {"Minecraft":minecraft_server.pid, "ngrok":ngrok.pid}

def get_ip():
	#curl --silent http://127.0.0.1:4040/api/tunnels | jq '.tunnels[0].public_url'
    resp = requests.get(url="http://127.0.0.1:4040/api/tunnels")
    dictResp = resp.json()
    return dictResp["tunnels"][0]["public_url"].replace("tcp://", "")

if __name__ == "__main__":
	get_ip()