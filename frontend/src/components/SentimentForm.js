import React, { useState } from 'react';
import axios from 'axios';

function SentimentForm() {
  const [reviews, setReviews] = useState("");
  const [results, setResults] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/predict', { reviews: reviews.split('\n') });
      setResults(response.data);
    } catch (error) {
      console.error("There was an error making the request:", error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <textarea
          value={reviews}
          onChange={(e) => setReviews(e.target.value)}
          placeholder="Enter reviews, one per line"
          rows="10"
          cols="50"
        />
        <br />
        <button type="submit">Analyze Sentiment</button>
      </form>
      <div>
        {results.map((result, index) => (
          <div key={index}>
            <p>Review: {result.review}</p>
            <p>Sentiment: {result.sentiment}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SentimentForm;
