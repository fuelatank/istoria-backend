import os
import logging
import ssl
from fastapi import HTTPException
import websocket
import json
import base64
import hmac
import hashlib
import datetime
import threading
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
    signature_origin = f"host: iat-api.xfyun.cn\ndate: {date}\nGET /v2/iat HTTP/1.1"

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
    v = {"authorization": authorization, "date": date, "host": "iat-api.xfyun.cn"}

    # 拼接url
    url = f"wss://iat-api.xfyun.cn/v2/iat?{urlencode(v)}"

    logging.debug(f"Generated URL: {url}")
    return url


# 处理收到的消息
def on_message(ws, message, result_container):
    try:
        logging.debug("Received a message from the server.")
        response = json.loads(message)
        if response["code"] != 0:
            result_container["error"] = response["message"]
            ws.close()
            return

        if "data" in response and "result" in response["data"]:
            result = response["data"]["result"]
            if "ws" in result:
                for ws_item in result["ws"]:
                    for cw_item in ws_item["cw"]:
                        result_container["text"] += cw_item["w"]

        if response["data"]["status"] == 2:
            print("\n语音识别完成！")
            ws.close()

    except Exception as e:
        print(f"处理消息时出错: {str(e)}")
        result_container["error"] = str(e)
        ws.close()


def on_error(ws, error, result_container):
    logging.error(f"发生错误: {str(error)}")
    result_container["error"] = str(error)


def on_close(ws, close_status_code, close_msg):
    logging.debug("连接已关闭")


def on_open(ws, audio_data, result_container):
    def run(*args):
        try:
            logging.debug("WebSocket connection opened. Sending audio data...")
            # 构建请求参数
            data = {
                "common": {"app_id": APPID},
                "business": {
                    "language": "zh_cn",
                    "domain": "iat",
                    "accent": "mandarin",
                    "dwa": "wpgs",  # 开启动态修正
                },
                "data": {
                    "status": 0,
                    "format": "audio/L16;rate=16000",
                    "encoding": "lame",
                    "audio": base64.b64encode(audio_data).decode("utf-8"),
                },
            }

            # 发送数据
            ws.send(json.dumps(data))

            # 发送结束标识
            end_data = {"data": {"status": 2}}
            ws.send(json.dumps(end_data))

        except Exception as e:
            logging.error(f"发送数据时出错: {str(e)}")
            result_container["error"] = str(e)
            ws.close()

    threading.Thread(target=run).start()


def main():
    # 创建websocket连接
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(
        create_url(), on_message=on_message, on_error=on_error, on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()


async def speech_to_text(file_name: str) -> str:

    # Normalize and validate the file name
    safe_file_name = os.path.basename(file_name)
    file_path = os.path.join("./audio_files", safe_file_name)

    # Check if the file exists in the directory
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found.")

    # Read the audio file
    try:
        with open(file_path, "rb") as f:
            audio_data = f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading audio file: {str(e)}")

    result_container = {"text": "", "error": None}

    ws = websocket.WebSocketApp(
        create_url(),
        on_message=lambda ws, msg: on_message(ws, msg, result_container),
        on_error=lambda ws, err: on_error(ws, err, result_container),
        on_close=on_close,
    )
    ws.on_open = lambda ws: on_open(ws, audio_data, result_container)

    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    if result_container["error"]:
        raise HTTPException(status_code=500, detail=result_container["error"])

    return result_container["text"]


if __name__ == "__main__":
    main()
