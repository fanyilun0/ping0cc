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
        
    def setup_stealth_driver(self):
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
    
    def human_like_delay(self, min_sec=1, max_sec=3):
        """人类般的随机延迟"""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)
    
    def simulate_human_behavior(self):
        """模拟人类行为"""
        print("👤 模拟人类浏览行为...")
        
        try:
            # 简化的鼠标移动 - 只使用JavaScript
            print("  模拟鼠标移动...")
            self.driver.execute_script("""
                // 简单的鼠标事件模拟
                var event = new MouseEvent('mousemove', {
                    'view': window,
                    'bubbles': true,
                    'cancelable': true,
                    'clientX': 300,
                    'clientY': 200
                });
                document.dispatchEvent(event);
            """)
            self.human_like_delay(0.5, 1.0)
            
        except Exception as e:
            print(f"⚠️ 鼠标模拟跳过: {e}")
        
        # 安全的页面滚动
        try:
            scroll_positions = [200, 400, 300, 100, 0]
            for position in scroll_positions:
                self.driver.execute_script(f"window.scrollTo(0, {position});")
                self.human_like_delay(0.8, 1.5)
        except Exception as e:
            print(f"⚠️ 滚动操作跳过: {e}")
    
    def wait_for_bot_detection_bypass(self):
        """等待绕过机器人检测"""
        print("🤖 检测反机器人机制...")
        
        max_attempts = 5
        for attempt in range(max_attempts):
            page_source = self.driver.page_source
            
            # 检查是否还在bot检测页面
            if "window.x1" in page_source or "window.difficulty" in page_source:
                print(f"🔄 第{attempt + 1}次尝试绕过检测...")
                
                # 等待JavaScript执行
                time.sleep(5 + attempt * 2)
                
                # 模拟人类行为
                self.simulate_human_behavior()
                
                # 尝试简单的页面交互
                try:
                    # 简单点击页面中心
                    self.driver.execute_script("document.body.click();")
                    self.human_like_delay(1, 2)
                except:
                    pass
                
                # 等待更长时间
                time.sleep(8 + attempt * 3)
                
            else:
                print("✅ 成功绕过机器人检测")
                return True
        
        print("⚠️ 可能仍在机器人检测中，继续尝试...")
        return False
    
    def extract_ip_info_advanced(self):
        """高级IP信息提取"""
        print("📊 提取IP信息...")
        
        # 等待页面完全加载
        try:
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        except:
            pass
        
        # 获取页面内容
        page_text = self.driver.page_source
        
        ip_info = {
            "检测时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "页面标题": self.driver.title,
            "页面URL": self.driver.current_url
        }
        
        # 使用多种方法提取IP信息
        import re
        
        # 提取IP地址
        ip_patterns = [
            r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
            r'IP[^0-9]*([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})',
            r'地址[^0-9]*([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})'
        ]
        
        for pattern in ip_patterns:
            matches = re.findall(pattern, page_text)
            if matches:
                ip_info["IP地址"] = matches[0] if isinstance(matches[0], str) else matches[0]
                break
        
        # 提取位置信息
        location_patterns = [
            r'(日本|美国|香港|新加坡|台湾|韩国|中国)[^a-zA-Z]*([^\s<>]{0,20})',
            r'位置[^>]*>([^<]+)',
            r'Location[^>]*>([^<]+)'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, page_text)
            if match:
                ip_info["IP位置"] = match.group(0)
                break
        
        # 提取风险信息
        risk_patterns = [
            r'(\d+%)[^a-zA-Z]*(?:风险|危险|安全)',
            r'风控[^0-9]*(\d+%)',
            r'Risk[^0-9]*(\d+%)'
        ]
        
        for pattern in risk_patterns:
            match = re.search(pattern, page_text)
            if match:
                ip_info["风控值"] = match.group(1)
                break
        
        # 提取ASN信息
        asn_match = re.search(r'AS(\d+)', page_text)
        if asn_match:
            ip_info["ASN"] = f"AS{asn_match.group(1)}"
        
        # 如果关键信息都没有获取到，保存页面内容用于调试
        if not ip_info.get("IP地址"):
            # 获取页面的可见文本
            try:
                visible_text = self.driver.find_element(By.TAG_NAME, "body").text
                ip_info["页面文本"] = visible_text[:1000]  # 保存前1000字符
            except:
                ip_info["页面源码"] = page_text[:1000]
        
        return ip_info
    
    def check_ip_advanced(self):
        """高级IP检查流程"""
        try:
            self.setup_stealth_driver()
            
            # 预热浏览器 - 访问常见网站
            print("🌍 预热浏览器...")
            warm_up_sites = ["https://www.baidu.com", "https://www.google.com"]
            
            for site in warm_up_sites:
                try:
                    self.driver.get(site)
                    self.human_like_delay(2, 4)
                except:
                    continue
            
            # 访问目标网站
            print("🎯 访问 ping0.cc...")
            self.driver.get("https://ping0.cc")
            
            # 等待初始加载
            self.human_like_delay(5, 8)
            
            # 检查并绕过机器人检测
            self.wait_for_bot_detection_bypass()
            
            # 额外等待确保页面完全加载
            print("⏰ 等待页面完全加载...")
            time.sleep(10)
            
            # 最后一次模拟人类行为
            self.simulate_human_behavior()
            
            # 提取信息
            ip_info = self.extract_ip_info_advanced()
            
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