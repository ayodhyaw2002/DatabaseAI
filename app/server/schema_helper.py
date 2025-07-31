from db import get_connection
import uvicorn


#need to extablish new connection object again?

def get_all_schema():
  coxn = get_connection()
  cursor = coxn.cursor()
  
  #this is the guide to LLM
  
  #may be this is not the proper way to get schema...because this connect to the database and get the schema
  
  query="""
  SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE
  FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_NAME != 'sysdiagrams'  
  ORDER BY TABLE_NAME, COLUMN_NAME  ;"""
  
  cursor.execute(query)
  results  = cursor.fetchall()
  
  
  for table_name, column_name, data_type in results:print(f"🟦 Table: {table_name} | Column: {column_name} | Type: {data_type}") 
# write the schema to a file take foregn and primary key relationships into account   

  

  