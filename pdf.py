import streamlit as st
import PyPDF2
import os
from openai import OpenAI

# Ensure the OPENAI_API_KEY environment variable is set
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("The OpenAI API key has not been set in the environment variables.")

client = OpenAI(api_key=api_key)

def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful research assistant."},
            {"role": "user", "content": f"Summarize this: {text}"}
        ],
    )
    summary = response.choices[0].message["content"]
    return summary

def process_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    full_text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        page_text = page.extract_text().lower()
        full_text += page_text + "\n"
    return full_text

st.title("PDF Summary Generator")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Read and process the PDF file
    pdf_text = process_pdf(uploaded_file)
    
    # Summarize the text
    summary_text = summarize_text(pdf_text)
    
    # Display the original PDF and the summary
    st.write("### Summary")
    st.write(summary_text)
    
    st.write("### Original PDF")
    with open("uploaded.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.download_button(
        label="Download PDF",
        data=uploaded_file.getbuffer(),
        file_name="uploaded.pdf",
        mime="application/pdf"
    )
    
    with st.expander("Show PDF"):
        pdf_display = f'<iframe src="data:application/pdf;base64,{uploaded_file.getbuffer().encode("base64").decode()}" width="700" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
else:
    st.write("Please upload a PDF file to summarize.")
