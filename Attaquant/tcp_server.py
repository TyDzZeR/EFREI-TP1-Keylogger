import socket

HOST = '0.0.0.0'
PORT = 9000

print(f"[*] SERVEUR TCP RAW en écoute sur {PORT}...")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        with conn:
            data = conn.recv(1024)
            if data:
                print(f"[REÇU TCP] {data.decode('utf-8')}")
