import os
# import openai
from openai import AzureOpenAI
from PyPDF2 import PdfReader
from dotenv import load_dotenv

load_dotenv()


OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION") #For app user: you need to pass the version configured by the admin
# print(OPENAI_API_VERSION)
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") #Eg: {BASE_URL}/api/azureai
# print(AZURE_OPENAI_ENDPOINT)
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY") #For App User: use the app-registration key along with the app configuration unique key name eg. app123key-configName, For Api User: Substitute the key generated from Key Config Panel
# print(AZURE_OPENAI_API_KEY)

client = AzureOpenAI()

# Set up Azure OpenAI API Key and Endpoint
# openai.api_key = "19ffba4957a4be25"
# openai.api_base = "https://hexavarsity-secureapi-azurewebsites.net/api/azureai"
# openai.api_type = "azure"
# openai.api_version = "2024-02-01" 

DEFAULT_UPLOAD_PATH = r"C:\Users\2000080631\workspace\DocumentExtractor\MyApp\drive"

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"The specified PDF file does not exist: {pdf_path}")

    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    return text

def generate_embeddings(text):
    """
    Generate embeddings for the given text using Azure OpenAI.
    """
    # response = openai.Embedding.create(
    #     input=text,
    #     engine="text-embedding-ada-002"  # Specify the embedding model
    # )
    # embeddings = response['data'][0]['embedding']
    
    response = client.embeddings.create(
    model="text-embedding-ada-002", #Allowed values for ApiUser: text-embedding-ada-002
    input=text,
    encoding_format="float"
    )
    embeddings = response['data'][0]['embedding']
    return embeddings

def answer_question(document_text, question):
    """
    Generate an answer to a question based on the document text using GPT-4.
    """
    prompt = f"Document: {document_text}\n\nQuestion: {question}\n\nAnswer:"
    # response = openai.ChatCompletion.create(
    #     deployment_id="gpt-4",
    #     messages=[
    #         {"role": "user", "content": prompt}
    #     ]
    # )
    
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role":"system","content":"you are a AI assistent to give answer based on the document provided"},
        {"role":"user","content":prompt}],
    temperature= 0.7,
    max_tokens= 3828,
    top_p= 0.6,
    frequency_penalty= 0.7
)
    print("response: ",response)
    return response.choices[0].message.content

def process_file_and_answer_question(file, question):
    """
    Process the uploaded file and generate an answer to the question.
    """
    # Save the uploaded file to the default path
    file_path = os.path.join(DEFAULT_UPLOAD_PATH, file.filename)
    file.save(file_path)

    # Extract text from the saved PDF
    document_text = extract_text_from_pdf(file_path)
    
    # Generate an answer to the question
    answer = answer_question(document_text, question)
    
    return answer
