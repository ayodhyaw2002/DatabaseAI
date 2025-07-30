import pyodbc
import json
import google.generativeai as genai
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from llm_agent_gemini import  ask_llm ,cleaned_Query
from db import get_connection
from io import BytesIO
from llm_agent_gemini import ask_llm, cleaned_Query
import pandas as pd
import plotly.express as px
import plotly
import json
from pydantic import BaseModel




app = FastAPI()
# CORS configuration

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:8501"] to be more strict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryInput(BaseModel):
    user_question: str
    

#database connection
coxn= get_connection()
cursor = coxn.cursor()


print("Starting the application...")





@app.post("/query")
def run_query(input_data: QueryInput):
    try:
        theuserQuery = ask_llm(input_data.user_question)
        sql_query = cleaned_Query(theuserQuery)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql_query)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        results = [dict(zip(columns, row)) for row in rows]
        cursor.close()
        conn.close()

        return {"sql_query": sql_query, "results": results}

    except Exception as e:
        return {"error": str(e)}


@app.route('/chart', methods=['GET', 'POST'])
def chart():
    chart_html = None
    sql_query = None
    error_message = None

    if request.method == 'POST':
        user_prompt = request.form['user_prompt']

        try:
            theuserQuery = ask_llm(user_prompt)
            print (f"Generated SQL Query: {theuserQuery}")
            sql_query = cleaned_Query(theuserQuery)

            # Run SQL Query
            conn = get_connection()
            
            #sql cleaned
            df = pd.read_sql(sql_query, conn)
            conn.close()

            # Generate chart using Plotly
            if df.shape[1] < 2:
                raise Exception(
                    "Query should return at least 2 columns for charting")

            fig = px.bar(
                df, x=df.columns[0], y=df.columns[1], title="Chart from SQL Result")
            chart_html = fig.to_html(full_html=False)

        except Exception as e:
            error_message = str(e)

    return render_template("chart.html", chart_html=chart_html, sql_query=sql_query, error_message=error_message)


if __name__ == "__main__":
    app.run(debug=True)


# #REST API
