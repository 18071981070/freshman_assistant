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
        allowed_extensions: 允许的文件扩展名元组，如 ('.pdf', '.txt')
        
    Returns:
        符合条件的文件路径列表
    """
    result = []
    
    if not os.path.exists(dir_path):
        return result
    
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith(allowed_extensions):
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
            # 打开图片文件
            with Image.open(self.file_path) as img:
                # 获取图片基本信息
                width, height = img.size
                format_type = img.format
                mode = img.mode
                
                # 获取文件名
                file_name = os.path.basename(self.file_path)
                
                # 构建图片描述文本
                content = f"图片文件: {file_name}\n"
                content += f"图片格式: {format_type}\n"
                content += f"图片尺寸: {width} x {height}\n"
                content += f"颜色模式: {mode}\n"
                content += f"文件路径: {self.file_path}\n"
                
                # 如果是可识别的图片（如图表、文档截图等），可以添加更多描述
                # 这里可以集成 OCR 功能来提取图片中的文字
                
                # 创建 Document 对象
                document = Document(
                    page_content=content,
                    metadata={
                        "source": self.file_path,
                        "file_name": file_name,
                        "file_type": "image",
                        "image_format": format_type,
                        "image_width": width,
                        "image_height": height,
                        "image_mode": mode,
                    }
                )
                
                return [document]
                
        except Exception as e:
            # 如果图片加载失败，返回一个包含错误信息的 Document
            file_name = os.path.basename(self.file_path)
            content = f"图片文件: {file_name}\n"
            content += f"文件路径: {self.file_path}\n"
            content += f"加载失败: {str(e)}\n"
            
            document = Document(
                page_content=content,
                metadata={
                    "source": self.file_path,
                    "file_name": file_name,
                    "file_type": "image",
                    "error": str(e),
                }
            )
            
            return [document]


class ImageLoaderWithOCR(ImageLoader):
    """
    带 OCR 功能的图片文件加载器
    可以提取图片中的文字内容
    """
    
    def __init__(self, file_path: str, use_ocr: bool = False):
        super().__init__(file_path)
        self.use_ocr = use_ocr
    
    def load(self) -> list[Document]:
        """
        加载图片文件，可选使用 OCR 提取文字
        
        Returns:
            包含图片信息和 OCR 文本的 Document 列表
        """
        documents = super().load()
        
        if self.use_ocr and documents:
            try:
                # 尝试使用 OCR 提取图片中的文字
                # 这里可以使用 pytesseract 或其他 OCR 库
                # 为了简化，这里先预留接口
                ocr_text = self._extract_text_with_ocr()
                if ocr_text:
                    # 在原有内容基础上添加 OCR 文本
                    original_content = documents[0].page_content
                    documents[0].page_content = original_content + f"\n图片中的文字内容:\n{ocr_text}"
                    documents[0].metadata["has_ocr_text"] = True
                    documents[0].metadata["ocr_text"] = ocr_text
            except Exception as e:
                # OCR 失败不影响基本图片信息
                documents[0].metadata["ocr_error"] = str(e)
        
        return documents
    
    def _extract_text_with_ocr(self) -> str:
        """
        使用 OCR 提取图片中的文字
        
        Returns:
            提取的文字内容
        """
        # 这里可以集成 pytesseract 或其他 OCR 库
        # 示例代码（需要安装 pytesseract 和 Tesseract-OCR）：
        # import pytesseract
        # image = Image.open(self.file_path)
        # text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        # return text
        
        # 目前返回空字符串，表示未启用 OCR
        return ""


def get_image_base64(file_path: str) -> str:
    """
    将图片文件转换为 base64 编码
    
    Args:
        file_path: 图片文件路径
        
    Returns:
        base64 编码的图片字符串
    """
    try:
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return encoded_string
    except Exception as e:
        return f""


def get_image_mime_type(file_path: str) -> str:
    """
    获取图片文件的 MIME 类型
    
    Args:
        file_path: 图片文件路径
        
    Returns:
        MIME 类型字符串
    """
    extension = os.path.splitext(file_path)[1].lower()
    mime_types = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.bmp': 'image/bmp',
        '.webp': 'image/webp',
    }
    return mime_types.get(extension, 'application/octet-stream')