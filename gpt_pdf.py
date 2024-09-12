import streamlit as st
import pdfplumber
import openai

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def create_prompt(text, query):
    return f"Based on the following text: \"{text}\", {query}"

def get_gpt35_response(prompt, api_key):
    openai.api_key = api_key
    try:
        response = openai.chat.Completion.create(
            model="gpt-3.5-turbo",  # Use GPT-3.5-turbo
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}],
            max_tokens=100  # Adjust based on your needs
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit application
st.title("PDF Text Prediction with GPT-3.5")

# API key input
api_key = st.text_input("Enter your OpenAI API key:", type="password")

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None and api_key:
    # Extract text from the uploaded PDF
    pdf_text = extract_text_from_pdf(uploaded_file)
    
    st.write("PDF text extracted successfully. Enter your query below to get predictions.")
    
    # Text input for query
    query = st.text_input("Enter your query:")

    if query:
        # Create the prompt for GPT-3.5
        prompt = create_prompt(pdf_text, query)
        
        # Get the response from GPT-3.5
        with st.spinner("Generating response..."):
            response = get_gpt35_response(prompt, api_key)
        
        st.write("Response from GPT-3.5:")
        st.write(response)
    elif not query:
        st.write("Please enter a query to get a response.")
else:
    if not uploaded_file:
        st.write("Please upload a PDF file.")
    if not api_key:
        st.write("Please enter your OpenAI API key.")
