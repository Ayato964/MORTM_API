from flask import Flask, jsonify
import music21
import AGSM

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def home():
    return jsonify({'message': 'Hello from Flask on Vercel!'})

if __name__ == '__main__':
    app.run()
