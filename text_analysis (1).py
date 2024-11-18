# -*- coding: utf-8 -*-
"""text_analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SQn5FiU4E5oKUImO2JJDjoHrhUJ7MiK4
"""

import os
import pandas as pd
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
import re

# Ensure you have the stopwords dataset
nltk.download('stopwords')

# Load stopwords and master dictionary
stop_words = set(stopwords.words('english'))

# Load positive and negative words with a fallback encoding
def load_words(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            words = set(file.read().split())
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as file:
            words = set(file.read().split())
    return words

positive_words = load_words('/content/positive-words.txt')
negative_words = load_words('/content/negative-words.txt')

# Function to calculate variables
def analyze_text(text):
    # Cleaning and tokenizing
    words = re.findall(r'\w+', text.lower())
    clean_words = [word for word in words if word not in stop_words]

    # Sentiment analysis
    positive_score = sum(1 for word in clean_words if word in positive_words)
    negative_score = sum(1 for word in clean_words if word in negative_words)
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(clean_words) + 0.000001)

    # Readability
    sentences = nltk.sent_tokenize(text)
    avg_sentence_length = len(clean_words) / len(sentences)
    complex_words = [word for word in clean_words if len(nltk.word_tokenize(word)) > 2]
    percentage_complex_words = len(complex_words) / len(clean_words)
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

    # Other metrics
    avg_words_per_sentence = len(clean_words) / len(sentences)
    complex_word_count = len(complex_words)
    word_count = len(clean_words)
    syllable_per_word = sum([len(re.findall(r'[aeiouy]', word)) for word in clean_words]) / len(clean_words)
    personal_pronouns = len(re.findall(r'\b(I|we|my|ours|us)\b', text, re.I))
    avg_word_length = sum(len(word) for word in clean_words) / len(clean_words)

    return {
        'positive_score': positive_score,
        'negative_score': negative_score,
        'polarity_score': polarity_score,
        'subjectivity_score': subjectivity_score,
        'avg_sentence_length': avg_sentence_length,
        'percentage_complex_words': percentage_complex_words,
        'fog_index': fog_index,
        'avg_words_per_sentence': avg_words_per_sentence,
        'complex_word_count': complex_word_count,
        'word_count': word_count,
        'syllable_per_word': syllable_per_word,
        'personal_pronouns': personal_pronouns,
        'avg_word_length': avg_word_length
    }

# Analyze each extracted article
article_dir = 'articles'
output_data = []

# Check if the directory exists
if os.path.exists(article_dir):
    for filename in os.listdir(article_dir):
        url_id = filename.split('.')[0]
        with open(os.path.join(article_dir, filename), 'r', encoding='utf-8') as file:
            text = file.read()

        analysis = analyze_text(text)
        analysis['URL_ID'] = url_id
        output_data.append(analysis)
else:
    print(f"The directory '{article_dir}' does not exist. Please check the path and try again.")

# Create output dataframe if there is data
if output_data:
    output_df = pd.DataFrame(output_data)

    # Load input data for merging
    input_df = pd.read_excel('/mnt/data/Input.xlsx')
    final_df = pd.merge(input_df, output_df, on='URL_ID')

    # Save output to Excel
    final_df.to_excel('Output Data Structure.xlsx', index=False)
    print("Text analysis completed.")
else:
    print("No data to process.")

