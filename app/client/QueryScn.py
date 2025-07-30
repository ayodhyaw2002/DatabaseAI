import streamlit as st
import requests

st.title("LLM SQL Query Runner")

user_question = st.text_input("Ask your question:")

if st.button("Run Query"):
    if user_question:
        with st.spinner("Sending to backend..."):
            response = requests.post(
                "http://localhost:8000/query",
                json={"user_question": user_question}
            )
            data = response.json()

            if "error" in data:
                st.error(data["error"])
            else:
                st.code(data["sql_query"], language='sql')
                st.dataframe(data["results"])
    else:
        st.warning("Please enter a question.")
