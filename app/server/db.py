import pyodbc
import json


def get_connection():
    
    try:
        coxn = pyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=DESKTOP-1D87M7U\SQLEXPRESS;"
            "Database=AdventureWorksLT2022;"
            "UID=sa;"
            "PWD=weerabahu1234;"
            "Encrypt=yes;"
            "TrustServerCertificate=yes;"
        )
         # create object from cursor to execute queries
        print("Connected to the database successfully.")

    except pyodbc.Error as e:
        print("Error connecting to the database:", e)
        sys.exit(1)
    
    return coxn



