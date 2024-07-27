from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.pdf import PyMuPDFLoader
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_openai import OpenAIEmbeddings


def init_qdrant(file, qdrant_url):
    # 文件嵌入到向量数据库
    docs = PyMuPDFLoader(file).load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    documents = text_splitter.split_documents(docs)
    # 返回数据库访问对象
    qdrant = Qdrant.from_documents(
        documents=documents,
        embedding=OpenAIEmbeddings(),
        url=qdrant_url,
        prefer_grpc=False,
        collection_name="danwen_docs"
    )
    return qdrant
