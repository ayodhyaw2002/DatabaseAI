# import pyodbc
# import json
# import google.generativeai as genai
# from db import get_connection
# import pandas as pd
# import sys
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from llm_agent_gemini import  ask_llm ,cleaned_Query


# #database connection
# coxn= get_connection()
# cursor = coxn.cursor()


# print("Starting the application...")

# user_question = "how many CustomerName stats with latter A  in the database?"


# theuserQuery = ask_llm(user_question)

# query = cleaned_Query(theuserQuery)

# print(query)


# cursor.execute(query)
# results = cursor.fetchall()
# print (results)

# if results :
#     print("Query executed successfully. Results:")
#     for row in results:
#         print(row)
# else:
#     print("No results found for the query.")
# # Close the cursor and connection
# cursor.close()
# coxn.close()


from flask import Flask, render_template, request, send_file
import pandas as pd
from db import get_connection
from io import BytesIO
from llm_agent_gemini import ask_llm, cleaned_Query

import pandas as pd
import plotly.express as px
import plotly
import json


app = Flask(__name__)


@app.route('/query', methods=['GET', 'POST'])
def query():
    sql_query = None
    results = None
    error_message = None

    if request.method == 'POST':
        user_question = request.form['user_question']

        try:
            # Get the SQL query using LLM
            theuserQuery = ask_llm(user_question)
            sql_query = cleaned_Query(theuserQuery)
            # df = run_sql_and_get_dataframe(sql_query)
            # df_available = True
            # latest_df = df

            # Connect and run the query
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(sql_query)
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()

            # Convert results to list of dicts
            results = [dict(zip(columns, row)) for row in rows]

            cursor.close()
            conn.close()

        except Exception as e:
            error_message = str(e)

    return render_template("index.html", sql_query=sql_query, results=results, error_message=error_message)



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
