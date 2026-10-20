
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from database import (
    create_database,
    add_expense,
    get_expenses,
    delete_all_expenses
)
from ai_service import generate_insight

st.set_page_config(
    page_title="AI Expense Tracker",
    page_icon="💰",
    layout="wide"
)

create_database()

st.title("💰 AI Expense Tracker")
st.write("Track your expenses and understand your spending.")



# Expense entry form
st.subheader("Add a New Expense")

with st.form("expense_form"):
    amount = st.number_input(
        "Amount (₹)",
        min_value=0.01,
        value=100.0,
        step=10.0
    )

    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Shopping", "Bills", "Education", "Other"]
    )

    description = st.text_input("Description")

    expense_date = st.date_input(
        "Expense Date",
        value=date.today()
    )

    submitted = st.form_submit_button("Add Expense")

    
    if submitted:
      add_expense(
        amount,
        category,
        description,
        expense_date
    )

    st.success("Expense saved to database!")


# Display dashboard
expenses = get_expenses()

if expenses:
    df = pd.DataFrame(
        expenses,
        columns=[
            "ID",
            "Amount",
            "Category",
            "Description",
            "Date"
        ]
    )

    total_expenses = df["Amount"].sum()
    transaction_count = len(df)
    average_expense = total_expenses / transaction_count

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Expenses", f"₹{total_expenses:,.2f}")
    col2.metric("Transactions", transaction_count)
    col3.metric("Average Expense", f"₹{average_expense:,.2f}")

    st.subheader("Category-wise Spending")

    category_summary = (
        df.groupby("Category", as_index=False)["Amount"]
        .sum()
    )

    fig = px.pie(
        category_summary,
        names="Category",
        values="Amount",
        title="Where Your Money Goes"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("All Transactions")

    st.dataframe(
        df.sort_values("Date", ascending=False),
        use_container_width=True,
        hide_index=True
    )

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Expenses as CSV",
        data=csv_data,
        file_name="expenses.csv",
        mime="text/csv"
    )

else:
    st.info("No expenses yet. Add your first expense above.")



st.subheader("AI Expense Assistant")

expenses = get_expenses()

if expenses:
    df_ai = pd.DataFrame(
        expenses,
        columns=["ID", "Amount", "Category", "Description", "Date"]
    )

    total = float(df_ai["Amount"].sum())

    category_totals = (
        df_ai.groupby("Category")["Amount"].sum().to_dict()
    )

    expense_summary = (
        f"Total recorded expenses: Rs. {total:.2f}\n"
        f"Spending by category: {category_totals}"
    )

    question = st.chat_input("Ask about your spending...")

    if question:
        st.chat_message("user").write(question)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing your expenses..."):
                try:
                    answer = generate_insight(
                        question, expense_summary
                    )
                    st.write(answer)
                except Exception as e:
                  st.error(f"AI error: {type(e).__name__}: {e}")
else:
    st.info("Add expenses before asking the AI assistant.")


# Clear All Expenses
st.divider()
st.subheader("Reset Database")

if st.button("🗑️ Clear All Expenses"):
    st.session_state.confirm_delete = True

if st.session_state.get("confirm_delete", False):
    st.warning(
        "Are you sure? This will permanently delete all expenses."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Yes, Delete All", type="primary"):
            delete_all_expenses()
            st.session_state.confirm_delete = False
            st.success("All expenses have been deleted.")
            st.rerun()

    with col2:
        if st.button("Cancel"):
            st.session_state.confirm_delete = False
            st.rerun()
