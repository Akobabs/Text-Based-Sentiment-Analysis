import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    # Check if text is a string and not empty
    if not isinstance(text, str) or text.strip() == "":
        return None  # Return None for empty or non-string values
    # Remove URLs, mentions, hashtags, special characters
    text = re.sub(r'http\S+|@\w+|#\w+|[^a-zA-Z\s]', '', text)
    # Lowercase
    text = text.lower()
    # Tokenize
    tokens = word_tokenize(text)
    # Remove stop words and lemmatize
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    # Return cleaned text or None if no tokens remain
    return ' '.join(tokens) if tokens else None

def preprocess_dataset(file_path, output_path, sample_size=10000):
    # Load dataset
    print(f"Loading dataset from {file_path}...")
    df = pd.read_csv(file_path, encoding='latin-1',
                     names=['sentiment', 'id', 'date', 'flag', 'user', 'text'])
    print(f"Initial dataset shape: {df.shape}")

    # Keep only sentiment and text
    df = df[['sentiment', 'text']]

    # Map sentiment: 0 (negative) -> 0, 4 (positive) -> 1
    df['sentiment'] = df['sentiment'].map({0: 0, 4: 1})

    # Remove rows with NaN in sentiment or text
    df = df.dropna()
    print(f"Shape after dropping NaN: {df.shape}")

    # Remove rows with empty strings in text
    df = df[df['text'].str.strip() != '']
    print(f"Shape after removing empty strings: {df.shape}")

    # Use a subset for faster testing
    df = df.sample(n=sample_size, random_state=42) if len(df) > sample_size else df
    print(f"Shape after sampling: {df.shape}")

    # Clean text
    df['cleaned_text'] = df['text'].apply(clean_text)

    # Remove rows where cleaned_text is None (empty after cleaning)
    df = df[df['cleaned_text'].notna()]
    print(f"Shape after removing empty cleaned text: {df.shape}")

    # Save cleaned dataset
    df.to_csv(output_path, index=False)
    print(f"Preprocessed dataset saved to {output_path}")
    print("Sentiment distribution:\n", df['sentiment'].value_counts())
if __name__ == "__main__":
    preprocess_dataset('data/sentiment140.csv', 'data/sentiment140_cleaned.csv')