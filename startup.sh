if [ ! -d "venv" ]; then
    echo "[*] Virtual Environment Not Found, creating one now..."
    python3 -m venv venv
    echo "[*] Activating Virtual Environment"
    source venv/bin/activate
    #pip install -r requirements.txt
else
    echo "[+] Virtual Environment Detected!"
    echo "[*] Activating Virtual Environment"
    source venv/bin/activate
fi