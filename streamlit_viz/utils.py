import os

import mysql.connector
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def get_dataframe():
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host="host.docker.internal",
        port=os.getenv("MYSQL_PORT"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database="weather",
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Execute the query to fetch the data
    query = "SELECT * FROM data"
    cursor.execute(query)

    # Fetch all the rows from the result
    rows = cursor.fetchall()

    # Get the column names from the cursor description
    column_names = [desc[0] for desc in cursor.description]

    # Create a Pandas DataFrame from the fetched data and column names
    df = pd.DataFrame(rows, columns=column_names)

    # Close the cursor and database connection
    cursor.close()
    conn.close()

    # Print the DataFrame
    return df
