#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据格式转换脚本
将PDF用户指南转为Markdown文本
将Excel数据转为CSV格式
"""

import os
import sys
import json
import pandas as pd
from pathlib import Path

def pdf_to_markdown(pdf_path, output_md_path):
    """
    将PDF转换为Markdown文本
    
    Args:
        pdf_path: PDF文件路径
        output_md_path: 输出Markdown文件路径
    """
    try:
        import pdfplumber
        
        print(f"正在读取PDF文件: {pdf_path}")
        
        with open(output_md_path, 'w', encoding='utf-8') as md_file:
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                md_file.write(f"# PDF文档转换\n\n")
                md_file.write(f"**源文件**: {pdf_path}\n")
                md_file.write(f"**总页数**: {total_pages}\n")
                md_file.write(f"**转换时间**: {pd.Timestamp.now()}\n\n")
                md_file.write("---\n\n")
                
                for idx, page in enumerate(pdf.pages, 1):
                    md_file.write(f"## 第 {idx} 页\n\n")
                    
                    # 提取文本
                    text = page.extract_text()
                    if text:
                        md_file.write(text)
                    
                    # 提取表格
                    tables = page.extract_tables()
                    if tables:
                        md_file.write(f"\n\n### 页面中的表格\n\n")
                        for table_idx, table in enumerate(tables, 1):
                            md_file.write(f"#### 表 {idx}-{table_idx}\n\n")
                            # 转换为DataFrame用于格式化
                            df = pd.DataFrame(table[1:], columns=table[0] if table else None)
                            md_file.write(df.to_markdown(index=False))
                            md_file.write("\n\n")
                    
                    md_file.write("\n---\n\n")
        
        print(f"✓ PDF已转换为Markdown: {output_md_path}")
        return True
        
    except ImportError:
        print("❌ 缺少pdfplumber库，请运行: pip install pdfplumber")
        return False
    except Exception as e:
        print(f"❌ PDF转换失败: {e}")
        return False


def excel_to_csv(excel_path, output_csv_path):
    """
    将Excel转换为CSV格式
    
    Args:
        excel_path: Excel文件路径
        output_csv_path: 输出CSV文件路径
    """
    try:
        print(f"正在读取Excel文件: {excel_path}")
        
        # 读取Excel
        df = pd.read_excel(excel_path)
        
        # 输出基本信息
        print(f"  - 行数: {len(df)}")
        print(f"  - 列数: {len(df.columns)}")
        print(f"  - 列名: {list(df.columns)}")
        
        # 保存为CSV
        df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
        
        print(f"✓ Excel已转换为CSV: {output_csv_path}")
        return True
        
    except Exception as e:
        print(f"❌ Excel转换失败: {e}")
        return False


def excel_to_json(excel_path, output_json_path):
    """
    将Excel转换为JSON格式
    
    Args:
        excel_path: Excel文件路径
        output_json_path: 输出JSON文件路径
    """
    try:
        print(f"正在读取Excel文件: {excel_path}")
        
        # 读取Excel
        df = pd.read_excel(excel_path)
        
        # 转换为JSON（记录格式）
        json_data = df.to_json(orient='records', force_ascii=False, indent=2)
        
        with open(output_json_path, 'w', encoding='utf-8') as f:
            f.write(json_data)
        
        print(f"✓ Excel已转换为JSON: {output_json_path}")
        return True
        
    except Exception as e:
        print(f"❌ Excel转换失败: {e}")
        return False


def generate_data_summary(excel_path, output_md_path):
    """
    生成数据文档摘要
    
    Args:
        excel_path: Excel文件路径
        output_md_path: 输出Markdown文件路径
    """
    try:
        print(f"正在生成数据摘要: {excel_path}")
        
        df = pd.read_excel(excel_path)
        
        with open(output_md_path, 'w', encoding='utf-8') as md_file:
            md_file.write("# 2024大样本死胎数据说明文档\n\n")
            
            # 数据基本信息
            md_file.write("## 数据概览\n\n")
            md_file.write(f"- **数据行数**: {len(df)}\n")
            md_file.write(f"- **数据列数**: {len(df.columns)}\n")
            md_file.write(f"- **数据生成时间**: {pd.Timestamp.now()}\n\n")
            
            # 列信息
            md_file.write("## 数据字段\n\n")
            md_file.write("| 序号 | 字段名 | 数据类型 | 非空数 | 唯一值 | 说明 |\n")
            md_file.write("|------|-------|--------|-------|-------|------|\n")
            
            for idx, col in enumerate(df.columns, 1):
                dtype = str(df[col].dtype)
                non_null = df[col].notna().sum()
                unique = df[col].nunique()
                md_file.write(f"| {idx} | {col} | {dtype} | {non_null} | {unique} | |\n")
            
            md_file.write("\n")
            
            # 数据样本
            md_file.write("## 数据示例（前10行）\n\n")
            md_file.write(df.head(10).to_markdown(index=False))
            md_file.write("\n\n")
            
            # 统计信息
            md_file.write("## 统计信息\n\n")
            md_file.write("### 数值列统计\n\n")
            md_file.write(df.describe().to_markdown())
            md_file.write("\n\n")
            
            # 缺失值
            md_file.write("## 数据质量\n\n")
            md_file.write("### 缺失值统计\n\n")
            missing = df.isnull().sum()
            if missing.sum() > 0:
                md_file.write(missing[missing > 0].to_markdown())
            else:
                md_file.write("✓ 数据完整，无缺失值")
            md_file.write("\n\n")
        
        print(f"✓ 数据摘要已生成: {output_md_path}")
        return True
        
    except Exception as e:
        print(f"❌ 生成摘要失败: {e}")
        return False


def main():
    """主函数"""
    
    print("=" * 60)
    print("数据格式转换工具")
    print("=" * 60)
    print()
    
    # 定义文件路径
    pdf_file = "2024死胎用户指南.pdf"
    excel_file = "2024大样本死胎.xlsx"
    
    # 输出文件
    md_guide = "docs/2024死胎用户指南.md"
    csv_data = "data/2024大样本死胎.csv"
    json_data = "data/2024大样本死胎.json"
    data_summary = "docs/数据说明文档.md"
    
    # 创建输出目录
    os.makedirs("docs", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    # 执行转换
    results = {
        "PDF转Markdown": False,
        "Excel转CSV": False,
        "Excel转JSON": False,
        "数据摘要生成": False
    }
    
    print("\n[1] 转换PDF为Markdown...")
    if os.path.exists(pdf_file):
        results["PDF转Markdown"] = pdf_to_markdown(pdf_file, md_guide)
    else:
        print(f"⚠ 文件不存在: {pdf_file}")
    
    print("\n[2] 转换Excel为CSV...")
    if os.path.exists(excel_file):
        results["Excel转CSV"] = excel_to_csv(excel_file, csv_data)
    else:
        print(f"⚠ 文件不存在: {excel_file}")
    
    print("\n[3] 转换Excel为JSON...")
    if os.path.exists(excel_file):
        results["Excel转JSON"] = excel_to_json(excel_file, json_data)
    else:
        print(f"⚠ 文件不存在: {excel_file}")
    
    print("\n[4] 生成数据说明文档...")
    if os.path.exists(excel_file):
        results["数据摘要生成"] = generate_data_summary(excel_file, data_summary)
    else:
        print(f"⚠ 文件不存在: {excel_file}")
    
    # 总结
    print("\n" + "=" * 60)
    print("转换结果总结")
    print("=" * 60)
    for task, status in results.items():
        status_str = "✓ 成功" if status else "✗ 失败"
        print(f"{task}: {status_str}")
    
    print("\n输出文件位置:")
    print(f"  - Markdown指南: {md_guide}")
    print(f"  - CSV数据: {csv_data}")
    print(f"  - JSON数据: {json_data}")
    print(f"  - 数据文档: {data_summary}")


if __name__ == "__main__":
    main()
