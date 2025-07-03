#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级ping0.cc IP信息检查器 - 专门处理反机器人检测
"""

import json
import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

class AdvancedPing0CCChecker:
    """高级ping0.cc检查器 - 专门处理反机器人检测"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        
    def setup_stealth_driver(self, proxy_url="http://127.0.0.1:7890"):
        """设置隐秘浏览器驱动"""
        print("🔧 设置高级反检测浏览器...")
        
        options = Options()
        
        # 基础反检测设置
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # 代理设置
        if proxy_url:
            print(f"🌐 设置代理: {proxy_url}")
            options.add_argument(f"--proxy-server={proxy_url}")
            # 忽略证书错误（对于某些代理很有用）
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--ignore-ssl-errors")
        
        # 窗口和显示设置
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        
        # 更真实的用户代理
        user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        options.add_argument(f"--user-agent={random.choice(user_agents)}")
        
        # 语言设置
        options.add_argument("--lang=zh-CN")
        options.add_experimental_option('prefs', {
            'intl.accept_languages': 'zh-CN,zh,en-US,en'
        })
        
        # 初始化驱动
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 20)
        
        # 执行高级反检测脚本
        stealth_js = """
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
        Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh', 'en']});
        window.chrome = { runtime: {} };
        Object.defineProperty(navigator, 'permissions', {get: () => ({query: () => Promise.resolve({state: 'granted'})})});
        """
        self.driver.execute_script(stealth_js)
        
        print("✅ 浏览器设置完成")
    
    def wait_for_bot_detection_bypass(self):
        """等待绕过机器人检测"""
        print("🤖 检测反机器人机制...")
        
        max_attempts = 2
        for attempt in range(max_attempts):
            page_source = self.driver.page_source
            
            # 检查是否还在bot检测页面
            if "window.x1" in page_source or "window.difficulty" in page_source:
                print(f"🔄 第{attempt + 1}次尝试绕过检测...")
                
                # 等待JavaScript执行
                time.sleep(5 + attempt * 2)
                
                # 尝试简单的页面交互
                try:
                    # 简单点击页面中心
                    self.driver.execute_script("document.body.click();")
                    time.sleep(random.uniform(1, 2))
                except:
                    pass
                
                # 等待更长时间
                time.sleep(8 + attempt * 3)
                
            else:
                print("✅ 成功绕过机器人检测")
                return True
        
        print("⚠️ 可能仍在机器人检测中，继续尝试...")
        return False
    
    def extract_ip_info_advanced(self, loop_index=1):
        """高级IP信息提取 - 基于ping0.cc页面结构优化"""
        print("📊 提取IP信息...")
        
        # 等待页面完全加载
        try:
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        except:
            pass
        
        # 获取页面内容
        page_source = self.driver.page_source
        
        ip_info = {
            "循环索引": loop_index,
            "检测时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "页面标题": self.driver.title,
            "页面URL": self.driver.current_url,
        }
        
        import re
        
        # 从JavaScript变量中提取信息（最准确的方法）
        js_ip_match = re.search(r"window\.ip\s*=\s*['\"]([^'\"]+)['\"]", page_source)
        if js_ip_match:
            ip_info["IP地址"] = js_ip_match.group(1)
        
        js_ipnum_match = re.search(r"window\.ipnum\s*=\s*['\"]([^'\"]+)['\"]", page_source)
        if js_ipnum_match:
            ip_info["IP地址(数字)"] = js_ipnum_match.group(1)
        
        js_longitude_match = re.search(r"window\.longitude\s*=\s*['\"]([^'\"]+)['\"]", page_source)
        if js_longitude_match:
            ip_info["经度"] = js_longitude_match.group(1)
        
        js_latitude_match = re.search(r"window\.latitude\s*=\s*['\"]([^'\"]+)['\"]", page_source)
        if js_latitude_match:
            ip_info["纬度"] = js_latitude_match.group(1)
        
        js_loc_match = re.search(r"window\.loc\s*=\s*`([^`]+)`", page_source)
        if js_loc_match:
            ip_info["IP位置"] = js_loc_match.group(1)
        
        js_asndomain_match = re.search(r"window\.asndomain\s*=\s*['\"]([^'\"]+)['\"]", page_source)
        if js_asndomain_match:
            ip_info["ASN域名"] = js_asndomain_match.group(1)
        
        js_orgdomain_match = re.search(r"window\.orgdomain\s*=\s*['\"]([^'\"]+)['\"]", page_source)
        if js_orgdomain_match:
            ip_info["企业域名"] = js_orgdomain_match.group(1)
        
        # 提取ASN信息
        asn_pattern = r'<a href="[^"]*\/as\/AS(\d+)"[^>]*>AS(\d+)<\/a>'
        asn_match = re.search(asn_pattern, page_source)
        if asn_match:
            ip_info["ASN"] = f"AS{asn_match.group(1)}"
        
        # 提取ASN所有者
        asn_owner_pattern = r'<div class="name">\s*ASN 所有者\s*</div>\s*<div class="content">\s*(?:<span[^>]*>[^<]*</span>\s*)?([^<\n]+?)(?:\s*<span|</div>)'
        asn_owner_match = re.search(asn_owner_pattern, page_source, re.DOTALL)
        if asn_owner_match:
            ip_info["ASN所有者"] = asn_owner_match.group(1).strip()
        
        # 提取企业信息
        org_pattern = r'<div class="name">\s*企业\s*</div>\s*<div class="content">\s*(?:<span[^>]*>[^<]*</span>\s*)?([^<\n]+?)(?:\s*<span|</div>)'
        org_match = re.search(org_pattern, page_source, re.DOTALL)
        if org_match:
            ip_info["企业"] = org_match.group(1).strip()
        
        # 提取IP类型
        iptype_pattern = r'<span class="label[^"]*">([^<]+)</span>'
        iptype_matches = re.findall(iptype_pattern, page_source)
        for iptype in iptype_matches:
            if "IDC" in iptype or "家庭宽带" in iptype:
                ip_info["IP类型"] = iptype.strip()
                break
        
        # 提取风控值
        risk_pattern = r'<span class="value">(\d+%)</span><span class="lab">\s*([^<]+)</span>'
        risk_match = re.search(risk_pattern, page_source)
        if risk_match:
            ip_info["风控值"] = risk_match.group(1)
            ip_info["风控等级"] = risk_match.group(2).strip()
        
        # 提取原生IP信息
        native_ip_pattern = r'<div class="name">\s*<span>原生 IP</span>.*?</div>\s*<div class="content">\s*<span class="label[^"]*"[^>]*>([^<]+)</span>'
        native_ip_match = re.search(native_ip_pattern, page_source, re.DOTALL)
        if native_ip_match:
            ip_info["原生IP"] = native_ip_match.group(1).strip()
        
        # 提取国家旗帜信息
        flag_pattern = r'<img src="/static/images/flags/([^"]+)\.png"[^>]*>([^<]+)'
        flag_matches = re.findall(flag_pattern, page_source)
        if flag_matches:
            ip_info["国家代码"] = flag_matches[0][0]
            # IP位置信息已经通过JS变量获取，这里不覆盖
        
        # 备用提取方法 - 如果JS变量提取失败
        if not ip_info.get("IP地址"):
            ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
            ip_matches = re.findall(ip_pattern, page_source)
            if ip_matches:
                ip_info["IP地址"] = ip_matches[0]
        
        # 如果重要信息缺失，记录调试信息
        missing_fields = []
        required_fields = ["IP地址", "IP位置", "ASN"]
        for field in required_fields:
            if not ip_info.get(field):
                missing_fields.append(field)
        
        if missing_fields:
            print(f"⚠️ 缺失字段: {', '.join(missing_fields)}")
            try:
                visible_text = self.driver.find_element(By.TAG_NAME, "body").text
                ip_info["调试_页面文本"] = visible_text[:500]
            except:
                ip_info["调试_页面源码"] = page_source[:500]
        
        return ip_info
    
    def check_ip_advanced(self, html_file="ping0.cc.html", proxy_url="http://127.0.0.1:7890", use_real_site=False, loop_index=1):
        """高级IP检查流程 - 支持本地HTML文件和在线检测"""
        try:
            if use_real_site:
                # 使用真实网站检测
                print("🌐 使用真实网站进行检测...")
                self.setup_stealth_driver(proxy_url)
                
                # 访问真实的ping0.cc网站
                print("🎯 访问 ping0.cc...")
                self.driver.get("https://ping0.cc")
                
                # 等待页面加载
                time.sleep(random.uniform(5, 8))
                
                # 检查并绕过机器人检测
                self.wait_for_bot_detection_bypass()
                
                # 额外等待确保页面完全加载
                print("⏰ 等待页面完全加载...")
                time.sleep(10)
                
            else:
                # 使用本地HTML文件
                import os
                if not os.path.exists(html_file):
                    print(f"❌ HTML文件不存在: {html_file}")
                    return None
                
                self.setup_stealth_driver(proxy_url)
                
                # 获取HTML文件的绝对路径
                html_path = os.path.abspath(html_file)
                file_url = f"file://{html_path}"
                
                print(f"📂 加载本地HTML文件: {html_file}")
                self.driver.get(file_url)
                
                # 等待页面加载
                time.sleep(random.uniform(2, 4))
            
            # 提取信息
            ip_info = self.extract_ip_info_advanced(loop_index)
            
            return ip_info
            
        except Exception as e:
            print(f"❌ 检查过程中出错: {e}")
            return None
        
        finally:
            if self.driver:
                self.driver.quit()

    def save_results(self, ip_info):
        """保存结果"""
        if not ip_info:
            return
        
        try:
            # 读取现有数据
            try:
                with open('advanced_ip_data.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except:
                data = []
            
            data.append(ip_info)
            
            # 保存数据
            with open('advanced_ip_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print("💾 结果已保存到 advanced_ip_data.json")
            
        except Exception as e:
            print(f"❌ 保存失败: {e}")

def main():
    print("🚀 高级ping0.cc IP检查工具")
    print("=" * 40)
    
    checker = AdvancedPing0CCChecker()
    
    print("开始高级检测流程...")
    ip_info = checker.check_ip_advanced()
    
    if ip_info:
        print("\n📋 检测结果:")
        print("=" * 40)
        for key, value in ip_info.items():
            if value and len(str(value)) < 100:  # 不显示太长的内容
                print(f"{key}: {value}")
        print("=" * 40)
        
        checker.save_results(ip_info)
    else:
        print("❌ 检测失败")

if __name__ == "__main__":
    main() 