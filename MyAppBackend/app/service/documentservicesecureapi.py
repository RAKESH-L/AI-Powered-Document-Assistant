from openai import AzureOpenAI
from app.service.database import create_database, create_connection_to_db, get_embedding, store_embedding, create_connection
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os
# from app.service.ragmodule import rag_answer

load_dotenv()

OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION") #For app user: you need to pass the version configured by the admin
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") #Eg: {BASE_URL}/api/azureai
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY") #For App User: use the app-registration key along with the app configuration unique key name eg. app123key-configName, For Api User: Substitute the key generated from Key Config Panel

client = AzureOpenAI()
    
def answer_question(document_text, question):
    
    document_text1 = document_text
    question1 = question
    prompt = f"Document: {document_text1}\n\nQuestion: {question1}\n\nAnswer:"

    res = client.chat.completions.create(
        model="gpt-4o",
        messages=[
                {"role":"system","content":"Respond in well-formatted HTML using bootstrap which will look very beautiful without docType tag, remove tripel quotes, html word at beginning and should fit in 3/4 of screen from left, only give answer what question is asked"},
                {"role":"user","content":prompt}],
        temperature= 0.7,
        max_tokens= 3828,
        top_p= 0.6,
        frequency_penalty= 0.7
    )
    response = res.choices[0].message.content
    embeddigs = embedding_storage(response, question)

    return res.choices[0].message.content

def embedding_storage(response, question):
    # Create the database and table if they do not exist
    create_database()
    question_response  = client.embeddings.create(
        model="text-embedding-ada-002", #Allowed values for ApiUser: text-embedding-ada-002
        input=question,
        encoding_format="float"
    )
    question_embedding = question_response.data[0].embedding
    print("question_embedding created")
    
    store_embedding(question, question_embedding)
    print("question_embedding stored")
    
    ans_response  = client.embeddings.create(
        model="text-embedding-ada-002", #Allowed values for ApiUser: text-embedding-ada-002
        input=response,
        encoding_format="float"
    )
    print("ans_embedding created")
    ans_embedding = ans_response.data[0].embedding

    # Step 2: Store document text embedding in the database
    store_embedding(response, ans_embedding)
    print("ans_embedding stored")

    # Step 5: Retrieve embeddings from the database
    retrieved_ans_embedding = get_embedding(response)
    retrieved_question_embedding = get_embedding(question)

    # Step 6: Compare embeddings
    assert ans_embedding == retrieved_ans_embedding, "Document embeddings do not match!"
    assert question_embedding == retrieved_question_embedding, "Question embeddings do not match!"

    print("Test Case #3: Embedding Creation and Storage - Passed")
    return None




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
    
    # embeddigs = embedding_storage(document_text, question)
    
    return answer



# document_text = [
#     "The quick brown fox jumps over the lazy dog.",
#     "A fast brown fox leaps over a sleepy dog.",
#     "The quick brown fox is known for jumping over lazy dogs."
# ]
# question = "What does the fox do?"

# # Store document embeddings in the database
# for text in document_text:
#     doc_response  = client.embeddings.create(
#         model="text-embedding-ada-002", #Allowed values for ApiUser: text-embedding-ada-002
#         input=text,
#         encoding_format="float"
#     )
#     print("ans_embedding created")
#     doc_embedding = doc_response.data[0].embedding
#     store_embedding(text, doc_embedding)

# # Generate answer using RAG technique
# answer = rag_answer(question)
# print(f"Question: {question}")
# print(f"Answer: {answer}")

# # Validate the answer
# assert "jumps over the lazy dog" in answer or "leaps over a sleepy dog" in answer, "RAG technique did not generate the expected answer!"

# print("Test Case #4: RAG Technique Functionality - Passed")