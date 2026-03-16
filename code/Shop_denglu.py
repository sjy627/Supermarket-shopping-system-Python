import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Shop_main import *
from config import IMG_DENGLO, FILE_ID, FILE_PASSWORD
from utils import hash_password, verify_password, show_message, read_accounts, save_account


class denglu(QWidget):
    """
    登录窗口 ：程序的入口
    登录窗口的内容包括两个tabel标签："账号"、"密码"，两个输入框分别用来输入账号及密码
    两个按钮：确定和退出，一个radiobutton用来设置密码的显示格式，一个显示标签用来创建新的账号
    密码在输入时应该默认为掩码输入，点击radiobutton时可以切换密码显示格式
    点击显示标签"创建新用户"时弹出创建窗口
    创建新账号时应该进行核查：账号不许为空不许重复，密码不许为空
    创建完成时把账号及密码存储在本地文件中：账号.txt、密码.txt  并退出关闭创建窗口
    登录时应核查账号与密码的匹配，并根据各种出错情况给出相应的提示信息
    登陆成功时进入主页面并自动退出关闭登录窗口
    """
    def __init__(self):
        super(denglu, self).__init__()
        self.resize(400, 247)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.initUI()
        
    def initUI(self):
        self.label_null1 = QLabel()
        self.label_null2 = QLabel()
        self.label_null3 = QLabel()
        self.label_null4 = QLabel()
        self.label_new = QLabel()
        
        self.label_new.setText("<a href='#'>注册新用户</a>")
        self.label_new.setStyleSheet('''color: rgb(253,129,53);''')
        self.label_new.linkActivated.connect(self.idnew)
        
        self.btn_check = QRadioButton("显示密码")
        self.btn_check.setStyleSheet('''color: rgb(253,129,53);''')
        self.btn_check.clicked.connect(self.yanma)
        
        self.btn_denglu = QPushButton("登录")
        self.btn_quxiao = QPushButton("退出")
        self.btn_denglu.setStyleSheet('''color: white;
                        background-color: rgb(218,181,150);''')
        self.btn_quxiao.setStyleSheet('''color: white;
                        background-color: rgb(218,181,150);''')
        self.btn_denglu.clicked.connect(self.check)
        self.btn_quxiao.clicked.connect(self.quxiao)
        
        self.lineedit_id = QLineEdit()
        self.lineedit_id.setPlaceholderText("账号")
        self.lineedit_password = QLineEdit()
        self.lineedit_password.setEchoMode(QLineEdit.Password)
        self.lineedit_password.setPlaceholderText("密码")
        
        layout = QHBoxLayout(self)
        wid_denglu_right = QWidget()
        wid_denglu_left = QLabel()
        g = QGridLayout()
        g.addWidget(self.lineedit_id, 1, 1, 1, 2)
        g.addWidget(self.lineedit_password, 2, 1, 1, 2)
        g.addWidget(self.btn_check, 3, 1)
        g.addWidget(self.btn_denglu, 4, 1)
        g.addWidget(self.btn_quxiao, 4, 2)
        g.addWidget(self.label_null1, 5, 1)
        g.addWidget(self.label_null2, 6, 1)
        g.addWidget(self.label_null3, 7, 1)
        g.addWidget(self.label_null4, 8, 1)
        g.addWidget(self.label_new, 9, 2)
        wid_denglu_right.setLayout(g)
        layout.addWidget(wid_denglu_left)
        layout.addWidget(wid_denglu_right)
        self.setLayout(layout)
        
    def yanma(self):
        if self.btn_check.isChecked():
            self.lineedit_password.setEchoMode(QLineEdit.Normal)
        else:
            self.lineedit_password.setEchoMode(QLineEdit.Password)
            
    def check(self):
        try:
            username = self.lineedit_id.text().strip()
            password = self.lineedit_password.text()
            
            if not username or not password:
                show_message(self, "提示", "账号和密码不能为空", "warning")
                return
            
            accounts = read_accounts(FILE_ID, FILE_PASSWORD)
            
            if username not in accounts:
                show_message(self, "提示", "账号或密码输入错误", "warning")
                return
            
            stored_hash = accounts[username]
            if verify_password(stored_hash, password):
                show_message(self, "成功", "登录成功！", "information")
                self.shop = Shopmain()
                self.shop.show()
                self.close()
            else:
                show_message(self, "提示", "账号或密码输入错误", "warning")
                
        except Exception as e:
            show_message(self, "错误", f"登录失败：{str(e)}", "critical")
            
    def idnew(self):
        self.label_idnew_id = QLabel("账号")
        self.label_idnew_password = QLabel("密码")
        self.lineedit_idnew_id = QLineEdit()
        self.lineedit_idnew_password = QLineEdit()
        self.btn_idnew_quren = QPushButton("注册")
        self.btn_idnew_quren.clicked.connect(self.idnewqueren)
        self.btn_idnew_quxiao = QPushButton("取消")
        self.btn_idnew_quxiao.clicked.connect(self.idnewclose)
        self.idnew_window = QWidget()
        layout_idnew = QGridLayout()
        layout_idnew.addWidget(self.label_idnew_id, 1, 0)
        layout_idnew.addWidget(self.label_idnew_password, 2, 0)
        layout_idnew.addWidget(self.lineedit_idnew_id, 1, 1, 1, 2)
        layout_idnew.addWidget(self.lineedit_idnew_password, 2, 1, 1, 2)
        layout_idnew.addWidget(self.btn_idnew_quren, 3, 1)
        layout_idnew.addWidget(self.btn_idnew_quxiao, 3, 2)
        self.idnew_window.setLayout(layout_idnew)
        self.idnew_window.move(self.pos())
        self.idnew_window.resize(200, 133)
        self.idnew_window.setWindowFlags(Qt.FramelessWindowHint)
        self.idnew_window.setStyleSheet("background-color :rgb(253,216,174)")
        self.idnew_window.show()
        
    def idnewqueren(self):
        try:
            username = self.lineedit_idnew_id.text().strip()
            password = self.lineedit_idnew_password.text()
            
            if not username:
                show_message(self, "提示", "账号不能为空", "warning")
                return
            
            accounts = read_accounts(FILE_ID, FILE_PASSWORD)
            if username in accounts:
                show_message(self, "提示", "账号已存在", "warning")
                return
            
            if not password:
                show_message(self, "提示", "密码不能为空", "warning")
                return
            
            password_hash = hash_password(password)
            if save_account(FILE_ID, FILE_PASSWORD, username, password_hash):
                show_message(self, "成功", "注册成功！", "information")
                self.idnew_window.close()
            else:
                show_message(self, "错误", "注册失败，请重试", "critical")
                
        except Exception as e:
            show_message(self, "错误", f"注册失败：{str(e)}", "critical")
            
    def paintEvent(self, event):
        painter = QPainter(self)
        try:
            pixmap = QPixmap(IMG_DENGLO)
            if not pixmap.isNull():
                painter.drawPixmap(self.rect(), pixmap)
        except Exception as e:
            print(f"加载背景图片失败: {e}")
            
    def idnewclose(self):
        self.idnew_window.close()
        
    def quxiao(self):
        sys.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    d = denglu()
    d.show()
    sys.exit(app.exec())
