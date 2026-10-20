
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from database import create_database, add_expense, get_expenses

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
