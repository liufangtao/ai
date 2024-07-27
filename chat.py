# 导入chainlit库，用于处理聊天事件
import chainlit as cl
# 当聊天开始时，chainlit会调用这个装饰过的函数
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory, ConversationBufferWindowMemory
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI


@cl.on_chat_start
async def on_chat_start():
    chat = ChatOpenAI(temperature=0.7)
    memory = ConversationBufferMemory()
    # memory = ConversationBufferWindowMemory
    conversation = ConversationChain(llm=chat, memory=memory)
    cl.user_session.set("conversation", conversation)


@cl.on_message
async def on_message(message: cl.Message):
    # 从用户会话中获取ConversationChain对象
    conversation = cl.user_session.get("conversation")  # type: ConversationChain

    # 创建一个空的AIMessage对象，用于接收处理后的消息
    msg = cl.Message(content="")
    # 异步迭代Runnable对象的输出，处理新消息和聊天记录
    async for chunk in conversation.astream(
            {"input": message.content},
            config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        # 将处理后的消息块流式发送给用户
        await msg.stream_token(chunk.get("response"))

    # 更新消息状态，这可能是将消息发送给用户或其他处理
    await msg.send()
