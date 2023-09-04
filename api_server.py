# api_server.py
from flask import Flask, request, jsonify

app = Flask(__name__)
should_run = True

@app.route('/receive_data', methods=['POST'])
def receive_data():
    from main import processFIInputJSON  # Moved the import here to avoid circular import
    incoming_data = request.json
    processFIInputJSON(incoming_data)
    return jsonify({"status": "success"})

@app.route('/stop', methods=['POST'])
def stop_server():
    global should_run
    should_run = False
    return "Server stopping"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

