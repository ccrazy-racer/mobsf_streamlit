from flask import Flask, request, jsonify
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
import json
import fetch_api_key

app = Flask(__name__)

SERVER = "http://127.0.0.1:8000"
APIKEY = fetch_api_key.fetch_api()

@app.route('/api/v1/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    multipart_data = MultipartEncoder(fields={'file': (file.filename, file.stream, 'application/octet-stream')})
    headers = {'Content-Type': multipart_data.content_type, 'Authorization': APIKEY}
    response = requests.post(SERVER + '/api/v1/upload', data=multipart_data, headers=headers)

    print(response.text)
    return response.text, response.status_code

@app.route('/api/v1/scan/<hash>', methods=['GET'])
def scan_file(hash):
    post_dict = str(f'hash={hash}')
    headers = {'Authorization': APIKEY}
    response = requests.post(SERVER + '/api/v1/scan', data={'hash': hash}, headers=headers)
    
    return response.text, response.status_code

@app.route('/api/v1/download_pdf/<hash>', methods=['GET'])
def generate_pdf_report(hash):
    data = {'hash': hash}
    headers = {'Authorization': APIKEY}
    response = requests.post(SERVER + '/api/v1/download_pdf', data=data, headers=headers, stream=True)

    if response.status_code == 200:
        return response.content, 200
    else:
        return response.text, response.status_code

@app.route('/api/v1/report_json', methods=['POST'])
def generate_json_report():
    data = request.get_json()
    headers = {'Authorization': APIKEY}
    response = requests.post(SERVER + '/api/v1/report_json', json=data, headers=headers)

    return response.text, response.status_code

@app.route('/api/v1/delete_scan', methods=['POST'])
def delete_scan_result():
    data = request.get_json()
    headers = {'Authorization': APIKEY}
    response = requests.post(SERVER + '/api/v1/delete_scan', json=data, headers=headers)

    return response.text, response.status_code

if __name__ == '__main__':
    app.run(host='192.168.0.113', port=81, debug=True)
