import sys
import subprocess
import requests
import time

def start_server(server_type = None):
	print(f"Server type of {server_type}")
	if not server_type:
		minecraft_server = subprocess.Popen(["java", "-Xmx3G", "-jar", "spigot-1.8.8.jar"], cwd="/home/ronan/Server/BedWarsOnly") #java -Dfile.encoding=UTF-8 -Xmx3G -jar 
		ngrok = subprocess.Popen(["./ngrok", "tcp", "-region", "au", "25565"], cwd="/home/ronan/")
		return {"Minecraft":minecraft_server.pid, "ngrok":ngrok.pid}
	elif server_type == 'bedwars':
		minecraft_server = subprocess.Popen(["java", "-Xmx3G", "-jar", "spigot-1.8.8.jar"], cwd="/home/ronan/Server/BedWarsOnly") #java -Dfile.encoding=UTF-8 -Xmx3G -jar 
		ngrok = subprocess.Popen(["./ngrok", "tcp", "-region", "au", "25565"], cwd="/home/ronan/")
		return {"Minecraft":minecraft_server.pid, "ngrok":ngrok.pid}
	elif server_type == 'bedwars-beta':
		minecraft_server = subprocess.Popen(["java", "-Dfile.encoding=UTF-8", "-Xmx3G", "-jar", "spigot-1.8.8.jar"], cwd="/home/ronan/Server/BedWars") #java -Dfile.encoding=UTF-8 -Xmx3G -jar 
		ngrok = subprocess.Popen(["./ngrok", "tcp", "-region", "au", "25565"], cwd="/home/ronan/")
		return {"Minecraft":minecraft_server.pid, "ngrok":ngrok.pid}
	elif server_type == 'smp-tst':
		minecraft_server = subprocess.Popen(["java", "-Dfile.encoding=UTF-8", "-Xms1G", "-Xmx3G", "-jar", "spigot-1.16.1.jar", "nogui"], cwd="/home/ronan/Server/SMP") #java -Dfile.encoding=UTF-8 -Xmx3G -jar 
		ngrok = subprocess.Popen(["./ngrok", "tcp", "-region", "au", "25565"], cwd="/home/ronan/")
		return {"Minecraft":minecraft_server.pid, "ngrok":ngrok.pid}
	elif server_type == 'bedwars-cracked':
		minecraft_server = subprocess.Popen(["java", "-Dfile.encoding=UTF-8", "-Xmx3G", "-jar", "spigot-1.8.8.jar"], cwd="/home/ronan/Server/BedWarsCracked") #java -Dfile.encoding=UTF-8 -Xmx3G -jar 
		ngrok = subprocess.Popen(["./ngrok", "tcp", "-region", "au", "25565"], cwd="/home/ronan/")
		return {"Minecraft":minecraft_server.pid, "ngrok":ngrok.pid}


def start_server_smp():
	#minecraft_server = subprocess.Popen(["java", "-Dfile.encoding=UTF-8", "-Xmx3G", "-jar", "paper-114.jar"], cwd="/home/ronan/Server/SMP") #java -Dfile.encoding=UTF-8 -Xmx3G -jar 
	#ngrok = subprocess.Popen(["./ngrok", "tcp", "-region", "au", "25565"], cwd="/home/ronan/")
	#return {"Minecraft":minecraft_server.pid, "ngrok":ngrok.pid}
	return {"Minecraft":"", "ngrok":""}

def get_ip():
	#curl --silent http://127.0.0.1:4040/api/tunnels | jq '.tunnels[0].public_url'
	try:
		resp = requests.get(url="http://127.0.0.1:4040/api/tunnels")
		dictResp = resp.json()
		return dictResp["tunnels"][0]["public_url"].replace("tcp://", "")
	except:
		return None

if __name__ == "__main__":
	get_ip()