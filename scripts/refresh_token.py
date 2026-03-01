#!/usr/bin/env python3
"""
Longbridge Token 刷新脚本

功能：
- 使用 refresh_access_token 刷新 access token
- 自动更新 .env 文件中的 LONGPORT_ACCESS_TOKEN
- 支持手动刷新和自动刷新（token 过期时调用）

用法：
    python scripts/refresh_token.py           # 刷新 token，默认 90 天有效
    python scripts/refresh_token.py --days 30 # 刷新 token，指定 30 天有效
    python scripts/refresh_token.py --check   # 检查当前 token 状态
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime, timezone
import re

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from dotenv import load_dotenv


def load_env_file(env_path: Path) -> dict:
    """加载 .env 文件内容"""
    env_vars = {}
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    return env_vars


def save_env_file(env_path: Path, env_vars: dict):
    """保存 .env 文件"""
    with open(env_path, 'w') as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")


def decode_jwt_payload(token: str) -> dict:
    """简单解码 JWT token 获取 payload 信息（不验证签名）"""
    try:
        import base64
        import json
        
        # JWT 格式: header.payload.signature
        parts = token.split('.')
        if len(parts) != 3:
            return {}
        
        # 解码 payload (第二部分)
        payload = parts[1]
        # 补齐 base64 padding
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += '=' * padding
        
        decoded = base64.urlsafe_b64decode(payload)
        return json.loads(decoded)
    except Exception:
        return {}


def check_token_status(token: str) -> dict:
    """检查 token 状态"""
    payload = decode_jwt_payload(token)
    
    if not payload:
        return {"valid": False, "error": "无法解析 token"}
    
    exp = payload.get('exp')
    iat = payload.get('iat')
    
    if exp:
        exp_dt = datetime.fromtimestamp(exp, tz=timezone.utc)
        now = datetime.now(timezone.utc)
        remaining = exp_dt - now
        
        return {
            "valid": True,
            "exp": exp_dt,
            "iat": datetime.fromtimestamp(iat, tz=timezone.utc) if iat else None,
            "remaining_days": remaining.days,
            "remaining_hours": remaining.seconds // 3600,
            "is_expired": remaining.total_seconds() < 0,
            "ak": payload.get('ak'),  # app key
            "mid": payload.get('mid'),  # member id
        }
    
    return {"valid": False, "error": "token 中没有过期时间"}


def refresh_token(days: int = 90) -> str:
    """刷新 access token"""
    from longport.openapi import Config
    
    # 加载环境变量
    load_dotenv()
    
    # 创建配置
    config = Config.from_env()
    
    print(f"正在刷新 access token (有效期: {days} 天)...")
    
    # 刷新 token
    new_token = config.refresh_access_token(expired_at=days)
    
    print("✅ Token 刷新成功!")
    return new_token


def main():
    parser = argparse.ArgumentParser(
        description="Longbridge Token 刷新工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python scripts/refresh_token.py           # 刷新 token，默认 90 天有效
    python scripts/refresh_token.py --days 30 # 刷新 token，指定 30 天有效
    python scripts/refresh_token.py --check   # 检查当前 token 状态
        """
    )
    parser.add_argument('--days', type=int, default=90,
                        help='Token 有效天数 (默认: 90)')
    parser.add_argument('--check', action='store_true',
                        help='仅检查当前 token 状态，不刷新')
    
    args = parser.parse_args()
    
    # 环境变量文件路径
    env_path = project_root / ".env"
    
    # 加载当前 token
    load_dotenv(env_path)
    current_token = os.getenv('LONGPORT_ACCESS_TOKEN', '')
    
    if not current_token:
        print("❌ 错误: .env 中没有找到 LONGPORT_ACCESS_TOKEN")
        sys.exit(1)
    
    # 检查模式
    if args.check:
        print("检查当前 token 状态...")
        print("-" * 50)
        
        status = check_token_status(current_token)
        
        if not status.get('valid'):
            print(f"❌ Token 无效: {status.get('error')}")
            sys.exit(1)
        
        print(f"App Key:    {status.get('ak', 'N/A')}")
        print(f"Member ID:  {status.get('mid', 'N/A')}")
        print(f"签发时间:   {status.get('iat').strftime('%Y-%m-%d %H:%M:%S UTC') if status.get('iat') else 'N/A'}")
        print(f"过期时间:   {status.get('exp').strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"剩余时间:   {status.get('remaining_days')} 天 {status.get('remaining_hours')} 小时")
        
        if status.get('is_expired'):
            print("\n⚠️  Token 已过期，请立即刷新!")
        elif status.get('remaining_days') < 7:
            print(f"\n⚠️  Token 即将过期，建议尽快刷新!")
        else:
            print("\n✅ Token 状态正常")
        
        sys.exit(0)
    
    # 刷新模式
    try:
        new_token = refresh_token(args.days)
        
        # 更新 .env 文件
        env_vars = load_env_file(env_path)
        env_vars['LONGPORT_ACCESS_TOKEN'] = new_token
        save_env_file(env_path, env_vars)
        
        print(f"✅ .env 文件已更新")
        
        # 显示新 token 状态
        status = check_token_status(new_token)
        if status.get('valid'):
            print(f"新过期时间: {status.get('exp').strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
    except Exception as e:
        print(f"❌ 刷新失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()