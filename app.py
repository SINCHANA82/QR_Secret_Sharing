from flask import Flask, request, render_template, jsonify
import os
import qrcode
import cv2

app = Flask(__name__)

QR_FOLDER = 'static/qr_codes'
os.makedirs(QR_FOLDER, exist_ok=True)

# --- From generate_qr.py ---
def split_secret(secret, num_shares):
    share_length = len(secret) // num_shares
    remainder = len(secret) % num_shares
    shares = []
    start = 0
    for i in range(num_shares):
        length = share_length + (1 if i < remainder else 0)
        shares.append(secret[start: start + length])
        start += length
    return shares

def generate_qr_codes(shares):
    filenames = []
    for i, share in enumerate(shares):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(share)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        filename = os.path.join(QR_FOLDER, f"share_{i+1}.png")
        img.save(filename)
        filenames.append(f"/{filename}")
    return filenames

# --- From decode_qr.py ---
def decode_qr_code(image_path):
    img = cv2.imread(image_path)
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img)
    return data if data else None

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    secret = data.get('secret')
    num_shares = int(data.get('num_shares', 1))

    shares = split_secret(secret, num_shares)
    image_urls = generate_qr_codes(shares)

    return jsonify({"images": image_urls})

@app.route('/reconstruct', methods=['POST'])
def reconstruct():
    files = request.files.getlist('files')
    shares = []

    for f in files:
        path = os.path.join(QR_FOLDER, f.filename)
        f.save(path)
        decoded = decode_qr_code(path)
        if decoded:
            shares.append(decoded)

    secret = "".join(shares) if shares else "Failed to decode QR codes."
    return jsonify({"secret": secret})

if __name__ == '__main__':
    app.run(debug=True)
