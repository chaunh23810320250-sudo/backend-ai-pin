from flask import Flask, request, jsonify
from flask_cors import CORS  # Thêm thư viện cấp phép
import joblib
import pandas as pd

app = Flask(__name__)

# Cấu hình CORS cực mạnh: Cho phép mọi domain (*) gọi vào API này
CORS(app, resources={r"/*": {"origins": "*"}})

# Tải "bộ não" AI
model = joblib.load('battery_ai_model.pkl')

@app.route('/')
def home():
    return "Máy chủ AI Dự đoán SOH Pin đang hoạt động bình thường!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        input_df = pd.DataFrame({
            'cycle': [float(data['cycle'])],
            'ambient_temperature': [float(data['temp'])],
            'temp_gradient': [float(data['gradient'])]
        })
        
        soh = model.predict(input_df)[0]
        status = "AN TOÀN" if soh >= 80 else "CẢNH BÁO" if soh >= 70 else "NGUY HIỂM"
        
        return jsonify({
            'success': True,
            'soh_value': round(soh, 2),
            'status': status
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Xóa đoạn app.run() ở cuối đi, vì lên mạng chúng ta dùng Gunicorn để chạy
