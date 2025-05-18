import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
        sslmode=os.getenv("SSL_MODE", "require")
    )
    return conn


def create_table_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT NOT NULL UNIQUE,
            secret_code TEXT NOT NULL UNIQUE,
            score INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_secret_code(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT secret_code FROM users WHERE user_id = %s', (user_id,))
    secret_code = cursor.fetchone()
    cursor.close()
    conn.close()
    return secret_code


def get_top_leaders():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT user_id, score
        FROM users
        ORDER BY score DESC
        LIMIT 10
        '''
    )

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return format_answer(rows)

def format_answer(leaders):
    leader_positions = []
    for i in range(1, len(leaders) + 1):
        current_position = f"{i}: {leaders[i - 1][0]} {leaders[i - 1][1]}\n"
        leader_positions.append(current_position)
        if i == 3:
            leader_positions.append("-"*25 + "\n")

    answer = "".join(leader_positions)

    return answer

if __name__ == '__main__':
    get_top_leaders()
    # print(len('1: 4b88e001 469'))
    print(format_answer(()))
    res = 'good' if '' else 'пуст'
    print(res)