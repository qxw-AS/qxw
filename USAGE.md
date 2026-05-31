# 数据转换工具使用指南

## 目录
1. [安装步骤](#安装步骤)
2. [运行转换](#运行转换)
3. [文件说明](#文件说明)
4. [常见问题](#常见问题)
5. [进阶用法](#进阶用法)

## 安装步骤

### 前置要求
- Python 3.7 或以上版本
- pip 包管理工具

### 步骤1：获取项目文件

```bash
# 克隆项目（如果还没有）
git clone https://github.com/qxw-AS/qxw.git
cd qxw
```

### 步骤2：创建虚拟环境（推荐）

```bash
# Windows用户
python -m venv venv
venv\Scripts\activate

# macOS/Linux用户
python3 -m venv venv
source venv/bin/activate
```

### 步骤3：安装依赖

```bash
pip install -r requirements.txt
```

**可能遇到的问题：**

如果pip安装速度慢，可以使用国内镜像：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 运行转换

### 快速开始

```bash
python convert_files.py
```

**预期输出：**
```
============================================================
数据格式转换工具
============================================================

[1] 转换PDF为Markdown...
正在读取PDF文件: 2024死胎用户指南.pdf
  - 总页数: XX
✓ PDF已转换为Markdown: docs/2024死胎用户指南.md

[2] 转换Excel为CSV...
正在读取Excel文件: 2024大样本死胎.xlsx
  - 行数: XXXX
  - 列数: XX
  - 列名: [...]
✓ Excel已转换为CSV: data/2024大样本死胎.csv

[3] 转换Excel为JSON...
正在读取Excel文件: 2024大样本死胎.xlsx
✓ Excel已转换为JSON: data/2024大样本死胎.json

[4] 生成数据说明文档...
正在生成数据摘要: 2024大样本死胎.xlsx
✓ 数据摘要已生成: docs/数据说明文档.md

============================================================
转换结果总结
============================================================
PDF转Markdown: ✓ 成功
Excel转CSV: ✓ 成功
Excel转JSON: ✓ 成功
数据摘要生成: ✓ 成功

输出文件位置:
  - Markdown指南: docs/2024死胎用户指南.md
  - CSV数据: data/2024大样本死胎.csv
  - JSON数据: data/2024大样本死胎.json
  - 数据文档: docs/数据说明文档.md
```

## 文件说明

### 输入文件

| 文件名 | 类型 | 说明 |
|-------|------|------|
| `2024死胎用户指南.pdf` | PDF | 原始用户指南文档 |
| `2024大样本死胎.xlsx` | Excel | 原始数据文件 |

### 输出文件

#### 1. Markdown文档
- **路径**: `docs/2024死胎用户指南.md`
- **用途**: 
  - GitHub上直接查看
  - 作为文档存档
  - 便于搜索和查询
- **打开方式**: 
  - 任何文本编辑器
  - GitHub网页直接查看
  - Markdown预览工具

#### 2. CSV数据
- **路径**: `data/2024大样本死胎.csv`
- **用途**:
  - Excel直接打开
  - 导入数据库
  - 任何支持CSV的工具
- **特点**:
  - UTF-8编码
  - 逗号分隔
  - 支持中文

#### 3. JSON数据
- **路径**: `data/2024大样本死胎.json`
- **用途**:
  - Web应用使用
  - REST API返回数据
  - 编程语言处理
- **格式**: Records格式（数组of对象）

#### 4. 数据说明
- **路径**: `docs/数据说明文档.md`
- **包含内容**:
  - 数据统计信息
  - 字段列表和类型
  - 数据样本
  - 质量分析

## 常见问题

### Q1: 运行时出现 "No module named 'pdfplumber'"

**原因**: 缺少pdfplumber库

**解决方案**:
```bash
pip install pdfplumber
# 或重新安装所有依赖
pip install -r requirements.txt
```

### Q2: Excel文件找不到

**原因**: 脚本找不到Excel文件

**解决方案**:
1. 确保 `2024大样本死胎.xlsx` 在项目根目录
2. 检查文件名是否完全匹配
3. 确保文件没有被其他程序占用

### Q3: 输出文件夹不存在

**问题表现**: 报错 "No such file or directory"

**解决方案**: 脚本会自动创建，确保有写权限

### Q4: PDF转换后是空文件

**原因**: 可能是扫描版PDF（图片形式）

**解决方案**: 
- 使用OCR工具（如Tesseract）
- 或手动提取文本

### Q5: 中文显示乱码

**原因**: 编码问题

**解决方案**:
- CSV和JSON均使用UTF-8编码
- 用支持UTF-8的编辑器打开
- Excel中选择UTF-8导入

### Q6: 如何只转换部分内容？

**方案1**: 注释掉不需要的函数调用

编辑 `convert_files.py` 的主函数部分：
```python
# 注释这些行来跳过不需要的转换
# print("\n[1] 转换PDF为Markdown...")
# if os.path.exists(pdf_file):
#     results["PDF转Markdown"] = pdf_to_markdown(pdf_file, md_guide)
```

**方案2**: 直接调用特定函数

```python
from convert_files import excel_to_csv

# 只转换CSV
excel_to_csv('2024大样本死胎.xlsx', 'data/2024大样本死胎.csv')
```

## 进阶用法

### 1. 在Python中使用转换后的数据

#### 使用CSV
```python
import pandas as pd

# 加载数据
df = pd.read_csv('data/2024大样本死胎.csv')

# 查看基本信息
print(f"行数: {len(df)}")
print(f"列数: {len(df.columns)}")
print(f"列名: {df.columns.tolist()}")

# 查看前5行
print(df.head())

# 查看数据摘要
print(df.describe())
```

#### 使用JSON
```python
import json

# 加载数据
with open('data/2024大样本死胎.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 遍历所有记录
for record in data:
    print(record)

# 获取特定字段
first_values = [r['字段名'] for r in data]
```

### 2. 数据过滤和分析

```python
import pandas as pd

df = pd.read_csv('data/2024大样本死胎.csv')

# 按条件过滤
filtered = df[df['某字段'] > 10]

# 分组统计
grouped = df.groupby('分组字段').agg({
    '统计字段': ['count', 'mean', 'sum']
})

# 数据透视表
pivot = pd.pivot_table(df, values='值字段', 
                       index='行字段', 
                       columns='列字段', 
                       aggfunc='sum')

# 保存结果
result.to_csv('output.csv', index=False)
```

### 3. 修改脚本以适应新数据

如果有新的Excel或PDF文件，只需修改文件名：

```python
# 在 main() 函数中修改这些行
pdf_file = "新PDF文件名.pdf"
excel_file = "新Excel文件名.xlsx"
```

### 4. 批量处理多个文件

```python
import os
from convert_files import excel_to_csv

# 找到所有xlsx文件
for file in os.listdir('.'):
    if file.endswith('.xlsx'):
        csv_file = file.replace('.xlsx', '.csv')
        excel_to_csv(file, csv_file)
        print(f"已转换: {file}")
```

### 5. 集成到自动化流程

```bash
# 创建shell脚本 (Linux/macOS)
#!/bin/bash
cd /path/to/project
source venv/bin/activate
python convert_files.py
# 可以添加后续处理，如上传到服务器
```

```batch
# 创建批处理脚本 (Windows)
@echo off
cd C:\path\to\project
venv\Scripts\activate
python convert_files.py
REM 后续处理
```

## 技术支持

遇到问题？

1. **检查文件**: 确保源文件存在且格式正确
2. **检查日志**: 运行脚本并查看错误信息
3. **查看Issue**: https://github.com/qxw-AS/qxw/issues
4. **联系开发者**: 825094670@qq.com

---

**更新时间**: 2026-05-31
