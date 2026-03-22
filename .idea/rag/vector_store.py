import sys
import os
import hashlib

current_file = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.config_hander import chroma_conf
from utils.path_tool import get_abs_path
from utils.file_handler import PyPDFLoader, TextLoader, ImageLoader, listdir_with_allowed_type
from model.factory import embeddings
from utils.logger_handler import logger


class VectorStore:
    def __init__(self):
        self.persist_directory = get_abs_path(chroma_conf["persist_directory"])
        self.md5_file = get_abs_path(chroma_conf["md5_hex_store"])
        
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            embedding_function=embeddings,
            persist_directory=self.persist_directory
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            length_function=len
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})

    def _get_file_md5(self, file_path: str) -> str:
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()

    def _is_file_processed(self, md5: str) -> bool:
        if not os.path.exists(self.md5_file):
            return False
        with open(self.md5_file, 'r', encoding='utf-8') as f:
            return md5 in [line.strip() for line in f]

    def _save_md5(self, md5: str):
        with open(self.md5_file, 'a', encoding='utf-8') as f:
            f.write(md5 + "\n")

    def _load_file(self, file_path: str):
        loaders = {
            ".pdf": PyPDFLoader,
            ".txt": TextLoader
        }
        ext = os.path.splitext(file_path)[1].lower()
        if ext in (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"):
            loader = ImageLoader(file_path)
        elif ext in loaders:
            loader = loaders[ext](file_path)
        else:
            raise ValueError(f"不支持的文件类型: {file_path}")
        return loader.load()

    def load_documents(self):
        files = listdir_with_allowed_type(
            chroma_conf["data_path"],
            tuple(chroma_conf["allow_knowledge_file_type"])
        )
        
        all_docs = []
        image_exts = (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp")
        
        for path in files:
            md5 = self._get_file_md5(path)
            if self._is_file_processed(md5):
                logger.info(f"[加载知识库]{path}已存在，跳过")
                continue

            try:
                docs = self._load_file(path)
                if not docs:
                    logger.warning(f"[加载知识库]{path}无有效内容，跳过")
                    continue

                if path.endswith(image_exts):
                    all_docs.extend(docs)
                else:
                    all_docs.extend(self.text_splitter.split_documents(docs))
                
                self._save_md5(md5)
                logger.info(f"[加载知识库]{path}已添加")
                    
            except Exception as e:
                logger.error(f"[加载知识库]{path}加载失败: {e}")

        if all_docs:
            logger.info(f"开始创建向量库，共 {len(all_docs)} 个文档...")
            try:
                batch_size = 10
                for i in range(0, len(all_docs), batch_size):
                    batch = all_docs[i:i + batch_size]
                    logger.info(f"处理批次 {i//batch_size + 1}/{(len(all_docs) + batch_size - 1)//batch_size}")
                    self.vector_store.add_documents(batch)
                logger.info("向量库创建成功")
            except Exception as e:
                logger.error(f"创建向量库失败: {e}")
        else:
            logger.info("没有新文档需要处理")


if __name__ == "__main__":
    vs = VectorStore()
    vs.load_documents()
    retriever = vs.get_retriever()
    
    print("开始检索...")
    for i, r in enumerate(retriever.invoke("保研")):
        print(f"\n结果 {i+1}:\n{r.page_content[:200]}\n-----------------")
