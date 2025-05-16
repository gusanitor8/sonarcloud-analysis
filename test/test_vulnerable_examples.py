import hashlib
import pytest
from vulnerable_examples import sql_injection, weak_crypto

def test_weak_crypto(capsys):
    weak_crypto("admin123")
    captured = capsys.readouterr()
    digest = hashlib.sha256("admin123".encode()).hexdigest()
    assert digest in captured.out

def test_sql_injection(monkeypatch, capsys):
    import sqlite3

    # Crear DB temporal con una tabla de prueba
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
    cur.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
    conn.commit()
    conn.close()

    sql_injection("Alice")
    captured = capsys.readouterr()
    assert "Alice" in captured.out