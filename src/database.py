import psycopg2
import pandas as pd
 
def extract_data_from_postgres(query, connection_params, output_csv):
    """
    1. Data Extraction from PostgreSQL
    2. Saving emails in a CSV file
 
    :param query: SQL Query
    :param connection_params: Dictionary with host, database, user, password.
    :param output_csv: Percorso del file CSV di output.
    """
    try:
        # DB Connection
        conn = psycopg2.connect(**connection_params)
        # Query execution and DataFrame uploading
        df = pd.read_sql_query(query, conn)
        # CSV saving
        df.to_csv(output_csv, index=False)
        print(f"Data saved with success in {output_csv}")
    except Exception as e:
        print(f"Error during data extraction: {e}")
    finally:
        conn.close()