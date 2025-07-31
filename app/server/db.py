import pyodbc
import json


def get_connection():
    
    try:
        coxn = pyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=192.168.1.211;"
            "Database=AdventureWorksLT2022;"
            "UID=sa;"
            "PWD=Sqlserver2017;"
            "Encrypt=yes;"
            "TrustServerCertificate=yes;"
        )
         # create object from cursor to execute queries
        print("Connected to the database successfully.")

    except pyodbc.Error as e:
        print("Error connecting to the database:", e)
        sys.exit(1)
    
    return coxn



