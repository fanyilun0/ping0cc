# -*- coding: utf-8 -*-
"""
配置文件
"""

# 网站URL
PING0CC_URL = "https://ping0.cc"

# 浏览器设置
BROWSER_CONFIG = {
    "headless": False,  # 是否使用无头模式（推荐False以便处理验证码）
    "timeout": 10,      # 等待超时时间（秒）
    "window_size": "1920,1080",  # 窗口大小
}

# 文件保存设置
SAVE_CONFIG = {
    "json_filename": "ip_history.json",  # JSON文件名
    "csv_filename": "ip_history.csv",    # CSV文件名
    "log_filename": "ping0cc_checker.log",  # 日志文件名
}

# 页面元素选择器配置（如果网站结构变化，可以在这里调整）
SELECTORS = {
    "captcha": "//div[contains(@class, 'captcha') or contains(@class, 'verify')]",
    "ip_address": [
        "//div[contains(text(), 'IP 地址')]/following-sibling::div",
        "//span[contains(@class, 'ip')]",
        "//div[contains(@class, 'ip-address')]"
    ]
}

# IP信息字段映射
INFO_FIELDS = {
    "IP位置": ["IP 位置", "位置", "Location"],
    "ASN": ["ASN"],
    "ASN所有者": ["ASN 所有者", "ASN所有者"],
    "企业": ["企业", "Organization"],
    "经度": ["经度", "Longitude"],
    "纬度": ["纬度", "Latitude"],
    "IP类型": ["IP类型", "IP 类型"],
    "风控值": ["风控值", "风险", "Risk"],
    "原生IP": ["原生 IP", "原生IP", "Native"],
    "大模型检测": ["大模型检测", "AI检测"]
} 