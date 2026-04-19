import sys
import os

sys.path.insert(0, 'd:/ai大模型RAG与智能体开发_agent项目/.idea')

from utils.path_tool import get_abs_path

data_path = get_abs_path('data')
print(f"data_path: {data_path}")

allowed_extensions = ('txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp')
print(f"allowed_extensions: {allowed_extensions}")

# 手动测试
normalized_extensions = tuple(
    ext if ext.startswith('.') else '.' + ext
    for ext in allowed_extensions
)
print(f"normalized_extensions: {normalized_extensions}")

for root, _, files in os.walk(data_path):
    for file in files:
        print(f"\n检查文件: {file}")
        print(f"  lower: {file.lower()}")
        print(f"  endswith test: {file.lower().endswith(normalized_extensions)}")
        for ext in normalized_extensions:
            if file.lower().endswith(ext):
                print(f"  匹配到: {ext}")
