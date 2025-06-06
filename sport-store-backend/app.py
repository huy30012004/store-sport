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
    # Gán id mới
    existing_ids = [p['id'] for p in data['products']]
    new_product['id'] = max(existing_ids, default=0) + 1

    # Bổ sung khởi tạo mảng reviews
    new_product['reviews'] = []

    # Những trường khác như image_url, categories, description,… giữ nguyên
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
@app.route('/api/products/<int:pid>/reviews', methods=['GET'])
def get_reviews(pid):
    """
    Trả về mảng các review (đánh giá) của sản phẩm có id = pid.
    Nếu chưa có key 'reviews', trả về mảng rỗng.
    """
    data = load_data()
    # Tìm sản phẩm
    prod = next((p for p in data['products'] if p['id'] == pid), None)
    if not prod:
        return jsonify({'error': 'Product not found.'}), 404

    reviews = prod.get('reviews', [])
    return jsonify({'reviews': reviews}), 200
@app.route('/api/orders/<int:oid>', methods=['GET'])
def get_order_by_id(oid):
    data = load_data()
    # Tìm đơn hàng có id == oid
    for o in data['orders']:
        if o.get('id') == oid:
            return jsonify(o)
    # Nếu không tìm thấy → trả về 404
    return jsonify({'error': 'Đơn hàng không tồn tại'}), 404

@app.route('/api/products/<int:pid>/reviews', methods=['POST'])
def post_review(pid):
    """
    Thêm review mới cho sản phẩm pid, chỉ cho phép nếu email user đã mua sản phẩm.
    Payload client gửi lên (JSON):
      {
        "email": "user@example.com",
        "rating": 4,                 ← bắt buộc, integer từ 1 đến 5
        "comment": "Bình luận ..."   ← có thể để chuỗi rỗng nếu chỉ chấm sao
      }
    """
    data = load_data()
    prod = next((p for p in data['products'] if p['id'] == pid), None)
    if not prod:
        return jsonify({'error': 'Product not found.'}), 404

    body = request.get_json()
    if not body:
        return jsonify({'error': 'Missing JSON payload.'}), 400

    # Lấy giá trị từ payload
    email = body.get('email', '').strip().lower()
    rating = body.get('rating')
    comment = body.get('comment', '').strip()

    # B1: Validate email và rating
    if not email:
        return jsonify({'error': 'Email is required.'}), 400
    if rating is None or not isinstance(rating, int) or rating < 1 or rating > 5:
        return jsonify({'error': 'Rating must be integer between 1 and 5.'}), 400

    # B2: Kiểm tra xem email từng mua sản phẩm pid chưa?
    orders = data.get('orders', [])
    has_purchased = False
    for order in orders:
        # So sánh lowercase để tránh case-sensitivity
        if order.get('customer', '').lower() == email:
            for item in order.get('items', []):
                if item.get('id') == pid:
                    has_purchased = True
                    break
        if has_purchased:
            break

    if not has_purchased:
        return jsonify({'error': 'Bạn chỉ có thể đánh giá sau khi đã mua sản phẩm này.'}), 403

    # B3: Nếu đã mua → tạo object review và append
    new_review = {
        'name': email,  # hoặc nếu bạn muốn hiển thị full tên, có thể sửa lại phần này
        'rating': rating,
        'comment': comment,
        'timestamp': datetime.utcnow().isoformat(timespec='seconds')
    }
    # Đảm bảo prod['reviews'] tồn tại
    if 'reviews' not in prod:
        prod['reviews'] = []
    prod['reviews'].append(new_review)

    # B4: Ghi lại data.json
    save_data(data)
    return jsonify({'message': 'Review added successfully.', 'review': new_review}), 201

if __name__ == '__main__':
    app.run(debug=True)
