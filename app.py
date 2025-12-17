from flask import Flask, request, jsonify, render_template
import sqlite3
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

import cv2
import os
from twilio.rest import Client

# Initialize Flask app
app = Flask(__name__)

# Path for uploaded images
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# --- Twilio setup ---
# ✅ Twilio SMS configuration (replace with your credentials)
TWILIO_SID = "AC73a9377014a958b5a7f22def668ec0db"
TWILIO_AUTH_TOKEN = "8e51b06963599e3c360e597e77d7b265"
TWILIO_PHONE_NUMBER = "+17623831363"  # e.g. "+12015551234"

# ------------------ Database Connection ------------------
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# ------------------ Routes ------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part in request'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No file selected'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # --- OCR Extraction ---
    try:
        img = cv2.imread(filepath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        text = pytesseract.image_to_string(gray)
        detected_plate = ''.join(e for e in text if e.isalnum()).upper()

        print(f"🕵️ Detected plate text: {detected_plate}")

        if not detected_plate:
            return jsonify({'status': 'error', 'message': 'Could not detect number plate text'}), 400

        # --- Database Lookup with Fuzzy Matching ---
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT owner_name, phone_number, number_plate FROM vehicles")
        rows = cursor.fetchall()
        conn.close()

        vehicle = None
        for row in rows:
            db_plate = row["number_plate"].replace(" ", "").strip().upper()
            if db_plate in detected_plate or detected_plate in db_plate:
                vehicle = row
                break

        if not vehicle:
            return jsonify({'status': 'error', 'message': f'Plate {detected_plate} not found in database'}), 404

        owner_name = vehicle['owner_name']
        phone_number = vehicle['phone_number']
        actual_plate = vehicle['number_plate']

        # --- Send SMS via Twilio ---
        try:
            client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
            message_body = f"Dear {owner_name}, your car ({actual_plate}) is parked improperly. Please move it."
            message = client.messages.create(
                body=message_body,
                from_=TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            print(f"✅ SMS sent successfully to {phone_number}")
        except Exception as e:
            print(f"⚠️ SMS sending failed: {e}")
            return jsonify({'status': 'error', 'message': f'SMS sending failed: {e}'}), 500

        return jsonify({
            'status': 'success',
            'message': f'Message sent to the owner',
            'plate_detected': detected_plate
        })

    except Exception as e:
        print(f"❌ Error processing image: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)



