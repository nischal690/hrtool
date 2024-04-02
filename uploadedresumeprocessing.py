from pypdf import PdfReader
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import spacy  # May need installation: pip install spacy 
from spacy.matcher import Matcher  

nltk.download('stopwords')


def process_uploaded_file(uploaded_file,jobdescription):
    
    
    reader = PdfReader(uploaded_file)
    resumeText = ""
    jobdescriptionText = jobdescription

    # Process all pages
    for page in reader.pages:
        text += page.extract_text()

    print("Extracted Text:\n", text)
    print("Job Description:\n", jobdescription)

    # Preprocessing steps:
    text = text.lower()  # Convert to lowercase
    jobdescriptionText = jobdescriptionText.lower()  # Convert to lowercase
    # Remove special characters, numbers, URLs, email addresses
    text = re.sub(r'[^a-z\s]', ' ', text) 
    jobdescriptionText = re.sub(r'[^a-z\s]', ' ', jobdescriptionText)
    text = re.sub(r'\d+', '', text)  
    jobdescriptionText = re.sub(r'\d+', '', jobdescriptionText)
    text = re.sub(r'http\S+', '', text, flags=re.MULTILINE) 
    jobdescriptionText = re.sub(r'http\S+', '', jobdescriptionText, flags=re.MULTILINE)
    text = re.sub(r'\S*@\S*\s?', '', text)
    jobdescriptionText = re.sub(r'\S*@\S*\s?', '', jobdescriptionText)

    # Tokenization
    tokens = nltk.word_tokenize(text)
    tokens2 = nltk.word_tokenize(jobdescriptionText)

    # Stop word removal
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    tokens2 = [word for word in tokens2 if word not in stop_words]

    # Stemming 
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]
    tokens2 = [stemmer.stem(word) for word in tokens2]

    # Final preprocessed text
    preprocessed_text = " ".join(tokens)
    preprocessed_text2 = " ".join(tokens2)

    # Output results
    print("Preprocessed Text:\n", preprocessed_text)
    print("Preprocessed Text:\n", preprocessed_text2)
