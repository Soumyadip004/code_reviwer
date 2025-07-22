import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from groq import Groq
from pathlib import Path

# 🌟 Initialize Groq client
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("⚠️ Please set your GROQ_API_KEY in the .env file.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# 📦 Supported file types & language mapping
LANGUAGE_MAP = {
    'py': 'python',
    'java': 'java',
    'c': 'c',
    'cpp': 'cpp',
    'js': 'javascript',
    'ts': 'typescript',
    'html': 'html',
    'css': 'css',
    'go': 'go',
    'rb': 'ruby'
}

# 🌈 Custom background & style
st.markdown("""
    <style>
    .stApp {
        background: #ffeb3b;  /* yellow background */
        color: #222;          /* dark text */
    }
    .stTextInput>div>div>input,
    .stTextArea>div>textarea,
    .stFileUploader>div>div {
        background-color: #fff9c4;
        color: #222;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
    }
    .stButton>button:hover {
        background-color: #45a049;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ✅ Page config & title
st.set_page_config(page_title="🤖 AI Code Reviewer", page_icon="🤖")
st.title("🤖 AI Code Reviewer with Groq + DeepSeek")

# 📍 Session state
if 'code_text' not in st.session_state:
    st.session_state.code_text = ""
if 'review' not in st.session_state:
    st.session_state.review = ""

# 🚀 Choose input method
option = st.radio("Choose input method:", ("Upload file", "Enter code manually"))

detected_language = "text"  # default fallback

if option == "Upload file":
    uploaded_file = st.file_uploader(
        "Upload your code file",
        type=list(LANGUAGE_MAP.keys())
    )
    if uploaded_file is not None:
        try:
            file_ext = Path(uploaded_file.name).suffix[1:]
            detected_language = LANGUAGE_MAP.get(file_ext, "text")
            code_text = uploaded_file.read().decode("utf-8")
            st.session_state.code_text = code_text
            st.markdown(f"### 📄 Uploaded Code (`.{file_ext}`)")
            st.code(code_text, language=detected_language)
        except Exception as e:
            st.error(f"❌ Error reading file: {e}")
else:
    code_input = st.text_area("Paste your code here:", height=300)
    if code_input:
        st.session_state.code_text = code_input
        # simple guess
        if code_input.strip().startswith(("def", "class", "import")):
            detected_language = "python"
        else:
            detected_language = "text"

# ✏️ If no detected language, keep fallback
if not detected_language:
    detected_language = "text"

# 🧠 Review button & clear button side by side
col_btn1, col_btn2 = st.columns([1, 1])

with col_btn1:
    if st.button("🔍 Review Code"):
        if not st.session_state.code_text.strip():
            st.warning("⚠️ Please provide some code to review!")
        else:
            with st.spinner("Analyzing your code..."):
                prompt = f"""
You are an expert senior code reviewer.

Please do the following for the code below:
1. Identify and explain any bugs, security issues, or inefficiencies (as bullet points).
2. Suggest and apply improvements for clarity, readability, or performance.
3. Provide the **full modified (corrected and improved) code** inside a single code block using the same language.
4. Finally, describe the **time and space complexity** of the final code in simple terms.

Here is the code:
```{detected_language}
{st.session_state.code_text}
"""
                try:
                    response = client.chat.completions.create(
                        model="deepseek-r1-distill-llama-70b",
                        messages=[
                            {"role": "system", "content": "You are a senior software engineer and code reviewer."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.2
                    )
                    st.session_state.review = response.choices[0].message.content
                except Exception as e:
                    st.error(f"❌ Error: {e}")

with col_btn2:
    if st.button("🗑 Clear"):
        st.session_state.code_text = ""
        st.session_state.review = ""
        st.rerun()

if st.session_state.review:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📄 Original Code")
        st.code(st.session_state.code_text, language=detected_language)
    with col2:
        st.markdown("### ✅ AI Review & Updated Code")
        st.write(st.session_state.review)
    