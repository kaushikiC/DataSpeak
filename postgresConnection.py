import streamlit as st
import psycopg2
import pandas as pd
import time
import google.generativeai as genai

DB_HOST = "localhost"
DB_NAME = "postgres"  
DB_USER = "postgres"
DB_PASSWORD = "@Password1"

GOOGLE_API_KEY = "AIzaSyCZ_py6dmu9C8BVgxyVNgyWw6kKmr1pKJY"

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def main():
    st.set_page_config(page_title="AI Query Generator", page_icon=":robot:")
    st.markdown(
        """
        <style>
        .title {
            text-align: center;
            margin-bottom: 20px;
        }
        .query-container {
            margin-top: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # st.markdown('<h1 class="title">AI Query Generator</h1>', unsafe_allow_html=True)
    # st.markdown("<p>This tool generates and executes SQL queries based on your inputs.</p>", unsafe_allow_html=True)
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
    st.markdown("<h1 class='gradient-text'>Data Speak (SQL to SQL)</h1>", unsafe_allow_html=True)
    text_input = st.text_area("Enter your SQL Query here:")

    submit = st.button("Enhance SQL Query")
    if submit:
        start_time = time.time()
        with st.spinner("Enhancing SQL Query..."):
            template = """
                Enhance or modify the following SQL query snippet:
                ```sql
                {sql_input}
                ```
                Provide a modified SQL query with improvements or optimizations.
            """
            formatted_template = template.format(sql_input=text_input)
            
            response = model.generate_content(formatted_template)
            enhanced_sql_query = response.text.strip().lstrip("```sql").rstrip("```")

            expected_output_template = """
                What would be the expected response of this SQL query snippet:
                ```sql
                {sql_query}
                ```
                Provide sample tabular response with no explanation.
            """
            expected_output_formatted = expected_output_template.format(sql_query=enhanced_sql_query)
            
            expected_output_response = model.generate_content(expected_output_formatted)
            expected_output = expected_output_response.text.strip().lstrip("```sql").rstrip("```")

            with st.container():
                st.success("Enhanced SQL query generated successfully! Here is your query:")
                st.code(enhanced_sql_query, language="sql")

                st.success("Expected Output of this SQL Query:")
                st.code(expected_output, language="sql")

    execute = st.button("Execute SQL Query")
    if execute:
        start_time = time.time()
        with st.spinner("Executing SQL Query..."):
            try:
                conn = psycopg2.connect(
                    host=DB_HOST,
                    database=DB_NAME,
                    user=DB_USER,
                    password=DB_PASSWORD
                )
                cursor = conn.cursor()

                cursor.execute(text_input)
                rows = cursor.fetchall()
                
                col_names = [desc[0] for desc in cursor.description]

                st.success("SQL query executed successfully! Here are the results:")
                st.dataframe(pd.DataFrame(rows, columns=col_names))

                cursor.close()
                conn.close()
            except psycopg2.Error as e:
                st.error(f"An error occurred: {e}")
        
        end_time = time.time()
        st.info(f"SQL query execution took {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()

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
