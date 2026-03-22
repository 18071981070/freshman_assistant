from abc import ABC, abstractmethod
from typing import Optional, Union
import os

try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models import ChatTongyi
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from utils.config_hander import rag_conf


def get_api_key():
    if HAS_STREAMLIT:
        try:
            return st.secrets.get("DASHSCOPE_API_KEY") or os.environ.get("DASHSCOPE_API_KEY")
        except Exception:
            return os.environ.get("DASHSCOPE_API_KEY")
    return os.environ.get("DASHSCOPE_API_KEY")


class BaseModelFactory(ABC):
    @abstractmethod
    def generate_base_model(self) -> Optional[Union[Embeddings, BaseChatModel]]:
        pass


class ChatModelFactory(BaseModelFactory):
    def generate_base_model(self) -> Optional[Union[Embeddings, BaseChatModel]]:
        api_key = get_api_key()
        if api_key:
            return ChatTongyi(
                model=rag_conf["chat_model_name"],
                dashscope_api_key=api_key
            )
        return ChatTongyi(model=rag_conf["chat_model_name"])


class EmbeddingsFactory(BaseModelFactory):
    def generate_base_model(self) -> Optional[Union[Embeddings, BaseChatModel]]:
        api_key = get_api_key()
        if api_key:
            return DashScopeEmbeddings(
                model=rag_conf["embedding_model_name"],
                dashscope_api_key=api_key
            )
        return DashScopeEmbeddings(model=rag_conf["embedding_model_name"])


chat_model = ChatModelFactory().generate_base_model()
embeddings = EmbeddingsFactory().generate_base_model()
