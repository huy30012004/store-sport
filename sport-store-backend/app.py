from flask import Flask, request, jsonify
from flask_cors import CORS
import json, os
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATA_FILE = 'data.json'

def load_data():
    full_path = os.path.abspath(DATA_FILE)
    print(f"📂 Flask đang sử dụng file data.json tại: {full_path}")
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({'products': [], 'orders': []}, f)
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/api/products', methods=['GET'])
def get_products():
    data = load_data()
    category = request.args.get('category')
    keyword = request.args.get('search')  # đọc param 'search'
    products = data['products']

    if category:
        products = [p for p in products if category in p.get('categories', [])]

    if keyword:
        key = keyword.lower()
        products = [p for p in products if key in p.get('name', '').lower()]

    return jsonify(products)


@app.route('/api/products', methods=['POST'])
def add_product():
    data = load_data()
    new_product = request.get_json()
    new_product['image_url'] = new_product.get('image_url', '')
    new_product['categories'] = new_product.get('categories', [])
    existing_ids = [p['id'] for p in data['products']]
    new_product['id'] = max(existing_ids, default=0) + 1
    data['products'].append(new_product)
    save_data(data)
    return jsonify({'message': 'Added'}), 201

@app.route('/api/products/<int:pid>', methods=['PUT'])
def update_product(pid):
    data = load_data()
    update = request.get_json()
    for p in data['products']:
        if p['id'] == pid:
            if 'image_url' in update:
                p['image_url'] = update['image_url']
            p['categories'] = update.get('categories', [])
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

@app.route('/api/products/<int:pid>', methods=['GET'])
def get_product(pid):
    data = load_data()
    for p in data['products']:
        if p['id'] == pid:
            return jsonify(p)
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/orders', methods=['GET'])
def get_orders():
    data = load_data()
    return jsonify(data['orders'])

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = load_data()
    new_order = request.get_json()

    # Gán ID và created_at (nếu chưa có)
    new_order['id'] = len(data['orders']) + 1
    new_order['created_at'] = new_order.get('created_at', datetime.now().isoformat())

    # Nếu payload không có phí ship riêng, có thể gán mặc định
    if 'shippingFee' not in new_order:
        new_order['shippingFee'] = 30000

    data['orders'].append(new_order)
    save_data(data)
    return jsonify({'message': 'Đơn hàng đã được lưu'}), 200
if __name__ == '__main__':
    app.run(debug=True)
