# 部署指南

## Streamlit Community Cloud 部署步骤

### 第一步：创建GitHub仓库

1. **登录GitHub**
   - 访问 https://github.com
   - 登录或注册账号

2. **创建新仓库**
   - 点击右上角 "+" → "New repository"
   - 仓库名称：`freshman_assistant`
   - 选择 "Public"（公开）
   - 点击 "Create repository"

### 第二步：上传代码到GitHub

**方法一：使用Git命令**

```bash
# 1. 在项目目录下初始化Git
git init

# 2. 添加所有文件
git add .

# 3. 提交
git commit -m "Initial commit"

# 4. 添加远程仓库（替换YOUR_USERNAME为您的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/freshman_assistant.git

# 5. 推送到GitHub
git branch -M main
git push -u origin main
```

**方法二：使用GitHub网页上传**

1. 在GitHub仓库页面点击 "uploading an existing file"
2. 拖拽所有项目文件到上传区域
3. 点击 "Commit changes"

### 第三步：部署到Streamlit Cloud

1. **访问 Streamlit Cloud**
   - 打开 https://share.streamlit.io
   - 使用GitHub账号登录

2. **部署应用**
   - 点击 "New app"
   - 选择仓库：`freshman_assistant`
   - 选择分支：`main`
   - 主文件路径：`app.py`
   - 点击 "Deploy!"

3. **等待部署完成**
   - 首次部署可能需要5-10分钟
   - 部署成功后，您会获得一个链接：`https://your-app-name.streamlit.app`

### 第四步：配置环境变量（如需要）

如果您的应用需要API密钥等敏感信息：

1. 在Streamlit Cloud应用页面点击 "Settings"
2. 找到 "Secrets" 部分
3. 添加键值对，例如：
   ```
   QIANFAN_API_KEY = "your_api_key_here"
   ```

### 注意事项

1. **隐私文件**：确保以下文件不会上传到GitHub：
   - `secrets.toml`（包含API密钥）
   - `chroma_db/`（向量数据库）
   - `data/`（知识库数据）

2. **创建 .gitignore 文件**：
   ```
   .streamlit/secrets.toml
   chroma_db/
   data/
   __pycache__/
   *.pyc
   .idea/
   *.log
   ```

3. **如果需要公开知识库**，可以将data文件夹添加到仓库中

### 常见问题

**Q: 部署失败怎么办？**
A: 检查Build Logs中的错误信息，常见问题包括：
- 依赖版本不兼容
- 文件路径错误
- 缺少必要的配置文件

**Q: 如何更新应用？**
A: 只需将新代码推送到GitHub仓库，Streamlit Cloud会自动重新部署

**Q: 应用访问不了？**
A: 检查是否需要配置CORS或代理设置

---

如有问题，请联系项目维护者。
