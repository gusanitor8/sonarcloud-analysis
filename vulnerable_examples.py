# vulnerable_examples.py
"""
❗️ CÓDIGO INTENCIONALMENTE INSEGURO – SOLO PARA PROBAR SONARCLOUD.
NO uses esto en producción. 
"""

import hashlib
import os
import pickle
import random
import shlex
import sqlite3
import subprocess
from pathlib import Path

DB_PATH = "users.db"
# VULN-1: Secreto hard-codeado (regla S2068 – “Hard-coded credentials”)
JWT_SECRET = os.getenv("JWT_SECRET", "default-secret")  # Usar variable de entorno con valor por defecto

def os_command_injection():
    """
    VULN-2: Inyección de comandos (regla S6073 / S5131)
    El usuario controla todo el comando.
    """
    cmd = input("Comando a ejecutar: ")
    safe_cmd = shlex.split(cmd)  # Sanitiza el comando dividiéndolo en argumentos seguros
    subprocess.run(safe_cmd, check=True)  # Usa subprocess.run para evitar shell injection

def sql_injection(name: str):
    """
    VULN-3: SQL injection (regla S3649)
    Concatenación directa en el query.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    query = f"SELECT * FROM users WHERE name = '{name}'"  # ⚠️ vulnerable
    cur.execute(query)
    print(cur.fetchall())
    conn.close()

def insecure_deserialization():
    """
    VULN-4: Deserialización insegura (regla S5135)
    Carga objetos arbitrarios desde entrada externa.
    """
    payload = input("Pega payload pickle: ")
    obj = pickle.loads(payload.encode())  # ⚠️ code execution risk
    print(obj)

def weak_crypto(password: str):
    """
    VULN-5: Algoritmo criptográfico débil (regla S2070)
    MD5 no es seguro para contraseñas.
    """
    digest = hashlib.md5(password.encode()).hexdigest()
    print(f"MD5 hash: {digest}")

def predictable_random_token():
    """
    EXTRA: Aleatoriedad predecible (regla S2245)
    """
    token = str(random.random())
    print(f"Token inseguro: {token}")

def path_traversal():
    """
    EXTRA: Path traversal (regla S2083)
    """
    filename = input("¿Qué archivo leer?: ")  # ../../etc/passwd
    data = Path(filename).read_text(encoding="utf-8")
    print(data)

if __name__ == "__main__":
    # Ejecuta alguna de las funciones para generar issues.
    os_command_injection()
