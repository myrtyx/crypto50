from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/api/data')
def get_data():
    try:
        with open('current_data.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({'error': 'Данные недоступны'}), 503
    except json.JSONDecodeError:
        return jsonify({'error': 'Данные повреждены'}), 500

if __name__ == '__main__':
    app.run(debug=True)
