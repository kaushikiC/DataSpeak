import streamlit as st
import sqlite3
from dotenv import load_dotenv
import os
import google.generativeai as gg
import pandas as pd
from constants import prompt
import random

load_dotenv()
gg.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question,prompt):
    
    model=gg.GenerativeModel('gemini-pro')
    res=model.generate_content([prompt[0],question])
    return res.text

def read_sql_query(sql, db):
    
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        
        col_names = []
        for desc in cur.description:
            col_names.append(desc[0])
            
        conn.commit()
        conn.close()

        return rows, col_names
    
    except sqlite3.Error as e:
        print(f"Error executing SQL query: {str(e)}")
        raise


# Streamlit App
st.set_page_config(page_title="SQL Query Generator with Gemini Pro")
# Create a container for the logo and heading
col1, col2 = st.columns([1, 4])  # Adjust the ratio as needed

with col1:
    # Add logo using Streamlit's st.image function
    st.image("./lloyds-logo.svg", width=200, use_column_width='auto')  # Ensure the path is correct

with col2:
    # Add heading with green text and centered alignmen
    st.markdown(
    """
    <div style='height:50px; font-size: 48px; line-height:1;font-weight:600; color: green; text-align: center; display: flex; flex-direction: column; justify-content: flex-start;gap:0rem;'>
        Lloyds Technology Centre
    </div>
    """,
    unsafe_allow_html=True
)

# Define gradient colors (rainbow-like)
colors = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#8B00FF"]  # Red, Orange, Yellow, Green, Blue, Indigo, Violet

# Format the heading with HTML and CSS gradient
gradient_css = """
    <style>
        .gradient-text {
            background: linear-gradient(to right, """ + ", ".join(colors) + """);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 48px;
            font-weight: bold;
            padding:0px;
        }
    </style>
"""

# Display the styled heading
st.markdown(gradient_css, unsafe_allow_html=True)
st.markdown("<h1 class='gradient-text'>Data Speak</h1>", unsafe_allow_html=True)
# st.title("Ask Your Database Questions in English")

question = st.text_input("Enter your question:",placeholder="Generate Queries and Interact with Database")

question_button = st.button("Generate Query")

if question_button:
    if not question:
        st.warning("Please enter a question.")
    else:
        # Generate SQL query using Gemini model
        ai_response = get_gemini_response(question, prompt)
        cleaned_sql = ai_response.strip().strip('```').strip().strip('sql').strip()

        # Display generated SQL query
        st.markdown("##### Generated SQL Query")
        st.code(cleaned_sql, language='sql')

        try:
            sql_response, col_names = read_sql_query(cleaned_sql, "adventureworks.db")

            st.markdown("##### Query Output")
            if len(sql_response) > 0:
                table_data = [col_names] + list(sql_response)
                df = pd.DataFrame(table_data[1:], columns=table_data[0])
                st.dataframe(df) 
            # Remove DML statements
            if ai_response.strip().lower().startswith(("insert", "update", "delete")):
                st.success("Query execution successful.")
        except Exception as e:
            st.error(f"Error executing SQL query: {str(e)}")


# Custom CSS for the button
st.markdown(
    """
    <style>
    .stButton button {
        color: white;
        background-color: green;
        font-size: 24px;
        padding: 12px 24px;
        border-radius: 4px;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

