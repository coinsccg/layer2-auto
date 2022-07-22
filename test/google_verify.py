# -*- coding: utf-8 -*-
import requests
import time

import time
import requests

""" 
YESCAPTCHA验证码DEMO Requests版本
目标网站 https://www.google.com/recaptcha/api2/demo
这是谷歌官方的演示
谷歌官方是reCaptcha V2
这里只是演示简单的处理
不同的网站需要针对性的提交
参考这个思路即可
不要生搬硬套
"""

# clientKey：在个人中心获取
clientKey = "084fec2a885c913e8094509a0cbb8661d2f02b654366"
# 目标参数：
websiteKey = "6LcKyLYbAAAAANM74ESqR5Q7Z_W2yolLdyK3fzFP"
# 目标参数：
websiteURL = "https://faucets.chain.link/rinkeby"
# 验证码类型：
task_type = "NoCaptchaTaskProxyless"


def create_task() -> str:
    """
    第一步，创建验证码任务
    :param
    :return taskId : string 创建成功的任务ID
    """
    url = "https://api.yescaptcha.com/createTask"
    data = {
        "clientKey": clientKey,
        "task": {
            "websiteURL": websiteURL,
            "websiteKey": websiteKey,
            "type": task_type
        }
    }
    try:
        # 发送JSON格式的数据
        result = requests.post(url, json=data, verify=False).json()
        taskId = result.get('taskId')
        if taskId is not None:
            return taskId
        print(result)

    except Exception as e:
        print(e)


def get_response(taskID: str):
    """
    第二步：使用taskId获取response
    :param taskID: string
    :return response: string 识别结果
    """

    # 循环请求识别结果，3秒请求一次
    times = 0
    while times < 120:
        try:
            url = f"https://api.yescaptcha.com/getTaskResult"
            data = {
                "clientKey": clientKey,
                "taskId": taskID
            }
            result = requests.post(url, json=data, verify=False).json()
            solution = result.get('solution', {})
            if solution:
                response = solution.get('gRecaptchaResponse')
                if response:
                    return response
            print(result)
        except Exception as e:
            print(e)

        times += 3
        time.sleep(3)


def verify_website(response):
    """
    第三步：提交给网站进行验证
    :param response: string
    :return html: string
    """
    url = "https://www.google.com/recaptcha/api2/userverify"
    data = {"g-recaptcha-response": response}
    r = requests.post(url, data=data)
    print(r.status_code, 11111111)
    if r.status_code == 200:
        return r.text


if __name__ == '__main__':
    taskId = create_task()
    print('创建任务:', taskId)
    if taskId is not None:
        response = get_response(taskId)
        print('识别结果:', response)
        result = verify_website(response)
        print('验证结果：', result)

