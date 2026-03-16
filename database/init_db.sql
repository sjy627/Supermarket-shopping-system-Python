-- 超市信息管理系统数据库初始化脚本
-- 创建日期: 2026-03-13

-- 创建数据库
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'SupermarketDB')
BEGIN
    CREATE DATABASE SupermarketDB;
END
GO

USE SupermarketDB;
GO

-- 删除已存在的表（如果需要重新创建）
IF OBJECT_ID('Sellgoods', 'U') IS NOT NULL DROP TABLE Sellgoods;
IF OBJECT_ID('Stock', 'U') IS NOT NULL DROP TABLE Stock;
IF OBJECT_ID('Inventory', 'U') IS NOT NULL DROP TABLE Inventory;
GO

-- 创建库存表
CREATE TABLE Inventory (
    intxm INT PRIMARY KEY,                    -- 条形码
    spmc NVARCHAR(100) NOT NULL,              -- 商品名称
    kcl INT DEFAULT 0,                        -- 库存量
    sccs NVARCHAR(100),                       -- 生产厂商
    spgg NVARCHAR(50),                        -- 商品规格
    lsj FLOAT NOT NULL                        -- 零售价
);

-- 创建进货表
CREATE TABLE Stock (
    id INT IDENTITY(1,1) PRIMARY KEY,         -- 自增ID
    sttxm INT NOT NULL,                       -- 条形码
    jj FLOAT NOT NULL,                        -- 进价
    cgsl INT NOT NULL,                        -- 采购数量
    cgrq NVARCHAR(20) NOT NULL,               -- 采购日期
    FOREIGN KEY (sttxm) REFERENCES Inventory(intxm)
);

-- 创建销售表
CREATE TABLE Sellgoods (
    id INT IDENTITY(1,1) PRIMARY KEY,         -- 自增ID
    xstm INT NOT NULL,                        -- 条形码
    xssl INT NOT NULL,                        -- 销售数量
    lsj FLOAT NOT NULL,                       -- 零售价
    xssj NVARCHAR(20) NOT NULL,               -- 销售时间
    FOREIGN KEY (xstm) REFERENCES Inventory(intxm)
);

-- 创建索引以提高查询性能
CREATE INDEX IX_Inventory_spmc ON Inventory(spmc);
CREATE INDEX IX_Stock_sttxm ON Stock(sttxm);
CREATE INDEX IX_Stock_cgrq ON Stock(cgrq);
CREATE INDEX IX_Sellgoods_xstm ON Sellgoods(xstm);
CREATE INDEX IX_Sellgoods_xssj ON Sellgoods(xssj);
GO

-- 插入测试数据
-- 测试商品数据
INSERT INTO Inventory (intxm, spmc, kcl, sccs, spgg, lsj) VALUES
(1001, N'可口可乐', 100, N'可口可乐公司', N'500ml', 3.5),
(1002, N'百事可乐', 80, N'百事公司', N'500ml', 3.5),
(1003, N'雪碧', 120, N'可口可乐公司', N'500ml', 3.5),
(1004, N'方便面', 200, N'康师傅', N'袋装', 4.5),
(1005, N'薯片', 50, N'乐事', N'70g', 6.0),
(1006, N'巧克力', 60, N'德芙', N'43g', 8.5),
(1007, N'牛奶', 40, N'伊利', N'250ml*12', 45.0),
(1008, N'面包', 30, N'桃李', N'300g', 5.5);

-- 测试进货记录
INSERT INTO Stock (sttxm, jj, cgsl, cgrq) VALUES
(1001, 2.5, 100, '2026-03-01'),
(1002, 2.5, 80, '2026-03-01'),
(1003, 2.5, 120, '2026-03-02'),
(1004, 3.0, 200, '2026-03-03'),
(1005, 4.0, 50, '2026-03-04'),
(1006, 6.0, 60, '2026-03-05'),
(1007, 35.0, 40, '2026-03-06'),
(1008, 3.5, 30, '2026-03-07');

-- 测试销售记录
INSERT INTO Sellgoods (xstm, xssl, lsj, xssj) VALUES
(1001, 2, 3.5, '2026-03-10 09:30:00'),
(1004, 5, 4.5, '2026-03-10 10:15:00'),
(1006, 1, 8.5, '2026-03-10 11:20:00'),
(1002, 3, 3.5, '2026-03-10 14:45:00'),
(1007, 1, 45.0, '2026-03-10 16:00:00');

GO

-- 创建视图方便查询
-- 库存视图
CREATE VIEW View_Inventory AS
SELECT 
    i.intxm AS 条形码,
    i.spmc AS 商品名称,
    i.sccs AS 生产厂商,
    i.spgg AS 规格,
    i.lsj AS 零售价,
    i.kcl AS 库存量
FROM Inventory i;
GO

-- 进货记录视图
CREATE VIEW View_Stock AS
SELECT 
    s.id AS 记录ID,
    s.sttxm AS 条形码,
    i.spmc AS 商品名称,
    s.jj AS 进价,
    s.cgsl AS 采购数量,
    s.cgrq AS 采购日期
FROM Stock s
INNER JOIN Inventory i ON s.sttxm = i.intxm;
GO

-- 销售记录视图
CREATE VIEW View_Sales AS
SELECT 
    s.id AS 记录ID,
    s.xstm AS 条形码,
    i.spmc AS 商品名称,
    i.spgg AS 规格,
    s.lsj AS 零售价,
    s.xssl AS 销售数量,
    s.xssj AS 销售时间
FROM Sellgoods s
INNER JOIN Inventory i ON s.xstm = i.intxm;
GO

PRINT '数据库初始化完成！';
