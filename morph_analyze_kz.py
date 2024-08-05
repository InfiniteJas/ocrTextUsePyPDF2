import json
from pymystem3 import Mystem
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import sys
import io
import re

# Set console output encoding to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Script execution started")

# Loading stop words and initializing lemmatizer
print("Loading stop words and initializing lemmatizer...")
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
stop_words = set(stopwords.words('kazakh'))
mystem = Mystem()

def clean_and_fix_text(text):
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Add space after punctuation if missing
    text = re.sub(r'([.,!?:;])(\S)', r'\1 \2', text)
    
    # Fix spaces before punctuation
    text = re.sub(r'\s([.,!?:;])', r'\1', text)
    
    # Separate words that are incorrectly joined
    text = re.sub(r'([а-яА-Я])([A-Za-z])', r'\1 \2', text)
    text = re.sub(r'([A-Za-z])([а-яА-Я])', r'\1 \2', text)
    
    # Fix dash issues
    text = re.sub(r'(?<=[а-яА-Я])-(?=[а-яА-Я])', ' - ', text)
    
    # Capitalize first letter of sentences
    text = '. '.join(s.capitalize() for s in text.split('. '))
    
    return text.strip()

def lemmatize_and_remove_stopwords(text):
    words = word_tokenize(text.lower())
    lemmas = mystem.lemmatize(' '.join(words))
    processed_words = [word for word in lemmas if word.strip() and word not in stop_words and word.isalnum()]
    return ' '.join(processed_words)

# Loading data from JSON file
print("Loading data from JSON file...")
try:
    with open('processed_documents.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    print(f"Loaded {len(data)} documents")
except FileNotFoundError:
    print("Error: File 'processed_documents.json' not found")
    sys.exit(1)
except json.JSONDecodeError:
    print("Error: Problem with JSON decoding")
    sys.exit(1)

# Processing each document
print("Starting document processing...")
for i, doc in enumerate(data, 1):
    # Clean and fix the text
    cleaned_text = clean_and_fix_text(doc['content'])
    doc['cleaned_content'] = cleaned_text
    
    # Lemmatize and remove stop words
    doc['processed_content'] = lemmatize_and_remove_stopwords(cleaned_text)
    
    if i % 10 == 0:  # Print message every 10 documents
        print(f"Processed {i} documents")

# Saving processed data to a new JSON file
print("Saving processed data...")
try:
    with open('processed_documents_cleaned_and_lemmatized.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    print("Processing completed. Results saved in 'processed_documents_cleaned_and_lemmatized2.json'")
except IOError:
    print("Error while saving results")
    sys.exit(1)

print("Script execution completed")
