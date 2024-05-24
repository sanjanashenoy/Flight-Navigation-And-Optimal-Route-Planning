import pandas as pd
import psycopg2

# Load the modified dataset
routes = pd.read_csv('cleaned_routes_with_predicted_delay.csv')

# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname="route_opti",
    user="postgres",
    password="sanj123",
    host="localhost"
)
cur = conn.cursor()

# Create the routes table if not exists
cur.execute("""
CREATE TABLE IF NOT EXISTS routes (
    id SERIAL PRIMARY KEY,
    origin_airport VARCHAR(3),
    destination_airport VARCHAR(3),
    distance INTEGER,
    predicted_delay INTEGER
);
""")

# Insert data into the database
for _, row in routes.iterrows():
    cur.execute("""
        INSERT INTO routes (origin_airport, destination_airport, distance, predicted_delay) 
        VALUES (%s, %s, %s, %s)
        """, (row['Origin'], row['Dest'], row['Distance'], row['Predicted_Delay']))

conn.commit()
cur.close()
conn.close()
