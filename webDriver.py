import uuid
import xpath
import os
import requests as requests
from playwright.sync_api import sync_playwright as playwright

roomId = 73726076014

#pip install 'protobuf~=3.19.0'


def getScriptDir():
    return os.path.split(os.path.realpath(__file__))[0]


def filterResponse(response):
    if 'https://live.douyin.com/webcast/im/fetch/' in response.url:
        # print("<<", response.url)
        with open('./douyinLiveFile/' + uuid.uuid4().hex, 'wb') as file:
            #lock.acquire()  # 加锁
            file.write(response.body())
            #lock.release()  # 释放锁
    else:
        # print("--", response.url)
        pass
    return response


def log_request(intercepted_request):
    print("a request was made:", intercepted_request.url)


def run(pw):
    browser = pw.webkit.launch(headless=True)
    page = browser.new_page()

    page.on("response", filterResponse)
    # 直播间地址
    page.goto(f"https://live.douyin.com/{roomId}")
    return page


def downloadImg(url, path):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        open(path, 'wb').write(r.content) # 将内容写入图片
        print(f"CODE: {r.status_code} download {url} to {path}") # 返回状态码
        r.close()
        return path
    else:
        print(f"CODE: {r.status_code} download {url} Failed.")
        return "error"


def startMonitoring():
    print("playwright")
    myi = 0
    with playwright() as pw:
        print(f"run {myi} times")
        page = run(pw)
        #直播间停留时间 单位ms 需要你们自己敲定  也可以永久驻留
        print("wait_for_timeout")
        page.wait_for_timeout(100000000)


if __name__ == '__main__':
    xpath.mkdir('./douyinLiveFile/')
    xpath.mkdir('./userImages/')
    print("startMonitoring")
    startMonitoring()

# https://live.douyin.com/webcast/im/fetch/
