import hashlib
import os
from PyQt5.QtWidgets import QMessageBox


def hash_password(password):
    salt = os.urandom(32)
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + pwdhash


def verify_password(stored_password, provided_password):
    salt = stored_password[:32]
    stored_hash = stored_password[32:]
    pwdhash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
    return pwdhash == stored_hash


def show_message(parent, title, message, msg_type='warning'):
    if msg_type == 'warning':
        QMessageBox.warning(parent, title, message, QMessageBox.Yes)
    elif msg_type == 'information':
        QMessageBox.information(parent, title, message, QMessageBox.Yes)
    elif msg_type == 'critical':
        QMessageBox.critical(parent, title, message, QMessageBox.Yes)
    elif msg_type == 'question':
        return QMessageBox.question(parent, title, message, QMessageBox.Yes | QMessageBox.No)


def read_accounts(file_id, file_password):
    accounts = {}
    try:
        if not os.path.exists(file_id) or not os.path.exists(file_password):
            return accounts
        with open(file_id, 'r', encoding='utf-8') as f_id, open(file_password, 'rb') as f_pwd:
            ids = [line.strip() for line in f_id.readlines()]
            passwords = []
            while True:
                chunk = f_pwd.read(64)
                if not chunk:
                    break
                passwords.append(chunk)
            for i, user_id in enumerate(ids):
                if i < len(passwords):
                    accounts[user_id] = passwords[i]
    except Exception as e:
        print(f"读取账号信息失败: {e}")
    return accounts


def save_account(file_id, file_password, user_id, password_hash):
    try:
        os.makedirs(os.path.dirname(file_id), exist_ok=True)
        with open(file_id, 'a', encoding='utf-8') as f_id, open(file_password, 'ab') as f_pwd:
            f_id.write(user_id + '\n')
            f_pwd.write(password_hash)
        return True
    except Exception as e:
        print(f"保存账号信息失败: {e}")
        return False


def validate_date(date_str):
    try:
        parts = date_str.split('-')
        if len(parts) != 3:
            return False
        year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
        if month < 1 or month > 12:
            return False
        if day < 1 or day > 31:
            return False
        if month in [4, 6, 9, 11] and day > 30:
            return False
        if month == 2:
            is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
            if is_leap and day > 29:
                return False
            if not is_leap and day > 28:
                return False
        return True
    except:
        return False
