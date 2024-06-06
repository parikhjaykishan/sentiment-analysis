import React from 'react';
import SentimentForm from './components/SentimentForm';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Sentiment Analysis</h1>
      </header>
      <main>
        <SentimentForm />
      </main>
    </div>
  );
}

export default App;
