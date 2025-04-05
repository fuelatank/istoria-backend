import websocket
import json
import base64
import hmac
import hashlib
import datetime
import os
from urllib.parse import urlencode

# 配置信息
APPID = "b340711c"
APIKey = "988e898fd5dc687c32ff10aab6ca5cda"
APISecret = "M2YwM2VjOTRlYWE0Y2E2YmJjNDIxZmRl"


# 生成鉴权url
def create_url():
    # 生成RFC1123格式的时间戳
    now = datetime.datetime.now()
    date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")

    # 拼接签名字符串
    signature_origin = f"host: tts-api.xfyun.cn\ndate: {date}\nGET /v2/tts HTTP/1.1"

    # 进行hmac-sha256进行加密
    signature_sha = hmac.new(
        APISecret.encode("utf-8"), signature_origin.encode("utf-8"), hashlib.sha256
    ).digest()
    signature = base64.b64encode(signature_sha).decode(encoding="utf-8")

    # 拼接authorization
    authorization_origin = f'api_key="{APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'
    authorization = base64.b64encode(authorization_origin.encode("utf-8")).decode(
        encoding="utf-8"
    )

    # 将请求参数编码
    v = {"authorization": authorization, "date": date, "host": "tts-api.xfyun.cn"}

    # 拼接url
    url = f"wss://tts-api.xfyun.cn/v2/tts?{urlencode(v)}"
    return url


# 处理收到的消息
def on_message(ws, message):
    try:
        response = json.loads(message)
        if response["code"] != 0:
            print(f"错误: {response['message']}")
            return

        if "data" in response and "audio" in response["data"]:
            audio = response["data"]["audio"]
            audio_data = base64.b64decode(audio)

            # 保存音频数据
            with open("Story.mp3", "ab") as f:
                f.write(audio_data)

        if response["data"]["status"] == 2:
            print("语音合成完成！")
            ws.close()

    except Exception as e:
        print(f"处理消息时出错: {str(e)}")


def on_error(ws, error):
    print(f"发生错误: {str(error)}")


def on_close(ws, close_status_code, close_msg):
    print("连接已关闭")


def on_open(ws):
    def run(*args):
        try:
            # 读取偏好内容
            with open("Story.txt", "r", encoding="utf-8") as f:
                text = f.read()

            # 构建请求参数
            data = {
                "common": {"app_id": APPID},
                "business": {
                    "aue": "lame",  # 使用mp3格式
                    "sfl": 1,  # 开启流式返回
                    "auf": "audio/L16;rate=16000",
                    "vcn": "xiaoyan",  # 使用小燕发音人
                    "speed": 50,  # 语速
                    "volume": 50,  # 音量
                    "pitch": 50,  # 音高
                    "tte": "UTF8",  # 文本编码格式
                },
                "data": {
                    "text": base64.b64encode(text.encode("utf-8")).decode("utf-8"),
                    "status": 2,
                },
            }

            # 发送数据
            ws.send(json.dumps(data))

        except Exception as e:
            print(f"发送数据时出错: {str(e)}")

    # 启动发送线程
    import threading

    threading.Thread(target=run).start()


def main():
    # 如果存在旧的音频文件，先删除
    if os.path.exists("Story.mp3"):
        os.remove("Story.mp3")

    # 创建websocket连接
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(
        create_url(), on_message=on_message, on_error=on_error, on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()


if __name__ == "__main__":
    main()
