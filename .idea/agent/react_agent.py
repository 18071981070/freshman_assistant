import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from model.factory import chat_model
except ImportError:
    # 如果直接运行，添加上级目录到Python路径
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from model.factory import chat_model

from langchain.agents import create_agent
from utils.prompt_loader import load_system_prompts
from agent.tools.agent_tools import (rag_summarize, get_campus_weather, get_user_location, get_competition_info, get_graduate_info)
# 暂时注释掉中间件导入，避免导入错误
# 导入中间件
# import sys
# import os

# 添加项目根目录到Python路径
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools'))

# try:
#     from middleware import monitor_tool, log_before_model
# except ImportError:
#     # 如果直接运行，添加上级目录到Python路径
#     sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#     from agent.tools.middleware import monitor_tool, log_before_model


class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            system_prompt=load_system_prompts(),
            tools=[rag_summarize, get_campus_weather, get_user_location, get_competition_info, get_graduate_info],
            # 暂时注释掉中间件，避免导入错误
            # middleware=[monitor_tool, log_before_model],
        )

    def execute_stream(self, query: str):
        input_dict = {
            "messages": [
                {"role": "user", "content": query},
            ]
        }

        for chunk in self.agent.stream(input_dict, stream_mode="values"):
            latest_message = chunk["messages"][-1]
            if latest_message.content:
                yield latest_message.content.strip() + "\n"


if __name__ == '__main__':
    agent = ReactAgent()

    for chunk in agent.execute_stream("给我生成我的使用报告"):
        print(chunk, end="", flush=True)
