import psycopg2


conn = psycopg2.connect(
    dbname="bookreviewsdb",
    user="postgres",
    password="1234",
    host="localhost"
)

cur = conn.cursor()

# Create tables
cur.execute('''
CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES books(id) ON DELETE CASCADE,
    review_text TEXT NOT NULL
)
''')

conn.commit()
cur.close()
conn.close()

print("Tables created successfully.")
