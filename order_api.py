import json
import re
import jmespath

import requests


# pip install jmespath

def search_order(input: str) -> str:
    pattern = r"\d+[A-Z]+"
    match = re.search(pattern, input)
    if match:
        # 得到整个订单字符串
        order_number = match.group(0)
    else:
        return "请问您的订单号是多少?"
    with open("./data/db.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    result = jmespath.search(f"orders[?order_number=='{order_number}']", data)
    if len(result) == 0:
        return f"对不起，根据 {order_number} 没有找到您的订单"
    return result
    # 调用订单查询接口（内部系统）
    # response = requests.get(f"http://127.0.0.1:3000/orders?order_number={order_number}")
    # return response.json()


# 模拟问关于推荐产品
def recommend_product(input: str) -> str:
    return "红色连衣裙"


# 模拟问电商faq
# @tool("FAQ")
def faq(input: str) -> str:
    return "7天无理由退货"
