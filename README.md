# 🎓 大一新生智能服务助手

专为大一新生打造的智能问答助手，帮助新生了解保研政策、竞赛信息等校园生活相关内容。

## 功能特点

- 📚 知识库检索：支持PDF、图片等多种文档格式
- 🤖 智能问答：基于RAG技术的智能问答系统
- 🎯 精准回答：针对保研政策、竞赛信息等提供准确答案

## 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export DASHSCOPE_API_KEY="your-api-key"

# 运行应用
streamlit run app.py
```

## 部署到Streamlit Cloud

1. 将代码推送到GitHub仓库
2. 访问 [share.streamlit.io](https://share.streamlit.io)
3. 连接GitHub账号并选择仓库
4. 在Advanced settings中设置Secrets：
   ```
   DASHSCOPE_API_KEY = "your-api-key"
   ```
5. 点击Deploy

## 项目结构

```
├── app.py                 # 主应用入口
├── requirements.txt       # Python依赖
├── .streamlit/
│   ├── config.toml       # Streamlit配置
│   └── secrets.toml.example  # Secrets示例
├── .idea/
│   ├── agent/            # 智能体模块
│   ├── rag/              # RAG检索模块
│   ├── model/            # 模型工厂
│   ├── utils/            # 工具函数
│   ├── config/           # 配置文件
│   ├── data/             # 知识库文档
│   └── prompts/          # 提示词模板
└── README.md
```

## 技术栈

- **前端**: Streamlit
- **LLM**: 通义千问 (DashScope)
- **向量数据库**: Chroma
- **框架**: LangChain
