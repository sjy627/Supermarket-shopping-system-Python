import os
import hashlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TXT_DIR = os.path.join(BASE_DIR, 'txt')
IMG_DIR = os.path.join(BASE_DIR, 'img')
CODE_DIR = os.path.join(BASE_DIR, 'code')

ACCOUNT_FILE = os.path.join(TXT_DIR, '账号.txt')
PASSWORD_FILE = os.path.join(TXT_DIR, '密码.txt')
SALES_RECORD_FILE = os.path.join(TXT_DIR, '销售记录.txt')

def get_img_path(filename):
    return os.path.join(IMG_DIR, filename)

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(password, hashed_password):
    return hash_password(password) == hashed_password.strip()

DB_CONFIG = {
    'driver': 'SQL Server Native Client 10.0',
    'server': '192.168.43.220,1433',
    'database': 'Supermarket',
    'uid': 'sa',
    'pwd': 'Vv86865211'
}

def get_db_connection():
    import pyodbc
    conn_str = (
        f"DRIVER={{{DB_CONFIG['driver']}}};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"UID={DB_CONFIG['uid']};"
        f"PWD={DB_CONFIG['pwd']}"
    )
    return pyodbc.connect(conn_str)
