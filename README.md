# 超市信息管理系统

一个基于 Python + PyQt5 开发的 GUI 超市信息管理系统，包含进货、售货、库存查询和登录管理功能。

## 功能特性

- **用户登录/注册**：支持新用户注册和登录验证，密码使用 PBKDF2 加密存储
- **进货录入**：录入商品进货信息，支持条形码自动补全已有商品信息
- **售货录入**：模拟超市收银界面，支持库存实时校验防止超卖
- **信息查询**：支持库存查询、进货查询、售货查询，可按条件筛选

## 技术栈

- Python 3.x
- PyQt5 - GUI 框架
- pyodbc - 数据库连接
- SQL Server - 数据库

## 安装说明

### 1. 克隆项目

```bash
git clone <repository-url>
cd Supermarket-shopping-system-Python
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置数据库

编辑 `code/config.py` 文件，修改数据库连接字符串：

```python
DB_CONNECTION_STRING = 'DRIVER={SQL Server};SERVER=localhost;DATABASE=SupermarketDB;UID=sa;PWD=your_password'
```

### 4. 创建数据库表

在 SQL Server 中执行以下脚本创建数据库和表：

```sql
-- 创建数据库
CREATE DATABASE SupermarketDB;
GO

USE SupermarketDB;
GO

-- 库存表
CREATE TABLE Inventory (
    intxm INT PRIMARY KEY,
    spmc NVARCHAR(100),
    kcl INT,
    sccs NVARCHAR(100),
    spgg NVARCHAR(50),
    lsj FLOAT
);

-- 进货表
CREATE TABLE Stock (
    sttxm INT,
    jj FLOAT,
    cgsl INT,
    cgrq NVARCHAR(20),
    FOREIGN KEY (sttxm) REFERENCES Inventory(intxm)
);

-- 销售表
CREATE TABLE Sellgoods (
    xstm INT,
    xssl INT,
    lsj FLOAT,
    xssj NVARCHAR(20),
    FOREIGN KEY (xstm) REFERENCES Inventory(intxm)
);
```

### 5. 运行程序

```bash
cd code
python Shop_denglu.py
```

## 项目结构

```
Supermarket-shopping-system-Python/
├── code/
│   ├── Shop_denglu.py      # 登录模块
│   ├── Shop_main.py        # 主窗口模块
│   ├── Shop_stock.py       # 进货录入模块
│   ├── Shop_sell.py        # 售货录入模块
│   ├── Shop_select.py      # 信息查询模块
│   ├── config.py           # 配置文件
│   └── utils.py            # 工具函数
├── img/
│   ├── denglu.jpg          # 登录界面背景
│   ├── main.jpg            # 主界面背景
│   ├── select.jpg          # 查询界面背景
│   └── stock.jpg           # 进货界面背景
├── txt/
│   ├── 账号.txt            # 账号存储文件
│   ├── 密码.txt            # 密码存储文件（加密）
│   └── 销售记录.txt        # 销售记录文件
├── requirements.txt        # 依赖列表
└── README.md               # 项目说明
```

## 使用说明

### 登录/注册

1. 首次使用需要点击"注册新用户"创建账号
2. 输入账号和密码进行登录
3. 密码使用 PBKDF2 算法加密存储

### 进货录入

1. 点击"进货录入"按钮进入进货界面
2. 输入条形码，如果商品已存在会自动补全信息
3. 填写完整的进货信息（商品名称、厂商、规格、进价、零售价、数量、日期）
4. 点击"录入"暂存，确认无误后点击"确定"保存到数据库

### 售货录入

1. 点击"售货录入"按钮进入收银界面
2. 输入条形码和销售数量
3. 系统会自动检查库存，库存不足时会提示
4. 商品会显示在表格中，自动计算总价
5. 输入实收金额，系统自动计算找零
6. 点击"确认"完成结算，打印小票

### 信息查询

1. 点击"信息查询"按钮进入查询界面
2. 支持三种查询：
   - **库存查询**：按商品名称或条形码查询当前库存
   - **进货查询**：按时间范围查询进货记录
   - **售货查询**：按时间范围查询销售记录

## 安全特性

- ✅ 密码使用 PBKDF2-SHA256 加密存储
- ✅ 使用盐值增强安全性
- ✅ 数据库操作使用参数化查询防止 SQL 注入
- ✅ 完善的异常处理机制

## 库存管理特性

- ✅ 实时库存校验，防止超卖
- ✅ 支持同一商品多次添加，自动计算可用库存
- ✅ 结算时事务处理，保证数据一致性
- ✅ 库存不足时友好提示

## 更新日志

### v2.0 (2026-03-13)
- 添加密码加密存储功能
- 添加库存校验防止超卖
- 修复文件路径问题，使用相对路径
- 添加完善的异常处理
- 优化代码结构，提取公共配置和工具函数

### v1.0
- 基础功能实现：登录、进货、售货、查询

## 注意事项

1. 请确保 SQL Server 已安装并启动
2. 请正确配置数据库连接字符串
3. 首次运行前请创建数据库和表结构
4. 图片文件请放在 img 目录下

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎提交 Issue 或 Pull Request。
