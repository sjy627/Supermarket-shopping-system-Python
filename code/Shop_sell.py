import sys
import pyodbc
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from config import DB_CONNECTION_STRING, FILE_SALES
from utils import show_message


class Shopsell(QWidget):
    """
    销售（sell）录入系统：
    模仿现实中超市的售货界面
    收货时只需要输入条形码及商品数量，系统自动计算总价并将详细信息显示在窗口中央的表格中
    每次销售商品种类及数量都不相同，在点结算之前所有信息都只是暂存于列表中，只有点击结算
    后才会将信息存储进售货表中
    结算时，信息存入数据库并且将其中一部分信息以TXT形式存储于文本文件中，此处模仿超市打印小票
    销售商品时时间应该精确到秒
    在点击确认结算时要先判断是否输入有预售卖的商品，如果没有弹出提示框
    """
    def __init__(self):
        super(Shopsell, self).__init__()
        self.initUI()
        self.temp_sales = []
        
    def initUI(self):
        self.setGeometry(60, 60, 1000, 600)
        label_sell_title = QLabel("售货录入")
        label_sell_title.setFont(QFont("华文行楷", 25))
        label_txm = QLabel("条形码")
        label_xssl = QLabel("销售数量")
        label_sell1 = QLabel("总计")
        label_sell2 = QLabel("应收")
        label_sell3 = QLabel("实收")
        label_sell4 = QLabel("找零")
        
        self.line_txm = QLineEdit()
        self.line_txm.setValidator(QIntValidator())
        self.line_xssl = QLineEdit()
        self.line_xssl.setValidator(QIntValidator())
        
        self.line_sell1 = QLineEdit()
        self.line_sell2 = QLineEdit()
        self.line_sell3 = QLineEdit()
        self.line_sell4 = QLineEdit()
        self.line_sell1.setText("0.0")
        self.line_sell2.setText("0.0")
        self.line_sell3.setText("0.0")
        self.line_sell3.textChanged.connect(self.jiesuan)
        self.line_sell3.selectionChanged.connect(self.jiesuan0)
        self.line_sell4.setText("0.0")
        self.line_sell1.setReadOnly(True)
        self.line_sell2.setReadOnly(True)
        self.line_sell4.setReadOnly(True)
        self.line_sell1.setFixedSize(150, 20)
        self.line_sell2.setFixedSize(150, 20)
        self.line_sell3.setFixedSize(150, 20)
        self.line_sell4.setFixedSize(150, 20)
        
        btn_sell_lr = QPushButton("录入")
        btn_sell_lr.clicked.connect(self.event_lr)
        btn_sell_qr = QPushButton("确认")
        btn_sell_qr.clicked.connect(self.event_qr)
        btn_sell_ql = QPushButton("清零")
        btn_sell_ql.clicked.connect(self.event_ql)
        btn_sell_qr.setFixedSize(150, 20)
        btn_sell_ql.setFixedSize(150, 20)
        
        self.tabel_sell = QTableWidget()
        self.tabel_sell.setRowCount(20)
        self.tabel_sell.setColumnCount(6)
        self.tabel_sell.setHorizontalHeaderLabels(["条形码", "商品名称", "单价", "数量", "总计", "销售时间"])
        self.tabel_sell.setColumnWidth(5, 200)
        self.tabel_sell.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        layout = QVBoxLayout(self)
        v1 = QVBoxLayout()
        h1 = QHBoxLayout()
        h2 = QHBoxLayout()
        h3 = QHBoxLayout()
        v2 = QVBoxLayout()
        f = QFormLayout()
        w_title = QWidget()
        w_21 = QWidget()
        w_22 = QWidget()
        w_31 = QWidget()
        w_321 = QWidget()
        w_321.setFixedSize(235, 330)
        w_322 = QWidget()
        
        v1.addWidget(label_sell_title, 0, Qt.AlignCenter)
        h1.addWidget(label_txm)
        h1.addWidget(self.line_txm)
        h1.addWidget(label_xssl)
        h1.addWidget(self.line_xssl)
        h2.addWidget(btn_sell_lr)
        h3.addWidget(self.tabel_sell)
        f.addRow(label_sell1, self.line_sell1)
        f.addRow(label_sell2, self.line_sell2)
        f.addRow(label_sell3, self.line_sell3)
        f.addRow(label_sell4, self.line_sell4)
        v2.addWidget(btn_sell_qr, Qt.AlignCenter | Qt.AlignVCenter)
        v2.addWidget(btn_sell_ql, Qt.AlignCenter | Qt.AlignVCenter)
        w_title.setLayout(v1)
        w_21.setLayout(h1)
        w_22.setLayout(h2)
        w_31.setLayout(h3)
        w_321.setLayout(f)
        w_322.setLayout(v2)
        
        splitter_sell1 = QSplitter(Qt.Horizontal)
        splitter_sell1.setSizes([800, 80])
        splitter_sell1.addWidget(w_title)
        splitter_sell2 = QSplitter(Qt.Horizontal)
        splitter_sell2.setSizes([150, 60])
        splitter_sell2.addWidget(w_22)
        splitter_sell3 = QSplitter(Qt.Horizontal)
        splitter_sell3.addWidget(w_21)
        splitter_sell3.addWidget(splitter_sell2)
        splitter_sell4 = QSplitter(Qt.Vertical)
        splitter_sell4.setSizes([800, 140])
        splitter_sell4.addWidget(splitter_sell1)
        splitter_sell4.addWidget(splitter_sell3)
        splitter_sell5 = QSplitter(Qt.Horizontal)
        splitter_sell5.setSizes([150, 60])
        splitter_sell5.addWidget(w_322)
        splitter_sell6 = QSplitter(Qt.Vertical)
        splitter_sell6.addWidget(w_321)
        splitter_sell6.addWidget(splitter_sell5)
        splitter_sell7 = QSplitter(Qt.Horizontal)
        splitter_sell7.setSizes([700, 390])
        splitter_sell7.addWidget(self.tabel_sell)
        splitter_sell8 = QSplitter(Qt.Horizontal)
        splitter_sell8.addWidget(splitter_sell7)
        splitter_sell8.addWidget(splitter_sell6)
        splitter_sell9 = QSplitter(Qt.Vertical)
        splitter_sell9.addWidget(splitter_sell4)
        splitter_sell9.addWidget(splitter_sell8)
        layout.addWidget(splitter_sell9)
        self.setLayout(layout)
        
        self.Row = 0
        
    def get_db_connection(self):
        try:
            return pyodbc.connect(DB_CONNECTION_STRING)
        except Exception as e:
            show_message(self, "错误", f"数据库连接失败：{str(e)}", "critical")
            return None
            
    def check_stock(self, txm, quantity):
        conn = self.get_db_connection()
        if not conn:
            return False, 0
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT kcl FROM Inventory WHERE intxm=?", (txm,))
            row = cursor.fetchone()
            if not row:
                return False, 0
            available_stock = row[0]
            for sale in self.temp_sales:
                if sale['txm'] == txm:
                    available_stock -= sale['quantity']
            return quantity <= available_stock, available_stock
        except Exception as e:
            show_message(self, "错误", f"查询库存失败：{str(e)}", "critical")
            return False, 0
        finally:
            conn.close()
            
    def event_lr(self):
        try:
            if not self.line_txm.text():
                show_message(self, "提示", "请输入条形码！", "warning")
                return
            if not self.line_xssl.text():
                show_message(self, "提示", "请输入商品数量！", "warning")
                return
            txm = int(self.line_txm.text())
            xssl = int(self.line_xssl.text())
            if xssl <= 0:
                show_message(self, "提示", "销售数量必须大于0！", "warning")
                return
            conn = self.get_db_connection()
            if not conn:
                return
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Inventory WHERE intxm=?", (txm,))
            row = cursor.fetchone()
            conn.close()
            if not row:
                show_message(self, "提示", "商品不存在！", "warning")
                return
            has_stock, available = self.check_stock(txm, xssl)
            if not has_stock:
                show_message(self, "提示", f"库存不足！当前可用库存：{available}", "warning")
                return
            newItem1 = QTableWidgetItem(str(row[0]))
            newItem2 = QTableWidgetItem(row[1])
            newItem3 = QTableWidgetItem(str(row[5]))
            newItem4 = QTableWidgetItem(str(xssl))
            newItem5 = QTableWidgetItem(str(float("%.1f" % (row[5] * xssl))))
            newItem6 = QTableWidgetItem(time.strftime("%Y-%m-%d %H:%M:%S"))
            self.tabel_sell.setItem(self.Row, 0, newItem1)
            self.tabel_sell.setItem(self.Row, 1, newItem2)
            self.tabel_sell.setItem(self.Row, 2, newItem3)
            self.tabel_sell.setItem(self.Row, 3, newItem4)
            self.tabel_sell.setItem(self.Row, 4, newItem5)
            self.tabel_sell.setItem(self.Row, 5, newItem6)
            
            total = float(self.line_sell1.text() or 0) + row[5] * xssl
            self.line_sell1.setText(str(float("%.1f" % total)))
            self.line_sell2.setText(self.line_sell1.text())
            
            self.temp_sales.append({
                'txm': txm,
                'spmc': row[1],
                'lsj': float(row[5]),
                'quantity': xssl,
                'time': time.strftime("%Y-%m-%d %H:%M:%S")
            })
            
            self.line_txm.setText("")
            self.line_xssl.setText("")
            self.Row += 1
            
        except ValueError:
            show_message(self, "错误", "请输入有效的数字！", "warning")
        except Exception as e:
            show_message(self, "错误", f"录入失败：{str(e)}", "critical")
            
    def jiesuan(self):
        try:
            paid = float(self.line_sell3.text() or 0)
            total = float(self.line_sell2.text() or 0)
            change = paid - total
            self.line_sell4.setText(str(float("%.1f" % change)))
        except ValueError:
            pass
            
    def jiesuan0(self):
        self.line_sell3.setText("")
        
    def event_qr(self):
        if not self.temp_sales:
            show_message(self, "提示", "未添加商品！", "warning")
            return
        try:
            paid = float(self.line_sell3.text() or 0)
            total = float(self.line_sell2.text() or 0)
            if paid < total:
                show_message(self, "提示", "实收金额不足！", "warning")
                return
            conn = self.get_db_connection()
            if not conn:
                return
            cursor = conn.cursor()
            
            with open(FILE_SALES, "a", encoding='utf-8') as xsjl:
                xsjl.write("*******************************************************************\n")
                xsjl.write("商品名称\t\t\t\t          单价  数量    总计\n\n")
                
                for sale in self.temp_sales:
                    xsjl.write(f"{sale['spmc']}\t\t\t\t{sale['lsj']:.1f}\t{sale['quantity']}\t{sale['lsj'] * sale['quantity']:.1f}\n")
                    cursor.execute("INSERT INTO Sellgoods VALUES (?, ?, ?, ?)",
                                 (sale['txm'], sale['quantity'], sale['lsj'], sale['time']))
                    cursor.execute("SELECT kcl FROM Inventory WHERE intxm=?", (sale['txm'],))
                    row = cursor.fetchone()
                    if row:
                        new_stock = row[0] - sale['quantity']
                        cursor.execute("UPDATE Inventory SET kcl=? WHERE intxm=?", (new_stock, sale['txm']))
                
                conn.commit()
                xsjl.write("___________________________________________________________________\n")
                xsjl.write(f"总计：{total:.1f}\n")
                xsjl.write(f"实收：{paid:.1f}\n")
                xsjl.write(f"找零：{float(self.line_sell4.text() or 0):.1f}\n\n")
                xsjl.write(time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                xsjl.write("*******************************************************************\n")
            
            conn.close()
            show_message(self, "成功", "结算完成！", "information")
            self.event_ql()
            
        except Exception as e:
            show_message(self, "错误", f"结算失败：{str(e)}", "critical")
            
    def event_ql(self):
        self.line_sell1.setText("0.0")
        self.line_sell2.setText("0.0")
        self.line_sell3.setText("0.0")
        self.line_sell4.setText("0.0")
        self.Row = 0
        self.temp_sales = []
        for i in range(20):
            for j in range(6):
                self.tabel_sell.setItem(i, j, QTableWidgetItem(""))
                
    def paintEvent(self, event):
        painter = QPainter(self)
        try:
            from config import IMG_SELECT
            pixmap = QPixmap(IMG_SELECT)
            if not pixmap.isNull():
                painter.drawPixmap(self.rect(), pixmap)
        except Exception as e:
            print(f"加载背景图片失败: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sell = Shopsell()
    sell.show()
    sys.exit(app.exec())
