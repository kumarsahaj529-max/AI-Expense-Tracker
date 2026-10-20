import streamlit as st
from google import genai


def generate_insight(question, expense_summary):
    api_key = st.secrets["GEMINI_API_KEY"]
    model = st.secrets["GEMINI_MODEL"]

    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are an AI expense analysis assistant.

    Analyze the user's spending using only the supplied
    expense statistics. Do not invent figures.
    Give practical, easy-to-understand suggestions.
    Do not present your response as professional
    financial advice.

    Expense statistics:
    {expense_summary}

    User question:
    {question}
    """

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return response.text