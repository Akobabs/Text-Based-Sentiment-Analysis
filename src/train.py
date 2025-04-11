import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import pickle

def train_model(input_path):
    # Load cleaned dataset
    df = pd.read_csv(input_path)
    # Extract TF-IDF features
    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(df['cleaned_text']).toarray()
    y = df['sentiment'].values
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Train SVM
    model = SVC(kernel='linear')
    model.fit(X_train, y_train)
    # Evaluate
    y_pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"F1-Score: {f1_score(y_test, y_pred):.4f}")
    # Save model and vectorizer
    with open('models/svm_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('models/tfidf_vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    print("Model and vectorizer saved.")

if __name__ == "__main__":
    train_model('data/sentiment140_cleaned.csv')