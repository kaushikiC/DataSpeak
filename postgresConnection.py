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

    st.markdown('<h1 class="title">AI Query Generator</h1>', unsafe_allow_html=True)
    st.markdown("<p>This tool generates and executes SQL queries based on your inputs.</p>", unsafe_allow_html=True)

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