#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能助手应用
"""

import streamlit as st
import time
import os
import sys

# 添加 .idea 目录到 Python 路径
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.idea'))

from agent.react_agent import ReactAgent
from rag.vector_store import VectorStore
from utils.config_hander import chroma_conf
from utils.path_tool import get_abs_path
from utils.logger_handler import logger
from utils.security_filter import security_filter

# 主应用
if __name__ == "__main__":
    st.set_page_config(
        page_title="智知灵问",
        page_icon="🎓",
        layout="wide"
    )

    # 自定义CSS样式
    st.markdown("""
    <style>
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: 0.15em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.3rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
        letter-spacing: 0.08em;
        padding: 0 20px;
    }
    .feature-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 4px solid #1E88E5;
    }
    .feature-title {
        font-size: 1.1rem;
        font-weight: bold;
        color: #1E88E5;
        margin-bottom: 5px;
    }
    .feature-desc {
        font-size: 0.9rem;
        color: #555;
    }
    .tip-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 15px;
        color: white;
        margin-top: 20px;
    }
    .stChatMessage {
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

    # 初始化向量存储
    @st.cache_resource
    def get_vector_store():
        return VectorStore()

    # 初始化智能代理
    @st.cache_resource
    def get_agent():
        return ReactAgent()

    # 添加标签页
    tab1, tab2 = st.tabs(["💬 智能问答", "📤 知识库上传"])

    # 智能问答标签页
    with tab1:
        st.markdown('<p class="main-header">🎓 智知灵问</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">基于 RAG+ReAct 双引擎的校园新生智能问答智能体</p>', unsafe_allow_html=True)

        # 初始化会话状态
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # 头像文件路径
        user_avatar = "user_avatar.jpg"
        bot_avatar = "bot_avatar.jpg"

        # 显示聊天历史
        for message in st.session_state.messages:
            if message["role"] == "user" and os.path.exists(user_avatar):
                with st.chat_message(message["role"], avatar=user_avatar):
                    st.markdown(message["content"])
            elif message["role"] == "assistant" and os.path.exists(bot_avatar):
                with st.chat_message(message["role"], avatar=bot_avatar):
                    st.markdown(message["content"])
            else:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # 输入框
        if prompt := st.chat_input("请输入你的问题，我会尽力帮你解答！"):
            # 安全检查
            if security_filter.contains_sensitive_content(prompt):
                st.session_state.messages.append({"role": "user", "content": prompt})
                if os.path.exists(user_avatar):
                    with st.chat_message("user", avatar=user_avatar):
                        st.markdown(prompt)
                else:
                    with st.chat_message("user"):
                        st.markdown(prompt)

                if os.path.exists(bot_avatar):
                    avatar_arg = bot_avatar
                else:
                    avatar_arg = None

                with st.chat_message("assistant", avatar=avatar_arg):
                    st.error("抱歉，您的问题包含敏感内容，我无法回答。")

                st.session_state.messages.append({"role": "assistant", "content": "抱歉，您的问题包含敏感内容，我无法回答。"})
            else:
                # 添加用户消息
                st.session_state.messages.append({"role": "user", "content": prompt})
                if os.path.exists(user_avatar):
                    with st.chat_message("user", avatar=user_avatar):
                        st.markdown(prompt)
                else:
                    with st.chat_message("user"):
                        st.markdown(prompt)

                # 显示助手消息
                if os.path.exists(bot_avatar):
                    avatar_arg = bot_avatar
                else:
                    avatar_arg = None

                with st.chat_message("assistant", avatar=avatar_arg):
                    message_placeholder = st.empty()
                    full_response = ""

                    # 初始化智能代理
                    agent = get_agent()

                    # 获取回答
                    try:
                        for chunk in agent.execute_stream(prompt):
                            full_response += chunk
                            message_placeholder.markdown(full_response + "▌")
                        message_placeholder.markdown(full_response)
                    except Exception as e:
                        error_msg = f"抱歉，我遇到了一些问题：{str(e)}"
                        message_placeholder.error(error_msg)
                        full_response = error_msg

                # 添加助手消息
                st.session_state.messages.append({"role": "assistant", "content": full_response})

        # 侧边栏
        with st.sidebar:
            st.header("📚 功能介绍")
            st.markdown("""
            <div class="feature-card">
                <div class="feature-title">1️⃣ 入学必备信息查询</div>
                <div class="feature-desc">
                    报到流程、军训安排、宿舍须知、校园卡、医保、户籍、档案、助学贷款、校园地图、快递点、食堂、超市、医务室位置及常用电话
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="feature-card">
                <div class="feature-title">2️⃣ 学业信息差破解</div>
                <div class="feature-desc">
                    专业培养方案、必修/选修课清单、绩点计算规则、保研/评奖要求、挂科/重修/缓考/转专业政策、四六级/计算机二级/普通话等考证信息、选课技巧、水课/硬课口碑、期末复习资料及往年试卷
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="feature-card">
                <div class="feature-title">3️⃣ 竞赛&科研入门</div>
                <div class="feature-desc">
                    校/省/国家级竞赛（大英赛、数学建模、挑战杯、蓝桥杯等）清单、报名时间、组队方式、备赛资料，大创项目、科研助理、实验室入门渠道，论文/专利/软著基础科普
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="feature-card">
                <div class="feature-title">4️⃣ 校园生活服务</div>
                <div class="feature-desc">
                    校园网、图书馆、体育馆使用规则，社团招新、学生会、志愿时长，兼职/家教/校内勤工助学，心理辅导、奖学金/助学金/困难补助
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="feature-card">
                <div class="feature-title">5️⃣ 升学/就业前置规划</div>
                <div class="feature-desc">
                    保研流程、夏令营、推免条件，考研常识、院校选择，考公/选调/国企/大厂求职入门，留学语言、申请时间线
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="feature-card">
                <div class="feature-title">6️⃣ 问答&智能咨询</div>
                <div class="feature-desc">
                    自然语言提问响应（如"怎么转专业？""奖学金怎么拿？"）、常见问题自动匹配答案、匿名提问/互助
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="feature-card">
                <div class="feature-title">7️⃣ 时间线提醒</div>
                <div class="feature-desc">
                    选课时间、四六级报名/考试、竞赛报名截止、奖学金申请、期末复习周、寒暑假安排等关键节点提醒
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.divider()

            # 重新加载知识库按钮
            if st.button("🔄 重新加载知识库", use_container_width=True):
                with st.spinner("正在重新加载知识库..."):
                    try:
                        vector_store = get_vector_store()
                        vector_store.load_documents()
                        st.success("✅ 知识库重新加载成功")
                    except Exception as e:
                        st.error(f"❌ 知识库重新加载失败: {str(e)}")

            st.divider()
            st.markdown("---")
            st.markdown("🎓 智知灵问 v1.0")

    # 知识库上传标签页
    with tab2:
        st.header("📤 知识库上传")
        st.markdown("### 上传文件到知识库")
        
        # 导入并运行知识库上传功能
        import knowledge_upload
        knowledge_upload.main()
