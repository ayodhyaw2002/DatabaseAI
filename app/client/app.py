import streamlit as st
import requests
from streamlit_navigation_bar import st_navbar


# page = st_navbar(
#   ["Ask Me" , "Generate Chart"]
# )
st.title("Chat with M+")

user_question = st.text_input("Ask your question:")

if st.button("Run Query"):
    if user_question:
        with st.spinner("Thinking ..."):
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
