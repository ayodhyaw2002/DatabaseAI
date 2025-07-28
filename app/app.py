import pyodbc
import json
import google.generativeai as genai
from db import get_connection
import pandas as pd
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from llm_agent_gemini import fix_sqlserver_syntax , ask_llm 
    

#database connection
coxn= get_connection()
cursor = coxn.cursor() 


print("Starting the application...")

user_question = "how many SalesLT.Customer are there in the database?"


theuserQuery = ask_llm(user_question)



query = theuserQuery.replace("```sql", "").replace("```", "").strip()
print(query)





cursor.execute(query)
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







