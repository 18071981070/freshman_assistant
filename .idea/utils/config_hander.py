"""
配置文件加载模块
"""
import yaml
import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from path_tool import get_abs_path

def load_config(config_name: str, config_file: str = None) -> dict:
    if not config_file:
        config_file = get_abs_path(f'config/{config_name}')
    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.load(f, Loader=yaml.FullLoader) or {}

rag_conf = load_config('rag.yml')
chroma_conf = load_config('chroma.yml')
prompts_conf = load_config('prompts.yml')
agent_conf = load_config('agent.yml')

if __name__ == "__main__":
    print(agent_conf.get("chat_model_name", "未配置"))
