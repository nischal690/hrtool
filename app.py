import os
from flask import Flask, jsonify, render_template, request
import logging
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
import json
import firebase_admin
from firebase_admin import credentials
import subprocess


cred = credentials.Certificate(r"C:\Users\Administrator\hrtool\hrtooljd-firebase-adminsdk-mbimv-45e1cfca77.json")
firebase_admin.initialize_app(cred)
from firebase_admin import firestore

db = firestore.client()
document = ""




app = Flask(__name__)
conversation_memory = ConversationBufferMemory()

template = """As an expert AI-based recruiter, your task is to develop a detailed scoring system for resume evaluation centered around key competencies listed in the job description. The scoring system should be point-based and total a maximum of 1000 points. Begin by asking the user for the job description and seek clarification on required skills and their respective priority levels according to the role. 

This includes investigating if certain conditions carry more weight, such as having no gap years in education. For example, if the job description lists six skills but the user prioritizes two, these two skills should carry more points, while the remaining skills accrue lesser points. Continue this interaction with the user until they confirm that all necessary requirements are integrated into the scoring system. 

Remember, your focus as a recruiter is strictly on developing this scoring plan; disregard any information irrelevant to this scope. 

Example Prompt:
"Could you provide the job description and identify which skills are of the highest priority? Additionally, are there any specific conditions, like no gap years in education or significant industry experience, that should hold more weight in our evaluation process?
Relevant Information(have a conversation with user to create a robout plan ):

{history}

Conversation:
Human: {input}
AI:
"""

custom_llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key="AIzaSyDIJnTZe1rj_l9PLQtnSpl8L6U_vLBIbK0")

PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
# ... other imports
chathistory = []  # Initialize chat history as a list
  # Initialize chat history 


conversation = ConversationChain(
    llm=custom_llm, verbose=True, memory=conversation_memory,
)


@app.route("/")
def home():
    print("Homepage requested") 
    global conversation_memory  # Access the global memory object
    conversation_memory.clear()  # Reset the memory
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    print(f"Received chat data: {data}") 
    user_message = data.get("message")
    


    response = conversation.run(PROMPT.format(history=conversation.memory.buffer, input=user_message))

    print(f"Sending API response back to client: {response}")

    new_interaction = {
        "human": user_message,
        "ai": response 
    }
    chathistory.append(new_interaction)
    
    
    return jsonify({"data": response})



def confirm_evaluation(chathistory):
    print("Starting evaluation with chat history:")
    print(chathistory[:500])  # Print the first 500 characters of the chat history for a quick overview

    prompt_template = PromptTemplate.from_template("""As an expert in data extraction and knowledge manipulation, you are tasked with analyzing a provided chat history ({chathistory}). Your goal is to identify a job description within this chat history and refine or reshape it based on any modifications mentioned in the conversation. If there are no modifications outlined, you should maintain the original description, ensuring it is as comprehensive and detailed as possible.

Additionally, you are to extract the scoring method used, as mentioned in the chat history. This information, along with the detailed job description, should be structured and presented in JSON format.

Instructions:

Review the chat history to pinpoint the job description and its components.
Adjust the job description based on any modifications mentioned in the chat or retain the existing description, ensuring it is detailed and comprehensive.
Determine the scoring method outlined in the chat.
Compile the refined job description and scoring method into JSON format, ensuring the total points allocated across different criteria sum up to 1000.
Remember, your expertise is crucial in accurately interpreting the details and subtleties from the chat history.

Note: You are allowed to improvise both the scoring method and the job description. However, ensure that the total points allocated across all assessed skills or criteria equal 1000."""
)

    response_schemas = [
        ResponseSchema(name="job_description", description="extracted job description"),
        ResponseSchema(
            name="scoring_method",
            description="extracted scoring method (valid JSON)",
           
        ),
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    prompt = prompt_template.format(chathistory=chathistory,)
    
    # Print the formatted prompt to see what is being sent to the LLM
    print("Formatted prompt for LLM:")
    print(prompt[:500])  # Print the first 500 characters of the prompt for a quick overview

    custom_llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key="AIzaSyDIJnTZe1rj_l9PLQtnSpl8L6U_vLBIbK0")
    llm = LLMChain(llm=custom_llm, prompt=prompt_template, output_parser=output_parser, verbose=False)
    
    try:
        llm_output = llm.run(prompt_template.format(chathistory=chathistory))
        print("LLM Output received successfully.")
    except Exception as e:
        print("Error running LLM:", e)
        return  # Early exit if LLM execution fails

    # Attempt to print the structured output from the LLM
    try:
        print("Structured LLM Output:", llm_output)
        job_description = llm_output['job_description']
        scoring_method = llm_output['scoring_method']
    except KeyError as e:
        print("Error parsing LLM output:", e)
        return  # Early exit if parsing fails

    # Assuming successful parsing of LLM output
    data = {
        'job_description': job_description,
        'scoring_method': scoring_method,
    }

    # Print the data to be stored for a final check
    

    # Your database storage operation here
    # Example:
    doc_ref = db.collection('jobDescriptions').document()

    doc_ref.set(data)
    doc_id = doc_ref.id

    print("Data storage operation completed.")
    fetch_scoring_method(doc_id)
    fetch_job_description(doc_id)
   

    
@app.route("/confirm", methods=["POST"])
def confirm():
    # Assuming confirm_evaluation updates or processes the chat history in some way
    confirm_evaluation(chathistory)
    
    
    # Fetching the scoring method as a JSON object
    print( "test" + document)
    
    # Embedding the scoring_method_json directly into the response JSON
    response_data = {
        "message": "Confirmation processed",
        "scoringMethod": document  # This assumes fetch_scoring_method returns a JSON-serializable object
    }
    
    
    # Returning the combined JSON
    return jsonify(response_data), 200
@app.route('/confirm-screen')
def confirm_screen():
    return render_template('confirm-screen.html')
def fetch_scoring_method(doc_id):

    global document

    
    # Fetch the document by ID
    doc_ref = db.collection('jobDescriptions').document(doc_id)

    doc = doc_ref.get()
    
    if doc.exists:
        # Extract the 'scoring_method' field from the document
        
        scoring_method = doc.to_dict().get('scoring_method', 'No scoring method found')
        print(f"Scoring Method: {scoring_method}")
        document = str(scoring_method)

          
        return scoring_method
    else:
        print("Document does not exist.")
        return None
    
    
from scrap import perform_scraping_task  

@app.route('/trigger-scrap', methods=['POST'])
def trigger_scrap():
    result = perform_scraping_task()

    if 'error' in result:
        app.logger.error("Scraping error: {}".format(result['error']))
        return jsonify({"message": "Scraping failed", "error": result['error']}), 500

    # Process the successful scraped data in 'result'
    app.logger.info("Scraping successful")
    return jsonify({"message": "Scraping completed", "data": result}), 200 

def fetch_job_description(doc_id):
    print("Fetching job description...")
    # Assuming db is a predefined database client instance
    doc_ref = db.collection('jobDescriptions').document(doc_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        print("Document does not exist.")
        return None
    
    job_description = doc.to_dict().get('job_description', 'No job description found')
    print(f"Job Descriptiontest: {job_description}")
    
    # Define the prompt template
    

if __name__ == "__main__":
    app.run(debug=True)
