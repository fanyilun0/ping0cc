#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IP池质量检测结果表格生成器
读取ip_pool_quality.json文件并生成表格格式的报告
"""

import json
import pandas as pd
from datetime import datetime
import os

def load_detection_results(json_file='ip_pool_quality.json'):
    """加载检测结果数据"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"❌ 文件 {json_file} 不存在")
        return None
    except json.JSONDecodeError:
        print(f"❌ 文件 {json_file} 格式错误")
        return None

def create_results_table(data):
    """创建检测结果表格"""
    if not data or '检测结果' not in data:
        print("❌ 数据中没有检测结果")
        return None
    
    results = data['检测结果']
    
    # 过滤掉失败的检测结果（只有调试信息的）
    valid_results = []
    for result in results:
        if 'IP地址' in result and result.get('IP地址'):
            valid_results.append(result)
    
    if not valid_results:
        print("❌ 没有有效的检测结果")
        return None
    
    # 准备表格数据
    table_data = []
    for i, result in enumerate(valid_results, 1):
        row = {
            '序号': i,
            '检测时间': result.get('检测时间', ''),
            'IP地址': result.get('IP地址', ''),
            'IP位置': result.get('IP位置', ''),
            'IP类型': result.get('IP类型', ''),
            '风控值': result.get('风控值', ''),
            '风控等级': result.get('风控等级', ''),
            '原生IP': result.get('原生IP', ''),
            'ASN': result.get('ASN', ''),
            'ASN所有者': result.get('ASN所有者', ''),
            '企业': result.get('企业', ''),
            '国家代码': result.get('国家代码', '')
        }
        table_data.append(row)
    
    # 创建DataFrame
    df = pd.DataFrame(table_data)
    return df

def create_summary_table(data):
    """创建统计摘要表格"""
    if not data:
        return None
    
    summary_data = []
    
    # 基本统计
    summary_data.append(['检测统计', '总检测次数', data.get('总检测次数', 0)])
    summary_data.append(['', '成功检测次数', data.get('成功检测次数', 0)])
    summary_data.append(['', '失败检测次数', data.get('失败检测次数', 0)])
    success_rate = (data.get('成功检测次数', 0) / max(data.get('总检测次数', 1), 1)) * 100
    summary_data.append(['', '成功率', f'{success_rate:.1f}%'])
    summary_data.append(['', '平均风控值', f"{data.get('平均风控值', 0)}%"])
    
    # IP类型统计
    ip_types = data.get('IP类型统计', {})
    for ip_type, count in ip_types.items():
        percentage = (count / data.get('成功检测次数', 1)) * 100
        summary_data.append(['IP类型分布', ip_type, f'{count} ({percentage:.1f}%)'])
    
    # 风控等级统计
    risk_levels = data.get('风控等级统计', {})
    for risk_level, count in risk_levels.items():
        percentage = (count / data.get('成功检测次数', 1)) * 100
        summary_data.append(['风控等级分布', risk_level, f'{count} ({percentage:.1f}%)'])
    
    # 国家分布统计（前10）
    countries = data.get('国家分布统计', {})
    sorted_countries = sorted(countries.items(), key=lambda x: x[1], reverse=True)[:10]
    for country, count in sorted_countries:
        percentage = (count / data.get('成功检测次数', 1)) * 100
        summary_data.append(['国家分布(前10)', country, f'{count} ({percentage:.1f}%)'])
    
    # 原生IP统计
    native_ips = data.get('原生IP统计', {})
    for native_type, count in native_ips.items():
        percentage = (count / data.get('成功检测次数', 1)) * 100
        summary_data.append(['原生IP分布', native_type, f'{count} ({percentage:.1f}%)'])
    
    df_summary = pd.DataFrame(summary_data, columns=['分类', '项目', '数值'])
    return df_summary

def export_to_excel(df_results, df_summary, filename=None):
    """导出到Excel文件"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'IP检测结果报告_{timestamp}.xlsx'
    
    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # 写入检测结果
            if df_results is not None:
                df_results.to_excel(writer, sheet_name='检测结果明细', index=False)
            
            # 写入统计摘要
            if df_summary is not None:
                df_summary.to_excel(writer, sheet_name='统计摘要', index=False)
        
        print(f"✅ Excel报告已生成: {filename}")
        return filename
    except Exception as e:
        print(f"❌ 生成Excel文件失败: {e}")
        return None

def export_to_csv(df_results, filename=None):
    """导出到CSV文件"""
    if df_results is None:
        return None
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'IP检测结果_{timestamp}.csv'
    
    try:
        # 去除重复的IP地址，保留第一次出现的记录
        df_unique = df_results.drop_duplicates(subset=['IP地址'], keep='first')
        
        # 重新生成序号
        df_unique = df_unique.reset_index(drop=True)
        df_unique['序号'] = range(1, len(df_unique) + 1)
        
        # 显示去重信息
        original_count = len(df_results)
        unique_count = len(df_unique)
        removed_count = original_count - unique_count
        
        if removed_count > 0:
            print(f"🔄 已去除 {removed_count} 个重复IP地址 (原始: {original_count}, 去重后: {unique_count})")
        
        df_unique.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"✅ CSV文件已生成: {filename}")
        return filename
    except Exception as e:
        print(f"❌ 生成CSV文件失败: {e}")
        return None

def print_table_to_console(df_results, df_summary, max_rows=20):
    """在控制台打印表格"""
    print("\n" + "="*80)
    print("📊 IP池质量检测结果报告")
    print("="*80)
    
    if df_summary is not None:
        print("\n📈 统计摘要:")
        print("-"*60)
        print(df_summary.to_string(index=False))
    
    if df_results is not None:
        print(f"\n📋 检测结果明细 (显示前{min(max_rows, len(df_results))}条记录):")
        print("-"*80)
        
        # 选择要显示的关键列
        display_columns = ['序号', 'IP地址', 'IP位置', 'IP类型', '风控值', '风控等级', '原生IP']
        display_df = df_results[display_columns].head(max_rows)
        
        print(display_df.to_string(index=False, max_colwidth=20))
        
        if len(df_results) > max_rows:
            print(f"\n... 还有 {len(df_results) - max_rows} 条记录，请查看导出的文件")
    
    print("\n" + "="*80)

def main():
    """主函数"""
    print("🚀 IP池质量检测结果表格生成器")
    print("="*50)
    
    # 加载数据
    print("📂 加载检测数据...")
    data = load_detection_results()
    
    if data is None:
        return
    
    print(f"✅ 数据加载成功，共 {data.get('总检测次数', 0)} 条检测记录")
    
    # 创建表格
    print("📊 生成检测结果表格...")
    df_results = create_results_table(data)
    
    print("📈 生成统计摘要表格...")
    df_summary = create_summary_table(data)
    
    # 在控制台显示
    print_table_to_console(df_results, df_summary)
    
    # 询问用户是否要导出文件
    print("\n📁 文件导出选项:")
    print("1. 导出Excel文件 (推荐)")
    print("2. 导出CSV文件")
    print("3. 两种格式都导出")
    print("4. 只在控制台显示")
    
    try:
        choice = input("请选择 (1-4): ").strip()
        
        if choice in ['1', '3']:
            export_to_excel(df_results, df_summary)
        
        if choice in ['2', '3']:
            export_to_csv(df_results)
        
        if choice == '4':
            print("📺 仅在控制台显示完成")
        
    except KeyboardInterrupt:
        print("\n👋 用户取消操作")
    except Exception as e:
        print(f"❌ 操作失败: {e}")

if __name__ == "__main__":
    # 检查是否安装了pandas
    try:
        import pandas as pd
    except ImportError:
        print("❌ 缺少pandas库，请安装: pip install pandas openpyxl")
        exit(1)
    
    main() 