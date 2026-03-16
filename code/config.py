import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CODE_DIR = os.path.join(BASE_DIR, 'code')
IMG_DIR = os.path.join(BASE_DIR, 'img')
TXT_DIR = os.path.join(BASE_DIR, 'txt')

IMG_DENGLO = os.path.join(IMG_DIR, 'denglu.jpg')
IMG_MAIN = os.path.join(IMG_DIR, 'main.jpg')
IMG_SELECT = os.path.join(IMG_DIR, 'select.jpg')
IMG_STOCK = os.path.join(IMG_DIR, 'stock.jpg')

FILE_ID = os.path.join(TXT_DIR, '账号.txt')
FILE_PASSWORD = os.path.join(TXT_DIR, '密码.txt')
FILE_SALES = os.path.join(TXT_DIR, '销售记录.txt')

DB_CONNECTION_STRING = 'DRIVER={SQL Server};SERVER=localhost;DATABASE=SupermarketDB;UID=sa;PWD=password'
