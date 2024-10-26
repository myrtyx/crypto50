# app.py

from flask import Flask, jsonify
from fdv_table import generate_data

app = Flask(__name__)

@app.route('/api/data')
def get_data():
    data = generate_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
