import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Feroz@13",
        database="password_strength_db"
    )
def save_password_result(password, strength):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO password_stats (password, strength) VALUES (%s, %s)"
    cursor.execute(query, (password, strength))
    conn.commit()
    cursor.close()
    conn.close()
