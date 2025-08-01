from db import get_connection
import pandas as pd

def get_all_schema():
    # ✅ Get a new DB connection
    conn = get_connection()
    cursor = conn.cursor()

    # ✅ SQL to get all table schemas
    query = """
    SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, DATA_TYPE
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME != 'sysdiagrams'
    ORDER BY TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME;
    """

  
    df = pd.read_sql(query, conn)
    tables = {}

    
    for row in df.itertuples(index=False):
        schema = row.TABLE_SCHEMA
        table = row.TABLE_NAME
        col = row.COLUMN_NAME
        dtype = row.DATA_TYPE

        key = f"{schema}.{table}"
        if key not in tables:
            tables[key] = []
        tables[key].append(f"{col} {dtype}")

   
    schema_description = "\n".join(
        [f"{table} ({', '.join(cols)})" for table, cols in tables.items()]
    )

    print(schema_description)
    return schema_description

# Run it to test
if __name__ == "__main__":
    get_all_schema()