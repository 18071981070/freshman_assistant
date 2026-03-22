from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
import os
import base64
from PIL import Image
import io


def listdir_with_allowed_type(dir_path, allowed_extensions):
    """
    列出目录下指定类型的文件

    Args:
        dir_path: 目录路径
        allowed_extensions: 允许的文件扩展名元组，如 ('.pdf', '.txt') 或 ('pdf', 'txt')

    Returns:
        符合条件的文件路径列表
    """
    result = []

    if not os.path.exists(dir_path):
        return result

    # 确保扩展名格式统一（都带点）
    normalized_extensions = tuple(
        ext if ext.startswith('.') else '.' + ext
        for ext in allowed_extensions
    )

    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.lower().endswith(normalized_extensions):
                file_path = os.path.join(root, file)
                result.append(file_path)

    return result


class ImageLoader:
    """
    图片文件加载器
    支持加载图片文件并提取图片信息（如尺寸、格式等）
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> list[Document]:
        """
        加载图片文件

        Returns:
            包含图片信息的 Document 列表
        """
        try:
            # 打开图片
            with Image.open(self.file_path) as img:
                # 获取图片基本信息
                width, height = img.size
                format_type = img.format
                mode = img.mode

                # 将图片转换为base64
                buffered = io.BytesIO()
                img.save(buffered, format=format_type if format_type else 'PNG')
                img_base64 = base64.b64encode(buffered.getvalue()).decode()

                # 创建包含图片信息的Document
                content = f"[图片文件: {os.path.basename(self.file_path)}]\n"
                content += f"格式: {format_type}\n"
                content += f"尺寸: {width}x{height}\n"
                content += f"模式: {mode}\n"
                content += f"Base64数据: {img_base64[:100]}..."

                return [Document(
                    page_content=content,
                    metadata={
                        "source": self.file_path,
                        "type": "image",
                        "format": format_type,
                        "width": width,
                        "height": height
                    }
                )]
        except Exception as e:
            print(f"加载图片失败 {self.file_path}: {e}")
            return []
