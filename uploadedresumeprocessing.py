from ctypes import Union
import json
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from pypdf import PdfReader
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import spacy  # May need installation: pip install spacy 
from spacy.matcher import Matcher 
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from langchain.chains import LLMChain
from langchain.prompts.prompt import PromptTemplate
import google.generativeai as genai





nltk.download('stopwords')


def process_uploaded_file(uploaded_file, job_description) :
    # Read PDF content
    try:
        reader = PdfReader(uploaded_file)
        text = ''.join([page.extract_text() or "" for page in reader.pages])
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return

    # Convert job_description to string if it is a dictionary
    if type(job_description) == dict:
        # Convert the entire dictionary to a string
        job_description_text = json.dumps(job_description)
    elif type(job_description) == str:
        job_description_text = job_description
    else:
        print("Invalid job description format.")
        return

    # Preprocess both the resume and job description texts
    preprocessed_resume = preprocess_text(text)
    preprocessed_job_description = preprocess_text(job_description_text)

    # Output results
    print("Preprocessed Resume Text:\n", preprocessed_resume)
    print("Preprocessed Job Description Text:\n", preprocessed_job_description)
    score = calculate_resume_score(preprocessed_resume, preprocessed_job_description)   
    print("Resume Score:", score)
    return score

def preprocess_text(text: str) -> str:
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^a-z\s]', ' ', text)  # Remove special characters, numbers
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = re.sub(r'http\S+', '', text, flags=re.MULTILINE)  # Remove URLs
    text = re.sub(r'\S*@\S*\s?', '', text)  # Remove email addresses

    # Tokenization
    tokens = nltk.word_tokenize(text)

    # Stop word removal
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    # Stemming
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(word) for word in tokens]

    return " ".join(stemmed_tokens)

def calculate_resume_score(resume_text, job_description):
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    percentage_score = score * 100
    return percentage_score 

def calculate_resume_score_using_LLM(resume_text, job_description, scoring_method):

    
    try:
        reader = PdfReader(resume_text)
        text = ''.join([page.extract_text() or "" for page in reader.pages])
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return

    # Convert job_description to string if it is a dictionary
    if type(job_description) == dict:
        # Convert the entire dictionary to a string
        job_description_text = json.dumps(job_description)
    elif type(job_description) == str:
        job_description_text = job_description
    else:
        print("Invalid job description format." + str(type(job_description)))
        return
    
    if type(scoring_method) == dict:
        # Convert the entire dictionary to a string
        scoring_method_text = json.dumps(scoring_method)
    elif type(scoring_method) == str:
        scoring_method_text = scoring_method
    else:
        print("Invalid scoring method format." + str(type(scoring_method)))
        return
    
    print("job_description: ", job_description_text)
    print("resume_text: ", text)
    print("scoring_method: ", scoring_method_text)
    
    
    prompt_template = f"""
    As an expert AI recruiter, your task is to evaluate a given resume based on a provided job description and scoring method. 

### Instructions:
- You will receive a detailed job description outlining the required skills and qualifications for the position.
- A specific scoring method will be provided, defining how each aspect of the resume should be evaluated.
- Your goal is to carefully analyze the resume, align it with the job description, and assess it according to the scoring criteria.
- Provide the final score in the format of "score x out of total y," along with the calculated match percentage based on the score.

Ensure that your evaluation reflects a comprehensive understanding of the job requirements and effectively measures the candidate's suitability for the role. 

Remember to consider both the content of the resume and how well it aligns with the expectations outlined in the job description. Your analysis will determine the match percentage, indicating the degree to which the candidate's profile meets the specific criteria set for the position. 

job_description: {job_description_text}  
resume_text: {text}  
scoring_method: {scoring_method_text}    


Deliver a thorough and insightful evaluation that highlights the candidate's strengths and areas for improvement, ultimately guiding the hiring decision with precision and accuracy.

your response should be in the format: "score x out of total y, match percentage"
    """

    print("Prompt Template:\n", prompt_template)
    genai.configure(api_key="AIzaSyDIJnTZe1rj_l9PLQtnSpl8L6U_vLBIbK0")
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt_template)

    return response.text  

