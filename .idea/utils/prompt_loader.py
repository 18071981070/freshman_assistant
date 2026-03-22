from utils.config_hander import prompts_conf
from utils.path_tool import get_abs_path
from utils.logger_handler import logger
def load_system_prompt():
    try:
        system_prompt_path = get_abs_path(prompts_conf["main_prompt_path"])
        with open(system_prompt_path, 'r', encoding='utf-8') as f:
            system_prompt = f.read()
        return system_prompt
    except Exception as e:
        logger.error(f"Error loading system prompt: {e}")
        return None
def load_rag_prompts():
    try:
        rag_summarize_prompt_path = get_abs_path(prompts_conf["rag_summarize_prompt_path"])
        with open(rag_summarize_prompt_path, 'r', encoding='utf-8') as f:
            rag_summarize_prompt = f.read()
        return rag_summarize_prompt
    except Exception as e:
        logger.error(f"Error loading rag summarize prompt: {e}")
        return None
def load_report_prompt():
    try:
        report_prompt_path = get_abs_path(prompts_conf["report_prompt_path"])
        with open(report_prompt_path, 'r', encoding='utf-8') as f:
            report_prompt = f.read()
        return report_prompt
    except Exception as e:
        logger.error(f"Error loading report prompt: {e}")
        return None

# 添加与 react_agent.py 中调用匹配的函数
def load_system_prompts():
    return load_system_prompt()

def load_report_prompts():
    return load_report_prompt()

if __name__=="--main__":
    print(load_system_prompt())

