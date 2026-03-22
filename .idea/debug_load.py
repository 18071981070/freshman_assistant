import sys
import os

sys.path.insert(0, 'd:/ai大模型RAG与智能体开发_agent项目/.idea')

from utils.config_hander import chroma_conf
from utils.path_tool import get_abs_path
from utils.file_handler import listdir_with_allowed_type

print("chroma_conf:", chroma_conf)
print()

data_path = chroma_conf["data_path"]
print(f"data_path from config: {data_path}")

abs_data_path = get_abs_path(data_path)
print(f"absolute data path: {abs_data_path}")
print(f"path exists: {os.path.exists(abs_data_path)}")

if os.path.exists(abs_data_path):
    print(f"files in directory: {os.listdir(abs_data_path)}")

allowed_types = tuple(chroma_conf["allow_knowledge_file_type"])
print(f"\nallowed types: {allowed_types}")

files = listdir_with_allowed_type(data_path, allowed_types)
print(f"\nfiles found: {files}")
