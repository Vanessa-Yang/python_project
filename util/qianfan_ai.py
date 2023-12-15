# 填充API Key与Secret Key
import requests
import json
import qianfan
import redis

# 建立 Redis 连接
redis_client = redis.StrictRedis(host='122.112.202.79', password="DaTcaChe1hbl#QT!", port=12363, db=0,
                                 socket_timeout=5000)

QIANFAN_AK = "iQofygrAaGoXoU6Rbylzc4E8"
QIANFAN_SK = "GC2SufSr4ycf6jEfsxgsZoE1DArZRGXt"
ACCESS_TOKEN = "24.4e59c1386ca833fd3b64ae5dbcd76fcd.2592000.1700277069.282335-41174501"

CACHE_KEY = "qianfan_chat_ai:access_token"


def chat_ai():
    # 替换下列示例中参数，应用API Key替换your_ak，Secret Key替换your_sk
    chat_comp = qianfan.ChatCompletion(ak=QIANFAN_AK, sk=QIANFAN_SK)

    # 调用默认模型，即 ERNIE-Bot-turbo
    resp = chat_comp.do(messages=[{
        "role": "user",
        "content": "请为我写一篇关于室内装修的作品介绍，符合年轻人审美，具有小红书风格"
    }])

    print(resp['body']['result'])

    # 异步调用
    # resp = await chat_comp.ado(model="ERNIE-Bot-turbo", messages=[{
    #     "role": "user",
    #     "content": "你好"
    # }])
    # print(resp['body']['result'])
    #
    # # 异步流式调用
    # resp = await chat_comp.ado(model="ERNIE-Bot-turbo", messages=[{
    #     "role": "user",
    #     "content": "你好"
    # }], stream=True)
    #
    # async for r in resp:
    #     print(r['result'])


# 输入：你好
# 输出：你好！有什么我可以帮助你的吗？

def access_token() -> str:
    if redis_client.exists(CACHE_KEY):
        return redis_client.get(CACHE_KEY)

    url = f"https://aip.baidubce.com/oauth/2.0/token?client_id={QIANFAN_AK}&client_secret={QIANFAN_SK}&grant_type=client_credentials"
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    acc_token = response.json()['access_token']

    # 注意：access_token默认有效期30天，生产环境注意及时刷新。
    # 此处按 28 天缓存
    # r.set(CACHE_KEY, token, 28 * 24 * 3600 * 1000)
    redis_client.set(CACHE_KEY, acc_token, 100)

    return redis_client.get(CACHE_KEY)


if __name__ == '__main__':
    # token = access_token()
    # print(token)
    # if r.get(CACHE_KEY) == token:
    #     print("Token is cached")
    chat_ai()
