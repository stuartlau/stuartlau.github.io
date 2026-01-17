#!/usr/bin/env python3
"""
分析HAR文件，提取小红书用户笔记/视频数据
安全声明：所有处理在本地进行，不上传任何数据
"""

import json
import sys
import os
from pathlib import Path

def analyze_har(har_path: str) -> dict:
    """解析HAR文件，提取小红书API数据"""
    
    print(f"📂 读取文件: {har_path}")
    
    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    # 获取所有请求
    entries = har_data.get('log', {}).get('entries', [])
    print(f"📊 总请求数: {len(entries)}")
    
    xhs_requests = []
    note_data = []
    
    for i, entry in enumerate(entries):
        request = entry.get('request', {})
        response = entry.get('response', {})
        url = request.get('url', '')
        
        # 筛选小红书相关API
        if 'xiaohongshu.com' in url or 'xhscdn.com' in url:
            xhs_requests.append({
                'url': url,
                'method': request.get('method', ''),
                'status': response.get('status', 0)
            })
            
            # 尝试提取笔记数据
            try:
                content = response.get('content', {})
                response_body = content.get('text', '')
                
                if response_body and ('note' in url or 'search' in url or 'profile' in url):
                    # 尝试解析JSON响应
                    if response_body.strip().startswith('{'):
                        resp_json = json.loads(response_body)
                        
                        # 提取notes数组
                        if 'data' in resp_json:
                            data = resp_json['data']
                            
                            # 多种可能的数据结构
                            notes = data.get('notes') or data.get('list') or data.get('items') or []
                            if notes:
                                for note in notes:
                                    if isinstance(note, dict):
                                        note_info = extract_note_info(note)
                                        if note_info:
                                            note_data.append(note_info)
                                            print(f"  ✓ 提取笔记: {note_info.get('title', 'Untitled')[:30]}...")
                                            
            except (json.JSONDecodeError, KeyError, TypeError):
                continue
    
    # 统计
    unique_notes = {n['note_id']: n for n in note_data}.values()
    
    result = {
        'total_requests': len(entries),
        'xiaohongshu_requests': len(xhs_requests),
        'notes_found': len(unique_notes),
        'notes': sorted(unique_notes, key=lambda x: x.get('time', ''), reverse=True)
    }
    
    return result

def extract_note_info(note: dict) -> dict:
    """从笔记对象中提取关键信息"""
    
    try:
        # 多种可能的数据结构
        if 'note_id' in note:
            note_id = note.get('note_id')
        elif 'id' in note:
            note_id = note.get('id')
        else:
            return None
        
        if not note_id:
            return None
        
        # 标题
        title = (note.get('title') or 
                note.get('desc') or 
                note.get('content') or 
                note.get('share_desc', '')[:50])
        
        # 图片/封面
        images = note.get('images') or note.get('pics', []) or []
        if images:
            if isinstance(images[0], dict):
                cover = images[0].get('url', images[0].get('web_url', ''))
            else:
                cover = images[0]
        else:
            cover = note.get('cover') or note.get('image', '')
        
        # 时间
        time = (note.get('time') or 
               note.get('create_time') or 
               note.get('date') or '')
        
        # 互动数据
        interact_info = note.get('interact_info', {})
        likes = interact_info.get('liked_count', 0) or note.get('likes', 0)
        comments = interact_info.get('comment_count', 0) or note.get('comments', 0)
        
        return {
            'note_id': str(note_id),
            'title': str(title).strip() if title else '',
            'cover': cover,
            'time': str(time),
            'likes': likes,
            'comments': comments,
            'type': note.get('type', 'normal'),  # video, normal, etc.
        }
        
    except Exception as e:
        print(f"  ⚠️ 解析错误: {e}")
        return None

def save_results(result: dict, output_path: str):
    """保存结果到JSON文件"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 结果已保存: {output_path}")

def print_summary(result: dict):
    """打印摘要"""
    
    print("\n" + "="*50)
    print("📊 分析摘要")
    print("="*50)
    print(f"  总请求数: {result['total_requests']}")
    print(f"  小红书请求: {result['xiaohongshu_requests']}")
    print(f"  提取笔记数: {result['notes_found']}")
    print("="*50)
    
    if result['notes']:
        print("\n📝 最新笔记预览:")
        for note in result['notes'][:5]:
            print(f"  • {note['time']} | ❤️{note['likes']} | {note['title'][:40]}...")
    
    print()

def main():
    """主函数"""
    
    print("\n🔒 小红书HAR分析工具 - 本地运行，安全可控")
    print("="*50)
    
    # 检查参数
    if len(sys.argv) < 2:
        print("❌ 用法: python xhs_har_analyzer.py <har文件路径>")
        print("   示例: python xhs_har_analyzer.py profile.har")
        sys.exit(1)
    
    har_path = sys.argv[1]
    
    # 检查文件存在
    if not os.path.exists(har_path):
        print(f"❌ 文件不存在: {har_path}")
        sys.exit(1)
    
    # 分析
    result = analyze_har(har_path)
    
    # 生成输出文件名
    output_path = har_path.replace('.har', '_notes.json')
    
    # 保存和摘要
    save_results(result, output_path)
    print_summary(result)

if __name__ == '__main__':
    main()
