import streamlit as st
import os

st.set_page_config(
    page_title="测试应用",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 测试应用")

# 显示用户头像
user_avatar = "user_avatar.png"
if os.path.exists(user_avatar):
    st.image(user_avatar, width=100, caption="你")
else:
    st.write("头像文件不存在")

st.write("应用运行正常！")
