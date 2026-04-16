import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()

@pytest.fixture
def temp_db():
    """Фикстура, которая создает чистую базу данных для каждого теста и удаляет её после."""
    create_db()
    yield
    try:
        if os.path.exists('users.db'):
            os.remove('users.db')
    except PermissionError:
        pass

def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."

def test_add_user_existing_username(temp_db):
    """Тест: добавление пользователя с уже существующим логином должно вернуть False"""
    # Добавляем первого пользователя
    result1 = add_user("alice", "alice@example.com", "pass123")
    assert result1 == True, "Первый пользователь должен добавиться успешно"  
    result2 = add_user("alice", "bob@example.com", "pass456")
    assert result2 == False, "Добавление пользователя с существующим логином должно вернуть False"

def test_authenticate_user_success(temp_db):
    """Тест: успешная аутентификация с правильными логином и паролем"""
    # Добавляем пользователя
    add_user("bob", "bob@example.com", "secret123")
    
    # Пытаемся аутентифицироваться с правильными данными
    result = authenticate_user("bob", "secret123")
    assert result == True, "Аутентификация с правильными данными должна вернуть True"

def test_authenticate_user_not_exists(temp_db):
    """Тест: аутентификация пользователя, которого нет в базе"""
    # Пытаемся аутентифицировать несуществующего пользователя
    result = authenticate_user("nonexistent", "anypass")
    assert result == False, "Аутентификация несуществующего пользователя должна вернуть False"

def test_authenticate_user_wrong_password(temp_db):
    """Тест: аутентификация с неправильным паролем"""
    # Добавляем пользователя
    add_user("charlie", "charlie@example.com", "correctpass")
    
    # Пытаемся аутентифицироваться с неправильным паролем
    result = authenticate_user("charlie", "wrongpass")
    assert result == False, "Аутентификация с неправильным паролем должна вернуть False"

def test_display_users(capsys, temp_db):
    """Тест: отображение списка пользователей должно выводить всех пользователей"""
    # Добавляем несколько пользователей
    add_user("alice", "alice@test.com", "pass1")
    add_user("bob", "bob@test.com", "pass2")
    add_user("charlie", "charlie@test.com", "pass3")
    
  
    display_users()
    captured = capsys.readouterr()
    
    
    assert "Логин: alice, Электронная почта: alice@test.com" in captured.out
    assert "Логин: bob, Электронная почта: bob@test.com" in captured.out
    assert "Логин: charlie, Электронная почта: charlie@test.com" in captured.out
# Возможные варианты тестов:
"""
Тест добавления пользователя с существующим логином.
Тест успешной аутентификации пользователя.
Тест аутентификации несуществующего пользователя.
Тест аутентификации пользователя с неправильным паролем.
Тест отображения списка пользователей.
"""