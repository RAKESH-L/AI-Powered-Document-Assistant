from aifc import Error
import openai
from app.service.database import create_database, create_connection_to_db, get_embedding, store_embedding, create_connection
import numpy as np
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION") #For app user: you need to pass the version configured by the admin
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") #Eg: {BASE_URL}/api/azureai
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY") #For App User: use the app-registration key along with the app configuration unique key name eg. app123key-configName, For Api User: Substitute the key generated from Key Config Panel

client = AzureOpenAI()

def cosine_similarity(vec1, vec2):
    """Calculate the cosine similarity between two vectors."""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def retrieve_relevant_documents(question_embedding, top_k=5):
    """Retrieve the most relevant documents based on cosine similarity."""
    connection = create_connection_to_db()
    if connection is None:
        return []
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT text, embedding FROM embeddings")
        all_embeddings = cursor.fetchall()
        cursor.fetchall()  # Clear the result set
        
        # Calculate similarities
        similarities = []
        for text, embedding_str in all_embeddings:
            embedding = list(map(float, embedding_str.split(',')))
            similarity = cosine_similarity(question_embedding, embedding)
            similarities.append((text, similarity))
        
        # Sort by similarity and return top_k documents
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_documents = [text for text, _ in similarities[:top_k]]
        return top_documents
    except Error as e:
        print(f"Error while retrieving documents: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def generate_answer(question, top_documents):
    """Generate an answer using the retrieved documents."""
    context = " ".join(top_documents)
    prompt=f"Context: {context}\nQuestion: {question}\nAnswer:"
    res = client.chat.completions.create(
        model="gpt-4o",
        messages=[
                # {"role":"system","content":"Respond in well-formatted HTML using bootstrap which will look very beautiful without docType tag, remove tripel quotes, html word at beginning and should fit in 3/4 of screen from left, only give answer what question is asked"},
                {"role":"user","content":prompt}],
        temperature= 0.7,
        max_tokens= 3828,
        top_p= 0.6,
        frequency_penalty= 0.7
    )

    return res.choices[0].message.content

def rag_answer(question):
    """Main function to generate an answer using the RAG technique."""
    # Step 1: Create embedding for the question
    question_response  = client.embeddings.create(
        model="text-embedding-ada-002", #Allowed values for ApiUser: text-embedding-ada-002
        input=question,
        encoding_format="float"
    )
    print("ans_embedding created")
    question_embedding = question_response.data[0].embedding
    
    # Step 2: Retrieve relevant documents
    top_documents = retrieve_relevant_documents(question_embedding)
    
    # Step 3: Generate answer based on retrieved documents
    answer = generate_answer(question, top_documents)
    return answer
