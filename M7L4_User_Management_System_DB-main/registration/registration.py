import sqlite3
import os

def create_db():
    """Создает базу данных users.db и таблицу users."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username, email, password):
    """
    Добавляет нового пользователя в базу данных.
    Возвращает True, если пользователь успешно добавлен, иначе False.
    """
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:  # username уже существует
        conn.close()
        return False

def authenticate_user(username, password):
    """
    Проверяет существование пользователя и соответствие пароля.
    Возвращает True, если пользователь существует и пароль верный, иначе False.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    )
    result = cursor.fetchone()
    conn.close()
    
    if result and result[0] == password:
        return True
    return False

def display_users():
    """Выводит в консоль список всех пользователей с их данными."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username, email FROM users")
    users = cursor.fetchall()
    conn.close()
    
    for username, email in users:
        print(f"Логин: {username}, Электронная почта: {email}")

def initialize_users():
    """Для обратной совместимости со старым кодом."""
    # Эта функция больше не используется с БД
    pass