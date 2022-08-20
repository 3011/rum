import time
import requests
import random


url = "http://localhost:8000/"


def performance():
    # post
    time_list = ["DNSTime", "connectTime", "ttfbTime", "responseTime", "parseDOMTime", "DOMReady", "domContentLoadedTime",
                 "timeToInteractive", "loadTime", "firstPaint", "firstContentPaint", "firstMeaningfulPaint", "largestContentfulPaint"]
    url_list = ["http://localhost:8080/", "http://www.google.com/"]
    ua_list = [{
        "full": "User-Agent:Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "name": "Safari",
        "version": "534.50",
        "fullName": "Safari 534.50",
        "os": "Intel Mac OS X 10_6_8"
    }, {
        "full": "User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "name": "Chrome",
        "version": "39.0.2171.95",
        "fullName": "Chrome 39.0.2171.95",
        "os": "Windows NT 6.1"
    }, {
        "full": "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "name": "Firefox",
        "version": "4.0.1",
        "fullName": "Firefox 4.0.1",
        "os": "Macintosh; Intel Mac OS X 10.6"
    }]
    body = {
        "title": "monitor-SDK",
        "url": random.choice(url_list),
        "timestamp": time.time()*1000,
        "userAgent": random.choice(ua_list),
        "kind": "experience",
        "type": "timing",
    }
    for i in time_list:
        body[i] = random.randint(0, 200)

    requests.post(url+"api/post_err", json=body)


def errors():
    body = {
        "title": "前端监控系统",
        "url": "https://apple.com/",
        "timestamp": "1760472173899",
        "userAgent": {
            "full": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "name": "chrome",
            "version": "103.0.0.0",
            "fullName": "chrome 103.0.0.0",
            "os": ""
        },
        "kind": "stability",
        "type": "error",
        "errorType": "jsError",
        "message": "Uncaught TypeError: Cannot set property 'error' of undefined",
        "filename": "http://localhost:8080/",
        "position": "0:0",
        "stack": "btnClick (http://localhost:8080/:20:39)^HTMLInputElement.onclick (http://localhost:8080/:14:72)",
        "selector": "HTML BODY #container .content INPUT"
    }

    requests.post(url+"api/post_err", json=body)


def main():

    while True:
        r = random.random()
        if r < 0.7:
            performance()
        else:
            errors()
        # time.sleep(r*15)


main()
