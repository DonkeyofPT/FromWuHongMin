import xpath
import os
import time
import requests as requests

from messages import message_pb2
from messages.chat import ChatMessage


def getScriptDir():
    return os.path.split(os.path.realpath(__file__))[0]


def log_request(intercepted_request):
    print("a request was made:", intercepted_request.url)


def downloadImg(url, path):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        open(path, 'wb').write(r.content) #将内容写入图片
        print(f"CODE: {r.status_code} download {url} to {path}") # 返回状态码
        r.close()
        return path
    else:
        print(f"CODE: {r.status_code} download {url} Failed.")
        return "error"


class Watcher:
    def __init__(self):
        self.monitoringFile = './douyinLiveFile/'

    def startWatcher(self):
        print("while true")
        while True:
            files = os.listdir(self.monitoringFile)
            if files:
                for _ in files:
                    filepath = self.monitoringFile + '\\' + _

                    with open(filepath, 'rb') as f:
                        # print(f.read())
                        response = message_pb2.Response()
                        response.ParseFromString(f.read())

                    for message in response.messages:
                        if message.method == 'WebcastChatMessage':
                            chat_message = ChatMessage()
                            chat_message.set_payload(message.payload)
                            print(type(chat_message))

                            # userID
                            userID = chat_message.user().id
                            # userShortID
                            userShortID = chat_message.user().shortId
                            # userName
                            userName = chat_message.user().nickname
                            # 发言
                            content = chat_message.instance.content
                            # 头像
                            userHeaderImg = chat_message.user().avatarThumb.urlList[0]
                            print(userName, userShortID, content, userHeaderImg)
                            filePath = downloadImg(userHeaderImg, f"{getScriptDir()}\\userImages\\{userID}.jpg")
                            # Socket.sendMsg(f"{userID}\0{content}\0{filePath}")

                    try:
                        os.remove(filepath)
                    except PermissionError as e:
                        time.sleep(1)
                        os.remove(filepath)

            time.sleep(2)


if __name__ == '__main__':
    xpath.mkdir('./douyinLiveFile/')
    xpath.mkdir('./userImages/')

    print("startWatcher")
    Watcher().startWatcher()

# https://live.douyin.com/webcast/im/fetch/
