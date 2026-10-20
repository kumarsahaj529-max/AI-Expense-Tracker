
import streamlit as st
from openai import OpenAI


def generate_insight(question, expense_summary):
    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"]
    )

    model = st.secrets["OPENAI_MODEL"]

    response = client.responses.create(
        model=model,
        instructions=(
            "You are an expense analysis assistant. "
            "Answer using only the supplied expense "
            "statistics. Do not invent figures. "
            "If the data is insufficient, say so. "
            "Do not present your answer as professional "
            "financial advice."
        ),
        input=(
            f"Expense statistics:\n{expense_summary}\n\n"
            f"User question: {question}"
        )
    )

    return response.output_text
