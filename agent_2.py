from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_community.llms import OpenAI

from order_api import search_order, recommend_product, faq

load_dotenv()
tools = [
    Tool(
        name="Search Order", func=search_order,
        description="""
    一个帮助用户查询最新订单状态的工具，并且能处理以下情况:
    1.在用户没有输入订单号的时候，会询问用户订单号
    2.在用户输入的订单号查询不到的时候，会让用户二次确认订单号是否正确
    """
    ),
    Tool(
        name="Recommend Product", func=recommend_product,
        description="useful for when you need to answer questions about product recommendations"
    ),
    Tool(
        name="FAQ", func=faq,
        description="useful for when you need to answer questions about shopping policies, like return policy,shipping policy. etc"
    ),
]
llm = OpenAI(temperature=0)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
question = "我有一张订单，订单号是 2022ABCDE，一直没有收到，能麻烦帮我查一下吗?"
result = agent.invoke({"input": question})
print(result)
