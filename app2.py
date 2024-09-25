import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline

# Load the CSV data
@st.cache_data
def load_data():
    data = pd.read_csv('train.csv')  # Update with the correct path to your CSV file
    return data

# Function to generate a response based on context using the Hugging Face pipeline
def generate_response(context, user_input):
    qa_pipeline = pipeline("question-answering", model="facebook/rag-token-nq")  # You can change the model if needed
    result = qa_pipeline(question=user_input, context=context)
    return result['answer']

# Function to find the best context based on user input using TF-IDF and cosine similarity
def find_best_context_and_response(data, user_input):
    tfidf_vectorizer = TfidfVectorizer()
    
    # Fit the TF-IDF model on the context data
    tfidf_matrix = tfidf_vectorizer.fit_transform(data['Context'].tolist())
    
    # Transform the user input to the same TF-IDF space
    user_input_vector = tfidf_vectorizer.transform([user_input])
    
    # Compute cosine similarity between user input and context
    cosine_similarities = cosine_similarity(user_input_vector, tfidf_matrix).flatten()
    
    # Find the index of the highest similarity score
    best_index = cosine_similarities.argmax()
    best_context = data['Context'][best_index]
    best_response = data['Response'][best_index]  # Get the corresponding response
    best_similarity = cosine_similarities[best_index]  # Store the best similarity score
    
    return best_context, best_response, best_similarity

def app():
    data = load_data()

    # Streamlit app layout
    st.title("Chatbot with RAG for Mental health")
    st.write("Ask me anything! I will respond based on the provided context.")

    # User input
    user_input = st.text_input("Your question:")

    if user_input:
        # Find the best context and corresponding response based on the user input
        best_context, best_response, similarity_score = find_best_context_and_response(data, user_input)

        # Display the context and response only if the similarity score is greater than 0.5
        if similarity_score > 0.5:  # Check if the similarity score exceeds the threshold
            st.write(f"**Best Context:** {best_context}")
            st.write(f"**Response:** {best_response}")
        else:
            st.write("No relevant context found. Please try asking something else.")

