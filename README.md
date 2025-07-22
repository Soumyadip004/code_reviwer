# 🤖 AI Code Reviewer (Streamlit + Groq)

An interactive AI-powered code review tool built with **Streamlit** and **Groq Cloud** (using the DeepSeek LLaMA model).  
Easily review code, get improvements, and see complexity analysis instantly!

---

## ✨ Features

✅ Upload code files (`.py`, `.java`, `.c`, etc.) or paste code manually  
✅ Automatic language detection  
✅ AI review highlighting:
- Bugs & security issues
- Readability & performance improvements
- Suggested **full modified code**
- Time & space complexity analysis  
✅ Clear button to reset  
✅ Modern UI with yellow background, dark text, and green buttons  
✅ Side-by-side view: original vs. reviewed code

---

## 🚀 How it works

- The app sends your code and a smart prompt to Groq’s **DeepSeek LLaMA** model.
- The model analyzes your code and returns:
  - A detailed review
  - Fully corrected & improved version of the code
  - Complexity explanation

---

## 📦 Installation

1. Clone this repo or download the code.
2. Create a virtual environment (recommended):

```bash
python -m venv venv
# Activate it
# On Linux / macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
