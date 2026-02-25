import requests
import re
import os
from pathlib import Path

# Base URL for raw markdown files
BASE_URL = "https://raw.githubusercontent.com/longportapp/openapi-website/main/docs/zh-CN/docs"

# Target documentation paths to crawl
TARGET_DOCS = [
    # Quote API
    "quote/pull/quote.md",
    "quote/pull/depth.md",
    "quote/pull/brokers.md",
    "quote/pull/candlestick.md",
    
    # Trade API
    "trade/order/submit.md",
    "trade/order/withdraw.md",
    "trade/order/today_orders.md",
    "trade/order/history_orders.md",
    
    # Asset API
    "trade/asset/account.md",
    "trade/asset/stock.md",
    "trade/asset/cashflow.md",
    
    # Auth API
    "api-reference/refresh-token-api.md"
]

def fetch_markdown(path):
    url = f"{BASE_URL}/{path}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {path}: {e}")
        return None

def parse_markdown(content):
    """
    Parse markdown content to extract API details.
    Returns a dictionary with extracted info.
    """
    if not content:
        return None
        
    info = {
        "title": "",
        "description": "",
        "endpoint": "",
        "method": "",
        "parameters": [], # List of dicts
        "response": ""
    }
    
    lines = content.split('\n')
    
    # 1. Extract Title (first H1)
    for line in lines:
        if line.startswith('# '):
            info["title"] = line.replace('# ', '').strip()
            break
            
    # 2. Extract Description (text after title)
    in_frontmatter = False
    for line in lines:
        if line.strip() == '---':
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter:
            continue
        if line.startswith('# '):
            continue
        if line.strip() and not line.startswith('#') and not line.startswith('|') and not line.startswith('`'):
            info["description"] = line.strip()
            break

    # 3. Extract Endpoint and Method
    for i, line in enumerate(lines):
        if "HTTP" in line and ("URL" in line or "Method" in line):
            for j in range(1, 5):
                if i + j >= len(lines): break
                next_line = lines[i+j].strip()
                if next_line.startswith('/'):
                    info["endpoint"] = next_line
                if next_line.upper() in ["GET", "POST", "PUT", "DELETE"]:
                    info["method"] = next_line.upper()
    
    if not info["endpoint"]:
        for line in lines:
            if "/v1/" in line:
                match = re.search(r'(GET|POST|PUT|DELETE)?\s*(/v1/[\w/-]+)', line)
                if match:
                    if match.group(1):
                        info["method"] = match.group(1)
                    info["endpoint"] = match.group(2)
                    break
    
    # 4. Extract Parameters (Look for table)
    # Strategy: Find header row | Name | Type | ...
    params = []
    in_table = False
    header_found = False
    
    for line in lines:
        if '|' in line and '---' in line:
            in_table = True
            continue
        
        if in_table:
            if not line.strip():
                in_table = False
                continue
            
            # Parse row
            # Format usually: | Name | Type | Required | Description |
            cols = [c.strip() for c in line.split('|') if c.strip()]
            if len(cols) >= 3:
                # Basic heuristic
                param = {
                    "name": cols[0],
                    "type": cols[1] if len(cols) > 1 else "",
                    "description": cols[-1] if len(cols) > 2 else ""
                }
                # Filter out header row repeated or other noise
                if param["name"] not in ["Name", "名称", "参数名"]:
                    params.append(param)
    
    info["parameters"] = params
    return info

def generate_api_reference(parsed_docs):
    """
    Generate the content for api_reference.md
    """
    content = "# Longbridge OpenAPI Reference\n\n"
    content += "This document is auto-generated from the official documentation source.\n\n"
    
    categories = {
        "Quote": [],
        "Trade": [],
        "Asset": [],
        "Auth": []
    }
    
    for doc in parsed_docs:
        path = doc['path']
        if 'quote' in path:
            categories['Quote'].append(doc)
        elif 'trade/order' in path:
            categories['Trade'].append(doc)
        elif 'trade/asset' in path:
            categories['Asset'].append(doc)
        elif 'refresh-token' in path:
            categories['Auth'].append(doc)
            
    for cat, docs in categories.items():
        if not docs: continue
        content += f"## {cat} API\n\n"
        for doc in docs:
            info = doc['info']
            if not info: continue
            
            content += f"### {info['title']}\n\n"
            content += f"{info['description']}\n\n"
            if info['endpoint']:
                method = info['method'] or "GET"
                content += f"- **Endpoint**: `{info['endpoint']}` ({method})\n"
            
            if info['parameters']:
                content += "\n**Parameters:**\n\n"
                content += "| Name | Type | Description |\n"
                content += "|------|------|-------------|\n"
                for p in info['parameters']:
                    content += f"| {p['name']} | {p['type']} | {p['description']} |\n"
                content += "\n"
            
            # View URL
            # Note: Path adjustment for view url
            # raw: api-reference/refresh-token-api.md -> view: refresh-token-api
            # raw: quote/pull/quote.md -> view: quote/pull/quote
            view_path = doc['path'].replace('.md', '')
            if 'api-reference/' in view_path:
                 view_path = view_path.replace('api-reference/', '')
                 
            view_url = f"https://open.longbridge.com/zh-CN/docs/{view_path}"
            content += f"- **Reference**: [Official Docs]({view_url})\n\n"

    return content

def main():
    parsed_docs = []
    
    print("Fetching documentation...")
    for path in TARGET_DOCS:
        print(f"Processing {path}...")
        content = fetch_markdown(path)
        if content:
            info = parse_markdown(content)
            parsed_docs.append({
                "path": path,
                "info": info
            })
            
    # Generate API Reference
    print("Generating API Reference...")
    api_ref_content = generate_api_reference(parsed_docs)
    
    # Update api_reference.md
    api_ref_path = Path("../docs/api_reference.md")
    # Resolve relative to script location if needed, but assuming running from scripts dir
    if not api_ref_path.parent.exists():
         # Maybe running from project root?
         api_ref_path = Path("longbrige_tools/docs/api_reference.md")
    
    if api_ref_path.parent.exists():
        with open(api_ref_path, "w", encoding="utf-8") as f:
            f.write(api_ref_content)
        print(f"Updated {api_ref_path}")
    else:
        print(f"Directory not found for: {api_ref_path}")

if __name__ == "__main__":
    main()
