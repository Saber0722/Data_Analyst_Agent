import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pdfplumber
import pytesseract
from PIL import Image
import docx
import io
import os
from together import Together
from wordcloud import WordCloud

# Loading API Key and Model
together = Together(api_key=os.getenv("TOGETHER_API_KEY"))
MODEL = "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"

# Setting Page Config
st.set_page_config(page_title="Data Analyst Agent", layout="wide")
st.title("📊 Data Analyst AI Agent")

# Session state for history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "df" not in st.session_state:
    st.session_state.df = None
if "raw_text" not in st.session_state:
    st.session_state.raw_text = ""

# Extractors
def extract_text_from_txt(file): 
    return file.read().decode()
def extract_text_from_docx(file): 
    return "\n".join([p.text for p in docx.Document(file).paragraphs])
def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        return "\n".join([page.extract_text() or "" for page in pdf.pages])
def extract_text_from_image(file): 
    return pytesseract.image_to_string(Image.open(file))
def load_tabular_file(file):
    if file.name.endswith(".csv"): 
        return pd.read_csv(file)
    elif file.name.endswith(".xlsx"): 
        return pd.read_excel(file)
    else: 
        raise ValueError("Unsupported file type")

# Wordcloud
def show_wordcloud_from_text(text):
    if not text or not isinstance(text, str) or not text.strip():
        st.warning("No valid text found for generating word cloud.")
        return
    try:
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='black',
            colormap='plasma',
            collocations=False
        ).generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt.gcf())
        plt.clf()
    except Exception as e:
        st.error(f"Failed to generate word cloud: {e}")

# LLM Interaction
def ask_llm(messages):
    response = together.chat.completions.create(
        model=MODEL,
        messages=messages
    )
    return response.choices[0].message.content

# Plots and Visualizations
def handle_visual_command(command):
    df = st.session_state.get("df", None)
    text_data = st.session_state.get("raw_text", "")
    try:
        command = command.lower()
        # Word Cloud from Text
        if "word cloud" in command or "wordcloud" in command:
            if text_data.strip():
                fig, ax = plt.subplots(figsize=(10, 5))
                wordcloud = WordCloud(width=800, height=400, background_color='black', colormap='viridis').generate(text_data)
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis("off")
                ax.set_title("Word Cloud")
                st.pyplot(fig)
                plt.clf()
                return True
            else:
                st.warning("No text data found for generating word cloud.")
                return False
        if df is not None:
            # Bar/Count Plot
            if "bar" in command or "countplot" in command:
                col = command.split("of")[-1].strip()
                if col in df.columns:
                    plt.figure(figsize=(10, 5))
                    plt.title(f"Bar Chart of {col}")
                    sns.countplot(data=df, x=col)
                    st.pyplot(plt.gcf()); plt.clf()
                    return True
                else:
                    st.warning(f"Column '{col}' not found in DataFrame.")
                    return False
            # Histogram
            elif "hist" in command or "histogram" in command:
                col = command.split("of")[-1].strip()
                if col in df.columns:
                    plt.figure(figsize=(10, 5))
                    plt.title(f"Histogram of {col}")
                    df[col].hist()
                    st.pyplot(plt.gcf()); plt.clf()
                    return True
                else:
                    st.warning(f"Column '{col}' not found in DataFrame.")
                    return False
            # Scatter Plot
            elif "scatter" in command:
                if " vs " in command:
                    parts = command.split("of")[-1].split(" vs ")
                    x, y = parts[0].strip(), parts[1].strip()
                    if x in df.columns and y in df.columns:
                        plt.figure(figsize=(10, 5))
                        plt.title(f"Scatter Plot of {x} vs {y}")
                        sns.scatterplot(data=df, x=x, y=y)
                        st.pyplot(plt.gcf()); plt.clf()
                        return True
                    else:
                        st.warning(f"Column(s) '{x}' or '{y}' not found in DataFrame.")
                        return False
                else:
                    st.warning("Scatter plot format should be: 'scatter plot of column1 vs column2'")
                    return False
        return False
    except Exception as e:
        st.error(f"Plot Error: {e}")
        return False

# File Upload Box
uploaded_file = st.file_uploader("Upload any file", type=["txt", "docx", "pdf", "csv", "xlsx", "png", "jpg", "doc", "jpeg"])

# Checking for uploaded file format and processing it
if uploaded_file:
    file_name = uploaded_file.name.lower()
    try:
        # Text files
        if file_name.endswith(".txt"):
            st.session_state.raw_text = extract_text_from_txt(uploaded_file)
            st.success("Text file processed.")
            st.subheader("Extracted Text")
            st.text_area("Text", st.session_state.raw_text, height=200)
            st.subheader("Word Cloud")
            show_wordcloud_from_text(st.session_state.raw_text)
        # Word documents
        elif file_name.endswith((".docx", ".doc")):
            st.session_state.raw_text = extract_text_from_docx(uploaded_file)
            st.success("Word document processed.")
            st.subheader("Extracted Text")
            st.text_area("Text", st.session_state.raw_text, height=200)
            st.subheader("Word Cloud")
            show_wordcloud_from_text(st.session_state.raw_text)
        # PDFs
        elif file_name.endswith(".pdf"):
            st.session_state.raw_text = extract_text_from_pdf(uploaded_file)
            st.success("PDF processed.")
            st.subheader("Extracted Text")
            st.text_area("Text", st.session_state.raw_text, height=200)
        # Images
        elif file_name.endswith((".png", ".jpg", ".jpeg")):
            st.session_state.raw_text = extract_text_from_image(uploaded_file)
            st.success("Image processed.")
            st.subheader("Extracted Text")
            st.text_area("Text", st.session_state.raw_text, height=200)
        # Tabular files
        elif file_name.endswith((".csv", ".xlsx")):
            df = load_tabular_file(uploaded_file)
            st.session_state.df = df
            st.session_state.raw_text = df.head(10).to_markdown()
            st.success("Tabular file processed.")
            st.subheader("📄 Sample of Uploaded Data")
            st.dataframe(df.head())
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        st.stop()

# Chat Interface
st.subheader("💬 Ask a question")
user_input = st.text_input("Enter your question")
if st.button("Ask"):
    if not st.session_state.raw_text:
        st.warning("Please upload a file first.")
    else:
        history = st.session_state.chat_history
        content_block = f"Dataset/Text:\n{st.session_state.raw_text}\n\nUser: {user_input}"
        messages = [{"role": "system", "content": "You are a helpful data analyst."}]
        for past in history:
            messages.append({"role": "user", "content": past["question"]})
            messages.append({"role": "assistant", "content": past["answer"]})
        messages.append({"role": "user", "content": content_block})
        response = ask_llm(messages)
        st.session_state.chat_history.append({"question": user_input, "answer": response})
        st.markdown(f"**🧠 LLM Response:**\n\n{response}")
        handled = handle_visual_command(user_input.lower())
        if not handled:
            handle_visual_command(response.lower())
            
# Display chat history
if st.session_state.chat_history:
    st.subheader("📚 Chat History")
    for item in st.session_state.chat_history:
        st.markdown(f"**You:** {item['question']}")
        st.markdown(f"**LLM:** {item['answer']}")