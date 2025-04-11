import React, { useState } from 'react';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);
    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });
      const data = await response.json();
      if (response.ok) {
        setResult(data);
      } else {
        setError(data.error || 'Something went wrong');
      }
    } catch (err) {
      setError('Failed to connect to the server');
    }
  };

  return (
    <div className="App">
      <h1>Sentiment Analysis</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter text to analyze"
          rows="5"
          cols="50"
        />
        <br />
        <button type="submit">Analyze</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {result && (
        <div>
          <h3>Result:</h3>
          <p>Text: {result.text}</p>
          <p>Sentiment: {result.sentiment}</p>
        </div>
      )}
    </div>
  );
}

export default App;