# 导入langchain库中的ChatOpenAI聊天模型
from langchain.chains import create_retrieval_chain, RetrievalQA
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_models import ChatOpenAI
# 导入langchain库中的ChatPromptTemplate，用于构建聊天提示
from langchain.prompts import ChatPromptTemplate
# 导入langchain库中的StrOutputParser，用于解析输出字符串
from langchain.schema import StrOutputParser
# 导入langchain库中的Runnable，表示可运行的聊天流程
from langchain.schema.runnable import Runnable
# 导入langchain库中的RunnableConfig，用于配置Runnable的行为
from langchain.schema.runnable.config import RunnableConfig

# 导入chainlit库，用于处理聊天事件
import chainlit as cl
# 从langchain_community库中导入DQuestionChat模型，用于处理特定类型的聊天
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models.dquestion import DQuestionChat
# 从langchain_core库中导入AIMessage，用于表示AI发送的消息
from langchain_community.document_loaders import WebBaseLoader, PyMuPDFLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.messages import AIMessage
# 从langchain_core库中导入MessagesPlaceholder，用于在提示中占位消息
from langchain_core.prompts import MessagesPlaceholder

# 当聊天开始时，chainlit会调用这个装饰过的函数
from langchain_openai import OpenAIEmbeddings

from qdrant_vector import init_qdrant


@cl.on_chat_start
async def on_chat_start():
    # 加载pdf文件
    files = None
    # Wait for the user to upload a file
    while files is None:
        files = await cl.AskFileMessage(
            content="请上传一个文件", accept=["application/pdf"]
        ).send()
    # 嵌入文件到QDrant数据库
    qdrant = init_qdrant(files[0].path, "http://114.55.110.60:6333")

    await cl.Message(
        content=f"`{files[0].name}` 已上传成功！"
    ).send()

    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(stream=True),
        chain_type="stuff",
        retriever=qdrant.as_retriever(),
        verbose=True,
    )
    cl.user_session.set("qa", qa)


# 当收到消息时，chainlit会调用这个装饰过的函数
@cl.on_message
async def on_message(message: cl.Message):
    # 从用户会话中获取RetrievalQA对象
    qa = cl.user_session.get("qa")  # type: RetrievalQA

    # 创建一个空的AIMessage对象，用于接收处理后的消息
    msg = cl.Message(content="")
    # 异步迭代Runnable对象的输出，处理新消息和聊天记录
    async for chunk in qa.astream(
            {"query": message.content},
            config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk.get("result"))

    await msg.send()
