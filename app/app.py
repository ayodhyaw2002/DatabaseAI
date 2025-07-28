import pyodbc
import json
import google.generativeai as genai
from db import get_connection
import pandas as pd
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from llm_agent_gemini import get_sql_query , ask_llm
    

#database connection
coxn= get_connection()
cursor = coxn.cursor() 


print("Starting the application...")

user_question = "how many SalesLT.Customer are there in the database?"


Query= get_sql_query(ask_llm(user_question))
print(Query)

cursor.execute(Query)
results = cursor.fetchall()
print (results)

if results :
    print("Query executed successfully. Results:")
    for row in results:
        print(row)
else:
    print("No results found for the query.")
# Close the cursor and connection
cursor.close()
coxn.close()



















#REST API







