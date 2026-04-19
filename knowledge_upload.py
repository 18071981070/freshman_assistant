import streamlit as st
import os
import sys
import time

# 添加 .idea 目录到 Python 路径
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.idea'))

from rag.vector_store import VectorStore
from utils.config_hander import chroma_conf
from utils.path_tool import get_abs_path
from utils.logger_handler import logger
from PIL import Image

<<<<<<< HEAD
def main():
    # 自定义CSS样式
    st.markdown("""
    <style>
    .upload-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: 0.1em;
    }
    .upload-subheader {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    .file-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 12px;
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    .file-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .file-info {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .file-name {
        font-weight: 600;
        color: #333;
        font-size: 1rem;
    }
    .file-size {
        color: #666;
        font-size: 0.9rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1E88E5;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e9ecef;
    }
    .upload-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 30px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    .stats-number {
        font-size: 2.5rem;
        font-weight: bold;
    }
    .stats-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .doc-icon {
        font-size: 1.5rem;
        margin-right: 10px;
    }
    .tip-box {
        background: linear-gradient(135deg, #00d4aa 0%, #7c3aed 100%);
        border-radius: 12px;
        padding: 15px;
        color: white;
        margin: 15px 0;
    }
    .warning-box {
        background: linear-gradient(135deg, #ffa726 0%, #ff7043 100%);
        border-radius: 12px;
        padding: 15px;
        color: white;
        margin: 15px 0;
    }
    .success-box {
        background: linear-gradient(135deg, #66bb6a 0%, #43a047 100%);
        border-radius: 12px;
        padding: 15px;
        color: white;
        margin: 15px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="upload-header">📤 知识库上传</p>', unsafe_allow_html=True)
    st.markdown('<p class="upload-subheader">上传文件到知识库，让智能助手更聪明</p>', unsafe_allow_html=True)

    # 初始化向量存储
    @st.cache_resource
    def get_vector_store():
        return VectorStore()

    vector_store = get_vector_store()

    # 获取数据目录
    data_dir = get_abs_path(chroma_conf["data_path"])

    # 初始化删除状态
    if "delete_confirm" not in st.session_state:
        st.session_state["delete_confirm"] = None
    if "delete_file" not in st.session_state:
        st.session_state["delete_file"] = None
    if "selected_files" not in st.session_state:
        st.session_state["selected_files"] = []

    # 处理删除确认
    if st.session_state.get("delete_confirm") and st.session_state.get("delete_file"):
        file_to_delete = st.session_state["delete_file"]
        try:
            if os.path.exists(file_to_delete):
                os.remove(file_to_delete)
                st.success(f"✅ 文件 {os.path.basename(file_to_delete)} 已从文件系统中删除")
                vector_store.load_documents()
            else:
                st.error(f"❌ 文件 {os.path.basename(file_to_delete)} 不存在")
        except Exception as e:
            st.error(f"❌ 删除文件 {os.path.basename(file_to_delete)} 失败: {str(e)}")
        finally:
            st.session_state["delete_confirm"] = None
            st.session_state["delete_file"] = None
        time.sleep(1)
        st.rerun()

    # 显示当前知识库中的文件
    st.markdown('<p class="section-header">📁 当前知识库文件</p>', unsafe_allow_html=True)
    st.markdown('<div class="tip-box">📂 知识库数据目录: <code>./data</code></div>', unsafe_allow_html=True)

    # 获取知识库中已有的文件
    if os.path.exists(data_dir):
        existing_files = [f for f in os.listdir(data_dir) if f.endswith(tuple(chroma_conf["allow_knowledge_file_type"]))]
        if existing_files:
            # 分离图片文件和文本文件
            image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
            image_files = [f for f in existing_files if f.endswith(image_extensions)]
            text_files = [f for f in existing_files if not f.endswith(image_extensions)]
            
            # 显示统计信息
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f'''
                <div class="stats-card">
                    <div class="stats-number">{len(text_files)}</div>
                    <div class="stats-label">📄 文档文件</div>
                </div>
                ''', unsafe_allow_html=True)
            with col2:
                st.markdown(f'''
                <div class="stats-card">
                    <div class="stats-number">{len(image_files)}</div>
                    <div class="stats-label">🖼️ 图片文件</div>
                </div>
                ''', unsafe_allow_html=True)
            with col3:
                total_size = sum(os.path.getsize(os.path.join(data_dir, f)) for f in existing_files) / 1024
                st.markdown(f'''
                <div class="stats-card">
                    <div class="stats-number">{total_size:.1f}</div>
                    <div class="stats-label">📦 总大小(KB)</div>
                </div>
                ''', unsafe_allow_html=True)
            
            st.markdown("---")
            
            if text_files:
                for i, file in enumerate(text_files, 1):
                    file_path = os.path.join(data_dir, file)
                    file_size = os.path.getsize(file_path) / 1024  # KB
                    file_ext = os.path.splitext(file)[1].upper().replace('.', '')
                    
                    # 根据文件类型选择图标
                    if file_ext in ['PDF']:
                        icon = "📕"
                    elif file_ext in ['DOC', 'DOCX']:
                        icon = "📘"
                    else:
                        icon = "📄"
                    
                    st.markdown(f'''
                    <div class="file-card">
                        <div class="file-info">
                            <div>
                                <span class="doc-icon">{icon}</span>
                                <span class="file-name">{i}. {file}</span>
                            </div>
                            <div>
                                <span class="file-size">{file_ext} · {file_size:.2f} KB</span>
                            </div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col3:
                        if st.button(f"🗑️ 删除", key=f"delete_text_{i}_{file}", type="secondary"):
                            st.session_state["delete_confirm"] = True
                            st.session_state["delete_file"] = file_path
            
            if image_files:
                st.markdown("---")
                st.markdown("### 🖼️ 图片文件预览")
                
                cols = st.columns(4)
                for i, file in enumerate(image_files):
                    file_path = os.path.join(data_dir, file)
                    file_size = os.path.getsize(file_path) / 1024  # KB
                    
                    with cols[i % 4]:
                        try:
                            img = Image.open(file_path)
                            st.image(img, caption=f"{file}\n({file_size:.2f} KB)", use_column_width=True)
                        except Exception as e:
                            st.error(f"无法预览 {file}: {str(e)}")
                        
                        if st.button(f"🗑️ 删除", key=f"delete_image_{i}_{file}", type="secondary"):
                            st.session_state["delete_confirm"] = True
                            st.session_state["delete_file"] = file_path
        else:
            st.markdown('<div class="warning-box">⚠️ 知识库中还没有文件</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="warning-box">⚠️ 知识库数据目录不存在</div>', unsafe_allow_html=True)

    st.divider()

    # 文件上传区域
    st.markdown('<p class="section-header">📤 上传新文件</p>', unsafe_allow_html=True)
    st.markdown('<div class="tip-box">📋 支持的文件格式: PDF, TXT, DOC, DOCX, PNG, JPG, JPEG, GIF, BMP, WEBP</div>', unsafe_allow_html=True)

    # 文件上传
    uploaded_files = st.file_uploader(
        "选择要上传的文件",
        type=chroma_conf["allow_knowledge_file_type"],
        accept_multiple_files=True,
        help="请选择PDF、TXT、DOC、DOCX或图片格式的文件"
    )

    if uploaded_files:
        # 分离图片文件和文本文件
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
        image_files = [f for f in uploaded_files if f.name.endswith(image_extensions)]
        text_files = [f for f in uploaded_files if not f.name.endswith(image_extensions)]
        
        if text_files:
            st.markdown(f"### 📄 已选择 {len(text_files)} 个文档文件:")
            for i, uploaded_file in enumerate(text_files, 1):
                file_ext = os.path.splitext(uploaded_file.name)[1].upper().replace('.', '')
                
                # 根据文件类型选择图标
                if file_ext in ['PDF']:
                    icon = "📕"
                elif file_ext in ['DOC', 'DOCX']:
                    icon = "📘"
                else:
                    icon = "📄"
                
                st.markdown(f'''
                <div class="file-card">
                    <div class="file-info">
                        <div>
                            <span class="doc-icon">{icon}</span>
                            <span class="file-name">{i}. {uploaded_file.name}</span>
                        </div>
                        <div>
                            <span class="file-size">{file_ext} · {uploaded_file.size / 1024:.2f} KB</span>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        if image_files:
            st.markdown(f"### 🖼️ 已选择 {len(image_files)} 个图片文件:")
            
            # 创建图片预览网格
            cols = st.columns(4)  # 每行显示4张图片
            for i, uploaded_file in enumerate(image_files):
                with cols[i % 4]:
                    try:
                        img = Image.open(uploaded_file)
                        st.image(img, caption=f"{uploaded_file.name}\n({uploaded_file.size / 1024:.2f} KB)", use_column_width=True)
                    except Exception as e:
                        st.error(f"无法预览 {uploaded_file.name}: {str(e)}")

        # 上传按钮
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 开始上传", type="primary", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                success_count = 0
                error_count = 0
                skip_count = 0
                
                for i, uploaded_file in enumerate(uploaded_files):
                    try:
                        # 保存文件到数据目录
                        file_path = os.path.join(data_dir, uploaded_file.name)
                        
                        # 检查文件是否已存在
                        if os.path.exists(file_path):
                            status_text.warning(f"⚠️ 文件 {uploaded_file.name} 已存在，跳过")
                            skip_count += 1
                            progress_bar.progress((i + 1) / len(uploaded_files))
                            continue
                        
                        # 保存文件
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        status_text.info(f"📄 正在处理文件: {uploaded_file.name}")
                        
                        # 获取文件的MD5
                        md5_hex = vector_store._get_file_md5(file_path)
                        
                        # 检查MD5是否已存在
                        if vector_store._is_file_processed(md5_hex):
                            status_text.warning(f"⚠️ 文件 {uploaded_file.name} 内容已存在于知识库中，跳过")
                            skip_count += 1
                            progress_bar.progress((i + 1) / len(uploaded_files))
                            continue
                        
                        # 加载文档
                        documents = vector_store._load_file(file_path)
                        
                        if not documents:
                            status_text.warning(f"⚠️ 文件 {uploaded_file.name} 内没有有效文本内容，跳过")
                            skip_count += 1
                            progress_bar.progress((i + 1) / len(uploaded_files))
                            continue
                        
                        # 对于图片文件，不需要分割，直接存入向量库
                        if uploaded_file.name.endswith(image_extensions):
                            # 将图片内容存入向量库
                            vector_store.vector_store.add_documents(documents)
                            # 保存MD5值
                            vector_store._save_md5(md5_hex)
                            status_text.success(f"✅ 图片 {uploaded_file.name} 已成功上传到知识库")
                            success_count += 1
                        else:
                            # 对于文本文件，需要分割
                            split_document = vector_store.text_splitter.split_documents(documents)
                            
                            if not split_document:
                                status_text.warning(f"⚠️ 文件 {uploaded_file.name} 分片后没有有效文本内容，跳过")
                                skip_count += 1
                                progress_bar.progress((i + 1) / len(uploaded_files))
                                continue
                            
                            # 将内容存入向量库
                            vector_store.vector_store.add_documents(split_document)
                            
                            # 保存MD5值
                            vector_store._save_md5(md5_hex)
                            
                            status_text.success(f"✅ 文件 {uploaded_file.name} 已成功上传到知识库")
                            success_count += 1
                        
                    except Exception as e:
                        status_text.error(f"❌ 文件 {uploaded_file.name} 上传失败: {str(e)}")
                        error_count += 1
                    
                    progress_bar.progress((i + 1) / len(uploaded_files))
                
                # 显示上传结果
                st.divider()
                st.header("📊 上传结果")
                if success_count > 0:
                    st.success(f"✅ 成功上传 {success_count} 个文件")
                if error_count > 0:
                    st.error(f"❌ 失败 {error_count} 个文件")
                if skip_count > 0:
                    st.info(f"⚠️ 跳过 {skip_count} 个文件（已存在或内容为空）")
                
                # 刷新页面
                time.sleep(2)
                st.rerun()

    st.divider()

    # 复制文件区域
    st.markdown('<p class="section-header">📋 复制本地文件到知识库</p>', unsafe_allow_html=True)
    st.markdown('<div class="tip-box">💡 从本地文件系统选择文件，复制到知识库数据目录</div>', unsafe_allow_html=True)

    # 文件路径输入
    file_paths = st.text_area(
        "📝 输入文件路径（每行一个文件路径）",
        placeholder="C:\\Users\\用户名\\Documents\\file1.pdf\nC:\\Users\\用户名\\Documents\\file2.txt\nC:\\Users\\用户名\\Pictures\\image.png",
        help="请输入完整的文件路径，每行一个文件，支持文本文件和图片文件"
    )

    # 或者使用文件上传器
    st.markdown("**或者直接上传文件:**")
    local_files = st.file_uploader(
        "选择要复制到知识库的文件",
        type=chroma_conf["allow_knowledge_file_type"],
        accept_multiple_files=True,
        help="请选择PDF、TXT、DOC、DOCX或图片格式的文件"
    )

    if local_files:
        st.session_state["selected_files"] = [file.name for file in local_files]
        st.markdown(f'<div class="success-box">✅ 已选择 {len(local_files)} 个文件</div>', unsafe_allow_html=True)
        
        # 分离图片文件和文本文件
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
        selected_image_files = [f for f in local_files if f.name.endswith(image_extensions)]
        selected_text_files = [f for f in local_files if not f.name.endswith(image_extensions)]
        
        if selected_text_files:
            st.markdown(f"### 📄 已选择 {len(selected_text_files)} 个文档文件:")
            for i, file in enumerate(selected_text_files, 1):
                st.markdown(f'''
                <div class="file-card">
                    <div class="file-info">
                        <div>
                            <span class="doc-icon">📄</span>
                            <span class="file-name">{i}. {file.name}</span>
                        </div>
                        <div>
                            <span class="file-size">{file.size / 1024:.2f} KB</span>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        if selected_image_files:
            st.markdown(f"### 🖼️ 已选择 {len(selected_image_files)} 个图片文件:")
            cols = st.columns(4)
            for i, file in enumerate(selected_image_files):
                with cols[i % 4]:
                    st.markdown(f'''
                    <div class="file-card">
                        <div class="file-info">
                            <div>
                                <span class="doc-icon">🖼️</span>
                                <span class="file-name">{i}. {file.name}</span>
                            </div>
                            <div>
                                <span class="file-size">{file.size / 1024:.2f} KB</span>
                            </div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)

    # 显示已选择的文件
    if "selected_files" in st.session_state and st.session_state["selected_files"]:
        st.markdown("---")
        
        # 分离图片文件和文本文件
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
        selected_image_files = [f for f in st.session_state["selected_files"] if f.endswith(image_extensions)]
        selected_text_files = [f for f in st.session_state["selected_files"] if not f.endswith(image_extensions)]
        
        if selected_text_files:
            st.markdown(f"### 📄 已选择 {len(selected_text_files)} 个文档文件:")
            for i, file_path in enumerate(selected_text_files, 1):
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path) / 1024  # KB
                    file_ext = os.path.splitext(file_path)[1].upper().replace('.', '')
                    
                    # 根据文件类型选择图标
                    if file_ext in ['PDF']:
                        icon = "📕"
                    elif file_ext in ['DOC', 'DOCX']:
                        icon = "📘"
                    else:
                        icon = "📄"
                    
                    st.markdown(f'''
                    <div class="file-card">
                        <div class="file-info">
                            <div>
                                <span class="doc-icon">{icon}</span>
                                <span class="file-name">{i}. {os.path.basename(file_path)}</span>
                            </div>
                            <div>
                                <span class="file-size">{file_ext} · {file_size:.2f} KB</span>
                            </div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="warning-box">❌ {i}. {file_path} (文件不存在)</div>', unsafe_allow_html=True)
        
        if selected_image_files:
            st.markdown(f"### 🖼️ 已选择 {len(selected_image_files)} 个图片文件:")
            
            # 创建图片预览网格
            cols = st.columns(4)  # 每行显示4张图片
            for i, file_path in enumerate(selected_image_files):
                with cols[i % 4]:
                    if os.path.exists(file_path):
                        try:
                            img = Image.open(file_path)
                            file_size = os.path.getsize(file_path) / 1024  # KB
                            st.image(img, caption=f"{os.path.basename(file_path)}\n({file_size:.2f} KB)", use_column_width=True)
                        except Exception as e:
                            st.error(f"无法预览 {os.path.basename(file_path)}: {str(e)}")
                    else:
                        st.markdown(f'<div class="warning-box">❌ {os.path.basename(file_path)} (文件不存在)</div>', unsafe_allow_html=True)
        
        # 复制按钮
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📋 开始复制", type="primary", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                success_count = 0
                error_count = 0
                skip_count = 0
                
                for i, file_path in enumerate(st.session_state["selected_files"]):
                    try:
                        # 检查文件是否存在
                        if not os.path.exists(file_path):
                            status_text.error(f"❌ 文件不存在: {file_path}")
                            error_count += 1
                            progress_bar.progress((i + 1) / len(st.session_state["selected_files"]))
                            continue
                        
                        # 获取文件名
                        file_name = os.path.basename(file_path)
                        dest_path = os.path.join(data_dir, file_name)
                        
                        # 检查目标文件是否已存在
                        if os.path.exists(dest_path):
                            status_text.warning(f"⚠️ 文件 {file_name} 已存在于知识库中，跳过")
                            skip_count += 1
                            progress_bar.progress((i + 1) / len(st.session_state["selected_files"]))
                            continue
                        
                        status_text.info(f"📄 正在复制文件: {file_name}")
                        
                        # 复制文件
                        import shutil
                        shutil.copy2(file_path, dest_path)
                        
                        # 获取文件的MD5
                        md5_hex = vector_store._get_file_md5(dest_path)
                        
                        # 检查MD5是否已存在
                        if vector_store._is_file_processed(md5_hex):
                            status_text.warning(f"⚠️ 文件 {file_name} 内容已存在于知识库中，跳过")
                            skip_count += 1
                            progress_bar.progress((i + 1) / len(st.session_state["selected_files"]))
                            continue
                        
                        # 加载文档
                        documents = vector_store._load_file(dest_path)
                        
                        if not documents:
                            status_text.warning(f"⚠️ 文件 {file_name} 内没有有效文本内容，跳过")
                            skip_count += 1
                            progress_bar.progress((i + 1) / len(st.session_state["selected_files"]))
                            continue
                        
                        # 对于图片文件，不需要分割，直接存入向量库
                        if file_name.endswith(image_extensions):
                            # 将图片内容存入向量库
                            vector_store.vector_store.add_documents(documents)
                            # 保存MD5值
                            vector_store._save_md5(md5_hex)
                            status_text.success(f"✅ 图片 {file_name} 已成功复制到知识库")
                            success_count += 1
                        else:
                            # 对于文本文件，需要分割
                            split_document = vector_store.text_splitter.split_documents(documents)
                            
                            if not split_document:
                                status_text.warning(f"⚠️ 文件 {file_name} 分片后没有有效文本内容，跳过")
                                skip_count += 1
                                progress_bar.progress((i + 1) / len(st.session_state["selected_files"]))
                                continue
                            
                            # 将内容存入向量库
                            vector_store.vector_store.add_documents(split_document)
                            
                            # 保存MD5值
                            vector_store._save_md5(md5_hex)
                            
                            status_text.success(f"✅ 文件 {file_name} 已成功复制到知识库")
                            success_count += 1
                        
                    except Exception as e:
                        status_text.error(f"❌ 文件 {os.path.basename(file_path)} 复制失败: {str(e)}")
                        error_count += 1
                    
                    progress_bar.progress((i + 1) / len(st.session_state["selected_files"]))
                
                # 显示复制结果
                st.markdown("---")
                st.markdown("### 📊 复制结果")
                col1, col2, col3 = st.columns(3)
                if success_count > 0:
                    with col1:
                        st.markdown(f'<div class="success-box">✅ 成功复制 {success_count} 个文件</div>', unsafe_allow_html=True)
                if error_count > 0:
                    with col2:
                        st.markdown(f'<div class="warning-box">❌ 失败 {error_count} 个文件</div>', unsafe_allow_html=True)
                if skip_count > 0:
                    with col3:
                        st.markdown(f'<div class="tip-box">⚠️ 跳过 {skip_count} 个文件</div>', unsafe_allow_html=True)
                
                # 清空已选择的文件
                st.session_state["selected_files"] = []
                
                # 刷新页面
                time.sleep(2)
                st.rerun()

    st.divider()

    # 知识库管理区域
    st.markdown('<p class="section-header">⚙️ 知识库管理</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🔄 重新加载知识库")
        st.markdown("重新扫描数据目录，加载所有文件到知识库")
        if st.button("🔄 重新加载知识库", type="primary", use_container_width=True):
            with st.spinner("正在重新加载知识库..."):
                try:
                    vector_store.load_documents()
                    st.markdown('<div class="success-box">✅ 知识库重新加载成功</div>', unsafe_allow_html=True)
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.markdown(f'<div class="warning-box">❌ 知识库重新加载失败: {str(e)}</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🗑️ 清空知识库")
        st.markdown("⚠️ 警告：此操作将删除所有知识库数据")
        if st.button("🗑️ 清空知识库", type="secondary", use_container_width=True):
            if st.session_state.get("confirm_clear", False):
                with st.spinner("正在清空知识库..."):
                    try:
                        # 清空向量库
                        vector_store.vector_store.delete_collection()
                        
                        # 清空MD5文件
                        md5_file = get_abs_path(chroma_conf["md5_hex_store"])
                        if os.path.exists(md5_file):
                            os.remove(md5_file)
                        
                        # 清空数据目录中的文件
                        if os.path.exists(data_dir):
                            for file in os.listdir(data_dir):
                                if file.endswith(tuple(chroma_conf["allow_knowledge_file_type"])):
                                    os.remove(os.path.join(data_dir, file))
                        
                        st.markdown('<div class="success-box">✅ 知识库已清空</div>', unsafe_allow_html=True)
                        st.session_state["confirm_clear"] = False
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.markdown(f'<div class="warning-box">❌ 清空知识库失败: {str(e)}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="warning-box">⚠️ 此操作将清空所有知识库数据，请再次点击确认</div>', unsafe_allow_html=True)
                st.session_state["confirm_clear"] = True

    st.divider()

    # 使用说明
    st.markdown('<p class="section-header">📖 使用说明</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="file-card">
        <h4>📤 上传文件</h4>
        <ol>
            <li>点击"选择要上传的文件"按钮，选择PDF、TXT、DOC、DOCX或图片格式的文件</li>
            <li>点击"🚀 开始上传"按钮将文件添加到知识库</li>
            <li>支持的文件格式: <strong>PDF, TXT, DOC, DOCX, PNG, JPG, JPEG, GIF, BMP, WEBP</strong></li>
        </ol>
    </div>
    
    <div class="file-card">
        <h4>📋 复制本地文件</h4>
        <ol>
            <li>输入文件路径（每行一个文件路径）</li>
            <li>或者直接拖拽上传文件</li>
            <li>点击"📋 开始复制"按钮将文件复制到知识库</li>
        </ol>
    </div>
    
    <div class="file-card">
        <h4>⚙️ 知识库管理</h4>
        <ul>
            <li><strong>重新加载</strong>: 点击"🔄 重新加载知识库"按钮，重新扫描数据目录</li>
            <li><strong>清空知识库</strong>: 点击"🗑️ 清空知识库"按钮，删除所有知识库数据（需二次确认）</li>
            <li><strong>删除文件</strong>: 在文件列表中点击"🗑️ 删除"按钮</li>
        </ul>
    </div>
    
    <div class="success-box">
        <strong>💡 提示</strong>: 上传文件后，您可以在智能助手中询问相关问题，智能助手会从知识库中检索相关信息来回答您的问题。
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("---")
    st.markdown("💡 **提示**: 上传文件后，您可以在智能助手中询问相关问题，智能助手会从知识库中检索相关信息来回答您的问题。")

if __name__ == "__main__":
    st.set_page_config(
        page_title="知识库文件上传",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 知识库文件上传")
    st.markdown("### 上传文件到知识库，让智能助手更聪明")
    
    main()
=======

st.set_page_config(
    page_title="知识库文件上传",
    page_icon="📚",
    layout="wide"
)

st.title("📚 知识库文件上传")
st.markdown("### 上传文件到知识库，让智能助手更聪明")
st.divider()

# 初始化向量存储
@st.cache_resource
def get_vector_store():
    return VectorStore()

vector_store = get_vector_store()

# 获取数据目录
data_dir = get_abs_path(chroma_conf["data_path"])

# 显示当前知识库中的文件
st.header("📁 当前知识库文件")
st.info(f"知识库数据目录: {data_dir}")

# 获取知识库中已有的文件
if os.path.exists(data_dir):
    existing_files = [f for f in os.listdir(data_dir) if f.endswith(tuple(chroma_conf["allow_knowledge_file_type"]))]
    if existing_files:
        # 分离图片文件和文本文件
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
        image_files = [f for f in existing_files if f.endswith(image_extensions)]
        text_files = [f for f in existing_files if not f.endswith(image_extensions)]
        
        if text_files:
            st.success(f"当前知识库中有 {len(text_files)} 个文本文件:")
            for i, file in enumerate(text_files, 1):
                file_path = os.path.join(data_dir, file)
                file_size = os.path.getsize(file_path) / 1024  # KB
                st.write(f"{i}. {file} ({file_size:.2f} KB)")
        
        if image_files:
            st.success(f"当前知识库中有 {len(image_files)} 个图片文件:")
            
            # 创建图片预览网格
            cols = st.columns(4)  # 每行显示4张图片
            for i, file in enumerate(image_files):
                file_path = os.path.join(data_dir, file)
                file_size = os.path.getsize(file_path) / 1024  # KB
                
                with cols[i % 4]:
                    try:
                        img = Image.open(file_path)
                        st.image(img, caption=f"{file}\n({file_size:.2f} KB)", use_column_width=True)
                    except Exception as e:
                        st.error(f"无法预览 {file}: {str(e)}")
    else:
        st.warning("知识库中还没有文件")
else:
    st.warning("知识库数据目录不存在")

st.divider()

# 文件上传区域
st.header("📤 上传新文件")
st.info("支持的文件格式: PDF, TXT, PNG, JPG, JPEG, GIF, BMP, WEBP")

# 文件上传
uploaded_files = st.file_uploader(
    "选择要上传的文件",
    type=chroma_conf["allow_knowledge_file_type"],
    accept_multiple_files=True,
    help="请选择PDF、TXT或图片格式的文件"
)

if uploaded_files:
    # 分离图片文件和文本文件
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
    image_files = [f for f in uploaded_files if f.name.endswith(image_extensions)]
    text_files = [f for f in uploaded_files if not f.name.endswith(image_extensions)]
    
    if text_files:
        st.write(f"已选择 {len(text_files)} 个文本文件:")
        for i, uploaded_file in enumerate(text_files, 1):
            st.write(f"{i}. {uploaded_file.name} ({uploaded_file.size / 1024:.2f} KB)")
    
    if image_files:
        st.write(f"已选择 {len(image_files)} 个图片文件:")
        
        # 创建图片预览网格
        cols = st.columns(4)  # 每行显示4张图片
        for i, uploaded_file in enumerate(image_files):
            with cols[i % 4]:
                try:
                    img = Image.open(uploaded_file)
                    st.image(img, caption=f"{uploaded_file.name}\n({uploaded_file.size / 1024:.2f} KB)", use_column_width=True)
                except Exception as e:
                    st.error(f"无法预览 {uploaded_file.name}: {str(e)}")

    # 上传按钮
    if st.button("开始上传", type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        success_count = 0
        error_count = 0
        
        for i, uploaded_file in enumerate(uploaded_files):
            try:
                # 保存文件到数据目录
                file_path = os.path.join(data_dir, uploaded_file.name)
                
                # 检查文件是否已存在
                if os.path.exists(file_path):
                    status_text.warning(f"⚠️ 文件 {uploaded_file.name} 已存在，跳过")
                    error_count += 1
                    progress_bar.progress((i + 1) / len(uploaded_files))
                    continue
                
                # 保存文件
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                status_text.info(f"📄 正在处理文件: {uploaded_file.name}")
                
                # 获取文件的MD5
                md5_hex = vector_store._get_file_md5_hex(file_path)
                
                # 检查MD5是否已存在
                if vector_store._check_md5_hex(md5_hex):
                    status_text.warning(f"⚠️ 文件 {uploaded_file.name} 内容已存在于知识库中，跳过")
                    error_count += 1
                    progress_bar.progress((i + 1) / len(uploaded_files))
                    continue
                
                # 加载文档
                documents = vector_store._get_file_documents(file_path)
                
                if not documents:
                    status_text.warning(f"⚠️ 文件 {uploaded_file.name} 内没有有效文本内容，跳过")
                    error_count += 1
                    progress_bar.progress((i + 1) / len(uploaded_files))
                    continue
                
                # 对于图片文件，不需要分割，直接存入向量库
                if uploaded_file.name.endswith(image_extensions):
                    # 将图片内容存入向量库
                    vector_store.vector_store.add_documents(documents)
                    # 保存MD5值
                    vector_store._save_md5_hex(md5_hex)
                    status_text.success(f"✅ 图片 {uploaded_file.name} 已成功上传到知识库")
                    success_count += 1
                else:
                    # 对于文本文件，需要分割
                    split_document = vector_store.text_splitter.split_documents(documents)
                    
                    if not split_document:
                        status_text.warning(f"⚠️ 文件 {uploaded_file.name} 分片后没有有效文本内容，跳过")
                        error_count += 1
                        progress_bar.progress((i + 1) / len(uploaded_files))
                        continue
                    
                    # 将内容存入向量库
                    vector_store.vector_store.add_documents(split_document)
                    
                    # 保存MD5值
                    vector_store._save_md5_hex(md5_hex)
                    
                    status_text.success(f"✅ 文件 {uploaded_file.name} 已成功上传到知识库")
                    success_count += 1
                
            except Exception as e:
                status_text.error(f"❌ 文件 {uploaded_file.name} 上传失败: {str(e)}")
                error_count += 1
            
            progress_bar.progress((i + 1) / len(uploaded_files))
        
        # 显示上传结果
        st.divider()
        st.header("📊 上传结果")
        if success_count > 0:
            st.success(f"✅ 成功上传 {success_count} 个文件")
        if error_count > 0:
            st.error(f"❌ 失败 {error_count} 个文件")
        
        # 刷新页面
        time.sleep(2)
        st.rerun()

st.divider()

# 复制文件区域
st.header("📋 复制本地文件到知识库")
st.info("从本地文件系统选择文件，复制到知识库数据目录")

# 文件路径输入
file_paths = st.text_area(
    "输入文件路径（每行一个文件路径）",
    placeholder="C:\\Users\\用户名\\Documents\\file1.pdf\nC:\\Users\\用户名\\Documents\\file2.txt\nC:\\Users\\用户名\\Pictures\\image.png",
    help="请输入完整的文件路径，每行一个文件，支持文本文件和图片文件"
)

# 或者使用文件选择器
st.markdown("或者选择文件:")
import tkinter as tk
from tkinter import filedialog

def select_files():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    root.attributes('-topmost', True)  # 窗口置顶
    
    file_types = [
        ("PDF 文件", "*.pdf"),
        ("文本文件", "*.txt"),
        ("PNG 图片", "*.png"),
        ("JPG 图片", "*.jpg;*.jpeg"),
        ("GIF 图片", "*.gif"),
        ("BMP 图片", "*.bmp"),
        ("WEBP 图片", "*.webp"),
        ("所有文件", "*.*")
    ]
    
    files = filedialog.askopenfilenames(
        title="选择要复制到知识库的文件",
        filetypes=file_types
    )
    
    root.destroy()
    return files

if st.button("📂 选择文件"):
    selected_files = select_files()
    if selected_files:
        st.session_state["selected_files"] = selected_files
        st.success(f"已选择 {len(selected_files)} 个文件")
        
        # 分离图片文件和文本文件
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
        selected_image_files = [f for f in selected_files if f.endswith(image_extensions)]
        selected_text_files = [f for f in selected_files if not f.endswith(image_extensions)]
        
        if selected_text_files:
            st.write("文本文件:")
            for i, file_path in enumerate(selected_text_files, 1):
                st.write(f"{i}. {file_path}")
        
        if selected_image_files:
            st.write("图片文件:")
            for i, file_path in enumerate(selected_image_files, 1):
                st.write(f"{i}. {file_path}")

# 显示已选择的文件
if "selected_files" in st.session_state and st.session_state["selected_files"]:
    st.divider()
    
    # 分离图片文件和文本文件
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
    selected_image_files = [f for f in st.session_state["selected_files"] if f.endswith(image_extensions)]
    selected_text_files = [f for f in st.session_state["selected_files"] if not f.endswith(image_extensions)]
    
    if selected_text_files:
        st.write(f"已选择 {len(selected_text_files)} 个文本文件:")
        for i, file_path in enumerate(selected_text_files, 1):
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path) / 1024  # KB
                st.write(f"{i}. {file_path} ({file_size:.2f} KB)")
            else:
                st.error(f"{i}. {file_path} (文件不存在)")
    
    if selected_image_files:
        st.write(f"已选择 {len(selected_image_files)} 个图片文件:")
        
        # 创建图片预览网格
        cols = st.columns(4)  # 每行显示4张图片
        for i, file_path in enumerate(selected_image_files):
            with cols[i % 4]:
                if os.path.exists(file_path):
                    try:
                        img = Image.open(file_path)
                        file_size = os.path.getsize(file_path) / 1024  # KB
                        st.image(img, caption=f"{os.path.basename(file_path)}\n({file_size:.2f} KB)", use_column_width=True)
                    except Exception as e:
                        st.error(f"无法预览 {os.path.basename(file_path)}: {str(e)}")
                else:
                    st.error(f"{os.path.basename(file_path)} (文件不存在)")
    
    # 复制按钮
    if st.button("开始复制", type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        success_count = 0
        error_count = 0
        
        for i, file_path in enumerate(st.session_state["selected_files"]):
            try:
                # 检查文件是否存在
                if not os.path.exists(file_path):
                    status_text.error(f"❌ 文件不存在: {file_path}")
                    error_count += 1
                    progress_bar.progress((i + 1) / len(st.session_state["selected_files"]))
                    continue
                
                # 获取文件名
                file_name = os.path.basename(file_path)
                dest_path = os.path.join(data_dir, file_name)
                
                # 检查目标文件是否已存在
                if os.path.exists(dest_path):
                    status_text.warning(f"⚠️ 文件 {file_name} 已存在于知识库中，跳过")
                    error_count += 1
                    progress_bar.progress((i + 1) / len(st.session_state["selected_files"]))
                    continue
                
                status_text.info(f"📄 正在复制文件: {file_name}")
                
                # 复制文件
                import shutil
                shutil.copy2(file_path, dest_path)
                
                # 获取文件的MD5
                md5_hex = vector_store._get_file_md5_hex(dest_path)
                
                # 检查MD5是否已存在
                if vector_store._check_md5_hex(md5_hex):
                    status_text.warning(f"⚠️ 文件 {file_name} 内容已存在于知识库中，跳过")
                    error_count += 1
                    progress_bar.progress((i + 1) / len(st.session_state["selected_files"]))
                    continue
                
                # 加载文档
                documents = vector_store._get_file_documents(dest_path)
                
                if not documents:
                    status_text.warning(f"⚠️ 文件 {file_name} 内没有有效文本内容，跳过")
                    error_count += 1
                    progress_bar.progress((i + 1) / len(st.session_state["selected_files"]))
                    continue
                
                # 对于图片文件，不需要分割，直接存入向量库
                if file_name.endswith(image_extensions):
                    # 将图片内容存入向量库
                    vector_store.vector_store.add_documents(documents)
                    # 保存MD5值
                    vector_store._save_md5_hex(md5_hex)
                    status_text.success(f"✅ 图片 {file_name} 已成功复制到知识库")
                    success_count += 1
                else:
                    # 对于文本文件，需要分割
                    split_document = vector_store.text_splitter.split_documents(documents)
                    
                    if not split_document:
                        status_text.warning(f"⚠️ 文件 {file_name} 分片后没有有效文本内容，跳过")
                        error_count += 1
                        progress_bar.progress((i + 1) / len(st.session_state["selected_files"]))
                        continue
                    
                    # 将内容存入向量库
                    vector_store.vector_store.add_documents(split_document)
                    
                    # 保存MD5值
                    vector_store._save_md5_hex(md5_hex)
                    
                    status_text.success(f"✅ 文件 {file_name} 已成功复制到知识库")
                    success_count += 1
                
            except Exception as e:
                status_text.error(f"❌ 文件 {os.path.basename(file_path)} 复制失败: {str(e)}")
                error_count += 1
            
            progress_bar.progress((i + 1) / len(st.session_state["selected_files"]))
        
        # 显示复制结果
        st.divider()
        st.header("📊 复制结果")
        if success_count > 0:
            st.success(f"✅ 成功复制 {success_count} 个文件")
        if error_count > 0:
            st.error(f"❌ 失败 {error_count} 个文件")
        
        # 清空已选择的文件
        st.session_state["selected_files"] = []
        
        # 刷新页面
        time.sleep(2)
        st.rerun()

st.divider()

# 知识库管理区域
st.header("⚙️ 知识库管理")

# 重新加载知识库按钮
if st.button("重新加载知识库"):
    with st.spinner("正在重新加载知识库..."):
        try:
            vector_store.load_documents()
            st.success("✅ 知识库重新加载成功")
            time.sleep(1)
            st.rerun()
        except Exception as e:
            st.error(f"❌ 知识库重新加载失败: {str(e)}")

# 清空知识库按钮
if st.button("清空知识库", type="secondary"):
    if st.session_state.get("confirm_clear", False):
        with st.spinner("正在清空知识库..."):
            try:
                # 清空向量库
                vector_store.vector_store.delete_collection()
                
                # 清空MD5文件
                md5_file = get_abs_path(chroma_conf["md5_hex_store"])
                if os.path.exists(md5_file):
                    os.remove(md5_file)
                
                # 清空数据目录中的文件
                if os.path.exists(data_dir):
                    for file in os.listdir(data_dir):
                        if file.endswith(tuple(chroma_conf["allow_knowledge_file_type"])):
                            os.remove(os.path.join(data_dir, file))
                
                st.success("✅ 知识库已清空")
                st.session_state["confirm_clear"] = False
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"❌ 清空知识库失败: {str(e)}")
    else:
        st.warning("⚠️ 此操作将清空所有知识库数据，请再次点击确认")
        st.session_state["confirm_clear"] = True

st.divider()

# 使用说明
st.header("📖 使用说明")
st.markdown("""
### 📤 上传文件
1. 点击"选择要上传的文件"按钮，选择PDF、TXT或图片格式的文件
2. 点击"开始上传"按钮将文件添加到知识库
3. 支持的图片格式: PNG, JPG, JPEG, GIF, BMP, WEBP

### 📋 复制文件
1. 点击"📂 选择文件"按钮，从本地文件系统选择文件
2. 或者直接输入文件路径（每行一个文件路径）
3. 点击"开始复制"按钮将文件复制到知识库

### ⚙️ 知识库管理
1. **重新加载**: 点击"重新加载知识库"按钮，重新加载所有文件到知识库
2. **清空知识库**: 点击"清空知识库"按钮，清空所有知识库数据（需要确认）

**注意事项**:
- 支持的文件格式: PDF, TXT, PNG, JPG, JPEG, GIF, BMP, WEBP
- 文件会自动去重，相同内容的文件不会重复添加
- 上传/复制的文件会保存到知识库数据目录中
- 图片文件会显示预览，方便识别
- 知识库数据目录: `{data_dir}`
""")

st.divider()
st.markdown("---")
st.markdown("💡 **提示**: 上传文件后，您可以在智能助手中询问相关问题，智能助手会从知识库中检索相关信息来回答您的问题。")
>>>>>>> 60952ec67107fb30fedf61073e0a6aa6470c650d
