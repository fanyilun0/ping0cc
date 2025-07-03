#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动态代理IP池质量统计工具 - 主程序入口
通过重复访问ping0.cc检测不同IP的质量
"""

import json
import time
import os
import signal
import sys
from datetime import datetime
from advanced_checker import AdvancedPing0CCChecker

class IPPoolQualityAnalyzer:
    """IP池质量分析器"""
    
    def __init__(self, data_file='ip_pool_quality.json', max_checks=100, delay_between_checks=5, 
                 proxy_url="http://127.0.0.1:7890", use_real_site=True):
        self.data_file = data_file
        self.max_checks = max_checks
        self.delay_between_checks = delay_between_checks
        self.proxy_url = proxy_url
        self.use_real_site = use_real_site
        self.current_count = 0
        self.total_stats = {
            "检测开始时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "总检测次数": 0,
            "成功检测次数": 0,
            "失败检测次数": 0,
            "IP类型统计": {},
            "风控等级统计": {},
            "国家分布统计": {},
            "ASN分布统计": {},
            "原生IP统计": {},
            "平均风控值": 0,
            "检测结果": []
        }
        
        # 设置信号处理器，支持优雅退出
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """处理退出信号"""
        print(f"\n🔄 接收到退出信号，正在保存数据...")
        self.save_final_stats()
        print("✅ 数据已保存，程序退出")
        sys.exit(0)
    
    def load_existing_data(self):
        """加载现有数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict) and "检测结果" in data:
                        self.total_stats = data
                        self.current_count = len(data.get("检测结果", []))
                        print(f"📂 加载现有数据，已检测 {self.current_count} 个IP")
            except Exception as e:
                print(f"⚠️ 加载现有数据失败: {e}")
    
    def update_statistics(self, ip_info):
        """更新统计信息"""
        if not ip_info:
            self.total_stats["失败检测次数"] += 1
            return
        
        self.total_stats["成功检测次数"] += 1
        
        # IP类型统计
        ip_type = ip_info.get("IP类型", "未知")
        self.total_stats["IP类型统计"][ip_type] = self.total_stats["IP类型统计"].get(ip_type, 0) + 1
        
        # 风控等级统计
        risk_level = ip_info.get("风控等级", "未知")
        self.total_stats["风控等级统计"][risk_level] = self.total_stats["风控等级统计"].get(risk_level, 0) + 1
        
        # 国家分布统计
        location = ip_info.get("IP位置", "未知")
        country = location.split()[0] if location and location != "未知" else "未知"
        self.total_stats["国家分布统计"][country] = self.total_stats["国家分布统计"].get(country, 0) + 1
        
        # ASN分布统计
        asn = ip_info.get("ASN", "未知")
        self.total_stats["ASN分布统计"][asn] = self.total_stats["ASN分布统计"].get(asn, 0) + 1
        
        # 原生IP统计
        native_ip = ip_info.get("原生IP", "未知")
        self.total_stats["原生IP统计"][native_ip] = self.total_stats["原生IP统计"].get(native_ip, 0) + 1
        
        # 计算平均风控值
        risk_value = ip_info.get("风控值", "0%")
        try:
            risk_num = float(risk_value.replace("%", ""))
            current_avg = self.total_stats.get("平均风控值", 0)
            success_count = self.total_stats["成功检测次数"]
            new_avg = ((current_avg * (success_count - 1)) + risk_num) / success_count
            self.total_stats["平均风控值"] = round(new_avg, 2)
        except:
            pass
    
    def save_data(self, ip_info):
        """保存单次检测数据"""
        self.total_stats["总检测次数"] += 1
        self.current_count += 1
        
        if ip_info:
            self.total_stats["检测结果"].append(ip_info)
            self.update_statistics(ip_info)
        
        # 更新检测时间
        self.total_stats["最后检测时间"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 保存到文件
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.total_stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ 保存数据失败: {e}")
    
    def save_final_stats(self):
        """保存最终统计信息"""
        self.total_stats["检测结束时间"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.total_stats, f, ensure_ascii=False, indent=2)
            
            # 同时保存一份统计摘要
            summary_file = f"ip_pool_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            summary = {
                "统计摘要": {
                    "检测时间范围": f"{self.total_stats.get('检测开始时间')} - {self.total_stats.get('检测结束时间')}",
                    "总检测次数": self.total_stats["总检测次数"],
                    "成功率": f"{(self.total_stats['成功检测次数'] / max(self.total_stats['总检测次数'], 1) * 100):.1f}%",
                    "平均风控值": f"{self.total_stats['平均风控值']}%",
                    "IP类型分布": self.total_stats["IP类型统计"],
                    "风控等级分布": self.total_stats["风控等级统计"],
                    "国家分布": self.total_stats["国家分布统计"],
                    "原生IP分布": self.total_stats["原生IP统计"]
                }
            }
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
            
            print(f"📊 统计摘要已保存到: {summary_file}")
            
        except Exception as e:
            print(f"❌ 保存最终统计失败: {e}")
    
    def print_current_stats(self):
        """打印当前统计信息"""
        print("\n" + "="*60)
        print("📊 当前统计信息")
        print("="*60)
        print(f"总检测次数: {self.total_stats['总检测次数']}")
        print(f"成功检测次数: {self.total_stats['成功检测次数']}")
        print(f"失败检测次数: {self.total_stats['失败检测次数']}")
        
        if self.total_stats["成功检测次数"] > 0:
            success_rate = self.total_stats["成功检测次数"] / self.total_stats["总检测次数"] * 100
            print(f"成功率: {success_rate:.1f}%")
            print(f"平均风控值: {self.total_stats['平均风控值']}%")
            
            print("\n🏷️ IP类型分布:")
            for ip_type, count in self.total_stats["IP类型统计"].items():
                percentage = count / self.total_stats["成功检测次数"] * 100
                print(f"  {ip_type}: {count} ({percentage:.1f}%)")
            
            print("\n⚠️ 风控等级分布:")
            for risk_level, count in self.total_stats["风控等级统计"].items():
                percentage = count / self.total_stats["成功检测次数"] * 100
                print(f"  {risk_level}: {count} ({percentage:.1f}%)")
            
            print("\n🌍 国家分布(前5):")
            sorted_countries = sorted(self.total_stats["国家分布统计"].items(), key=lambda x: x[1], reverse=True)[:5]
            for country, count in sorted_countries:
                percentage = count / self.total_stats["成功检测次数"] * 100
                print(f"  {country}: {count} ({percentage:.1f}%)")
        
        print("="*60)
    
    def run(self):
        """运行主程序"""
        print("🚀 动态代理IP池质量统计工具")
        print("="*60)
        print(f"📁 数据文件: {self.data_file}")
        print(f"🎯 最大检测次数: {self.max_checks}")
        print(f"⏰ 检测间隔: {self.delay_between_checks}秒")
        print(f"🌐 代理设置: {self.proxy_url}")
        print(f"🔗 检测模式: {'真实网站' if self.use_real_site else '本地HTML'}")
        print("💡 按 Ctrl+C 可随时停止并保存数据")
        print("="*60)
        
        # 加载现有数据
        self.load_existing_data()
        
        while self.current_count < self.max_checks:
            print(f"\n🔍 开始第 {self.current_count + 1} 次IP检测...")
            
            # 创建检查器实例
            checker = AdvancedPing0CCChecker()
            
            try:
                # 执行检测 - 支持代理和多种模式，传递循环索引
                if self.use_real_site:
                    ip_info = checker.check_ip_advanced(
                        proxy_url=self.proxy_url, 
                        use_real_site=True,
                        loop_index=self.current_count + 1
                    )
                else:
                    ip_info = checker.check_ip_advanced(
                        html_file="ping0.cc.html",
                        proxy_url=self.proxy_url,
                        use_real_site=False,
                        loop_index=self.current_count + 1
                    )
                
                if ip_info:
                    print("✅ 检测成功")
                    print(f"📍 IP地址: {ip_info.get('IP地址', '未知')}")
                    print(f"🌍 位置: {ip_info.get('IP位置', '未知')}")
                    print(f"🏷️ 类型: {ip_info.get('IP类型', '未知')}")
                    print(f"⚠️ 风控: {ip_info.get('风控值', '未知')} ({ip_info.get('风控等级', '未知')})")
                    print(f"🔗 ASN: {ip_info.get('ASN', '未知')}")
                else:
                    print("❌ 检测失败")
                
                # 保存数据
                self.save_data(ip_info)
                
                # 每10次检测显示统计信息
                if (self.current_count) % 10 == 0:
                    self.print_current_stats()
                
            except Exception as e:
                print(f"❌ 检测过程出错: {e}")
                self.save_data(None)
            
            # 如果还没达到最大次数，等待后继续
            if self.current_count < self.max_checks:
                print(f"⏳ 等待 {self.delay_between_checks} 秒后进行下一次检测...")
                time.sleep(self.delay_between_checks)
        
        # 完成所有检测
        print(f"\n🎉 已完成 {self.max_checks} 次检测!")
        self.print_current_stats()
        self.save_final_stats()

def generate_final_table():
    """生成最终表格报告"""
    try:
        print("\n🔄 正在生成表格报告...")
        
        # 导入表格生成模块
        import json
        import csv
        from datetime import datetime
        
        # 加载数据
        try:
            with open('ip_pool_quality.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            print("❌ 无法读取检测数据文件")
            return
        
        # 过滤有效结果
        results = data.get('检测结果', [])
        valid_results = [result for result in results if 'IP地址' in result and result.get('IP地址')]
        
        if not valid_results:
            print("❌ 没有有效的检测结果")
            return
        
        # 生成CSV文件
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_filename = f'IP检测结果_{timestamp}.csv'
        
        with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['循环索引', '序号', '检测时间', 'IP地址', 'IP位置', 'IP类型', '风控值', '风控等级', 
                         '原生IP', 'ASN', 'ASN所有者', '企业', '国家代码']
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for i, result in enumerate(valid_results, 1):
                row = {
                    '循环索引': result.get('循环索引', ''),
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
                writer.writerow(row)
        
        print(f"✅ CSV报告已生成: {csv_filename}")
        print(f"📊 共导出 {len(valid_results)} 条有效记录")
        
        # 显示简要统计
        print(f"\n📈 检测摘要:")
        print(f"  总检测次数: {data.get('总检测次数', 0)}")
        print(f"  成功检测次数: {data.get('成功检测次数', 0)}")
        print(f"  失败检测次数: {data.get('失败检测次数', 0)}")
        success_rate = (data.get('成功检测次数', 0) / max(data.get('总检测次数', 1), 1)) * 100
        print(f"  成功率: {success_rate:.1f}%")
        print(f"  平均风控值: {data.get('平均风控值', 0)}%")
        
    except Exception as e:
        print(f"❌ 生成表格报告失败: {e}")

def main():
    """主函数"""
    print("🚀 动态代理IP池质量统计工具")
    print("="*60)
    print("请选择运行模式:")
    print("1. 快速测试 (5次检测, 间隔5秒, 真实网站)")
    print("2. 标准检测 (50次检测, 间隔5秒, 真实网站)") 
    print("3. 深度分析 (100次检测, 间隔5秒, 真实网站)")
    print("4. 本地测试 (使用ping0.cc.html文件)")
    print("5. 自定义设置")
    
    try:
        choice = input("请输入选择 (1-5): ").strip()
        delay_between_checks = 2
        
        if choice == "1":
            analyzer = IPPoolQualityAnalyzer(max_checks=5, delay_between_checks=delay_between_checks, use_real_site=True)
        elif choice == "2":
            analyzer = IPPoolQualityAnalyzer(max_checks=50, delay_between_checks=delay_between_checks, use_real_site=True)
        elif choice == "3":
            analyzer = IPPoolQualityAnalyzer(max_checks=100, delay_between_checks=delay_between_checks, use_real_site=True)
        elif choice == "4":
            analyzer = IPPoolQualityAnalyzer(max_checks=5, delay_between_checks=delay_between_checks, use_real_site=False)
        elif choice == "5":
            max_checks = int(input("请输入最大检测次数: ").strip())
            delay = int(input("请输入检测间隔(秒): ").strip())
            proxy = input("请输入代理URL (默认: http://127.0.0.1:7890): ").strip() or "http://127.0.0.1:7890"
            use_real = input("使用真实网站? (y/n, 默认y): ").strip().lower() != 'n'
            analyzer = IPPoolQualityAnalyzer(
                max_checks=max_checks, 
                delay_between_checks=delay,
                proxy_url=proxy,
                use_real_site=use_real
            )
        else:
            print("无效选择，使用默认设置 (50次检测, 间隔5秒, 真实网站)")
            analyzer = IPPoolQualityAnalyzer()
        
        analyzer.run()
        
        # 循环结束后自动生成表格
        print("\n" + "="*60)
        print("🎉 检测完成！正在生成报告...")
        generate_final_table()
        
    except KeyboardInterrupt:
        print("\n👋 用户取消操作")
        # 即使被中断也尝试生成表格
        print("🔄 正在保存已检测的数据...")
        try:
            generate_final_table()
        except:
            pass
    except Exception as e:
        print(f"❌ 程序运行出错: {e}")

if __name__ == "__main__":
    main() 