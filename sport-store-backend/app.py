
from flask import Flask, request, jsonify
from flask_cors import CORS
import json, os

app = Flask(__name__)
CORS(app)

DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({'products': [], 'orders': []}, f)
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/api/products', methods=['GET'])
def get_products():
    data = load_data()
    return jsonify(data['products'])

@app.route('/api/products', methods=['POST'])
def add_product():
    data = load_data()
    new_product = request.get_json()
    new_product['id'] = len(data['products']) + 1
    data['products'].append(new_product)
    save_data(data)
    return jsonify({'message': 'Added'}), 201

@app.route('/api/products/<int:pid>', methods=['PUT'])
def update_product(pid):
    data = load_data()
    for p in data['products']:
        if p['id'] == pid:
            update = request.get_json()
            p.update(update)
            save_data(data)
            return jsonify({'message': 'Updated'})
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/products/<int:pid>', methods=['DELETE'])
def delete_product(pid):
    data = load_data()
    data['products'] = [p for p in data['products'] if p['id'] != pid]
    save_data(data)
    return jsonify({'message': 'Deleted'})

@app.route('/api/orders', methods=['GET'])
def get_orders():
    data = load_data()
    return jsonify(data['orders'])

if __name__ == '__main__':
    app.run(debug=True)
