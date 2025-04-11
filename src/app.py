import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
from src.preprocessing import clean_text

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load model and vectorizer
with open('models/svm_model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('models/tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    # Clean text
    cleaned_text = clean_text(text)
    # Transform text to TF-IDF
    X = vectorizer.transform([cleaned_text]).toarray()
    # Predict
    prediction = model.predict(X)[0]
    sentiment = 'positive' if prediction == 1 else 'negative'
    return jsonify({
        'text': text,
        'sentiment': sentiment
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
