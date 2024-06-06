from flask import Flask, request, jsonify
import nltk
from nltk.corpus import movie_reviews
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy as nltk_accuracy
import random
from flask_cors import CORS

# Download NLTK data
nltk.download('movie_reviews')
nltk.download('punkt')
nltk.download('stopwords')

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load and preprocess data
def extract_features(words):
    return dict([(word, True) for word in words])

# Load movie reviews from NLTK corpus
fileids_pos = movie_reviews.fileids('pos')
fileids_neg = movie_reviews.fileids('neg')

features_pos = [(extract_features(movie_reviews.words(fileids=[f])), 'Positive') for f in fileids_pos]
features_neg = [(extract_features(movie_reviews.words(fileids=[f])), 'Negative') for f in fileids_neg]

# Split the data into training and testing datasets
threshold = 0.8
num_pos = int(threshold * len(features_pos))
num_neg = int(threshold * len(features_neg))

features_train = features_pos[:num_pos] + features_neg[:num_neg]
features_test = features_pos[num_pos:] + features_neg[num_neg:]

# Train a Naive Bayes classifier
classifier = NaiveBayesClassifier.train(features_train)

# Function to predict sentiment of a sentence
def predict_sentiment(text):
    words = nltk.word_tokenize(text)
    features = extract_features(words)
    return classifier.classify(features)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data or 'reviews' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    reviews = data['reviews']
    results = [{"review": review, "sentiment": predict_sentiment(review)} for review in reviews]
    
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True)
