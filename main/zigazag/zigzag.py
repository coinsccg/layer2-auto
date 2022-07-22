# -*- coding: gbk -*-
import re
import time
import requests
from auto_metamask.auto_metamask import *

PROJECT_ID = 4
VERIFY_RPC = "http://api.adpg.xyz/api/F_User/authorizationcodeverification"
SUB_POINT_RPC = "http://api.adpg.xyz/api/F_User/consumeIntegral"


class Zigzag:
    URL = "https://trade.zigzag.exchange/bridge"
    chrome_driver_path = "./tool/chrome/chromedriver.exe"

    def __init__(self, deposit_num, withdraw_num):
        self.deposit_num = deposit_num
        self.withdraw_num = withdraw_num

        try:
            self.instance = ChromAndMetamask(self.chrome_driver_path)
            self.driver = self.instance.driver
        except:
            print("chromedriver驱动路径不正确！")

    def website_connect(self, start_account: int):
        # 切换到账号1
        self.instance.change_account(start_account)
        time.sleep(3)

        try:
            self.driver.get(self.URL)
            self.driver.find_element(By.XPATH, '//*[@id="root"]/header/div[3]/div[2]/div[2]/button').click()
        except:
            pass

        try:
            time.sleep(3)
            self.instance.connect_to_website()
            time.sleep(3)
            self.driver.find_element(By.XPATH, '//div[text()="MetaMask"]').click()
            self.instance.sign_confirm()
        except:
            pass

    def deposit(self, start_account: 1, end_account: int):
        n = start_account
        try:
            while True:
                if n >= start_account + 1:
                    # 切换网络
                    self.driver.get(self.URL)
                    try:
                        time.sleep(3)
                        self.website_connect(n)
                    except:
                        pass

                # 质押
                self.driver.get(self.URL)
                try:
                    self.driver.find_element(By.XPATH, '//*[@id="root"]/header/div[3]/div[2]/div[2]/button').click()
                    time.sleep(2)
                    self.driver.find_element(By.XPATH, '//div[text()="MetaMask"]').click()
                    self.instance.sign_confirm()
                except:
                    pass
                time.sleep(3)
                while True:
                    text = self.driver.find_element(By.XPATH,
                                                    '//*[@id="root"]/div[1]/div/div[2]/div[1]/div[1]/div[3]/div[2]/span').text.split(
                        " ")
                    if float(text[0]) > 0:
                        break
                time.sleep(3)
                self.driver.find_element(By.XPATH,
                                         '//*[@id="root"]/div[1]/div/div[2]/div[1]/div[1]/div[2]/input').send_keys(
                    self.deposit_num)  # 授权
                time.sleep(3)

                text = self.driver.find_element(By.XPATH,
                                                '//*[@id="root"]/div[1]/div/div[2]/div[1]/div[2]/div[5]/button/span').text
                if text == "Must be more than Infinity ETH":
                    while True:
                        self.driver.get(self.URL)
                        try:
                            self.driver.find_element(By.XPATH,
                                                     '//*[@id="root"]/header/div[3]/div[2]/div[2]/button').click()
                            time.sleep(2)
                            self.driver.find_element(By.XPATH, '//div[text()="MetaMask"]').click()
                        except:
                            pass
                        time.sleep(3)
                        while True:
                            text = self.driver.find_element(By.XPATH,
                                                            '//*[@id="root"]/div[1]/div/div[2]/div[1]/div[1]/div[3]/div[2]/span').text.split(
                                " ")
                            if float(text[0]) > 0:
                                break
                        time.sleep(3)
                        self.driver.find_element(By.XPATH,
                                                 '//*[@id="root"]/div[1]/div/div[2]/div[1]/div[1]/div[2]/input').send_keys(
                            self.deposit_num)  # 授权
                        time.sleep(3)
                        text = self.driver.find_element(By.XPATH,
                                                        '//*[@id="root"]/div[1]/div/div[2]/div[1]/div[2]/div[5]/button/span').text
                        if text != "Must be more than Infinity ETH":
                            break

                self.driver.find_element(By.XPATH,
                                         '//*[@id="root"]/div[1]/div/div[2]/div[1]/div[2]/div[5]/button').click()  # 存款
                time.sleep(4)

                # 确认交易
                self.instance.confirm_approval_from_metamask()

                # 断开网站
                try:
                    self.instance.breakoff_website(self.URL)
                except:
                    pass
                finally:
                    print(f"账号{n}，质押完成！")
                time.sleep(5)

                if n >= end_account:
                    break

                # 切换网络
                n += 1
                self.instance.change_account(n)
        except:
            try:
                self.instance.breakoff_website(self.URL)
            except:
                pass

            if n < end_account:
                print("运行失败请重新启动程序！")
            else:
                print("所有账号全部完成质押！")

    def withdraw(self, start_account: int, end_account: int, token: str):
        n = start_account
        try:
            while True:
                # 切换网络
                self.driver.get(self.URL)
                try:
                    time.sleep(3)
                    self.website_connect(n)
                except:
                    pass

                # 质押
                self.driver.get(self.URL)
                try:
                    self.driver.find_element(By.XPATH, '//*[@id="root"]/header/div[3]/div[2]/div[2]/button').click()
                    time.sleep(2)
                    self.driver.find_element(By.XPATH, '//div[text()="MetaMask"]').click()
                    self.instance.sign_confirm()
                except:
                    pass
                time.sleep(3)

                self.driver.find_element(By.XPATH,
                                         '//*[@id="root"]/div[1]/div/div[2]/div[1]/div[2]/div[1]/button').click()
                time.sleep(2)
                self.driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div/div[2]/div[1]/div[1]/div[2]/a').click()
                time.sleep(2)
                self.driver.find_element(By.XPATH,
                                         '//*[@id="root"]/div[1]/div/div[2]/div[1]/div[2]/div[5]/button').click()
                time.sleep(3)
                self.instance.sign_confirm()

                # 断开网站
                try:
                    self.instance.breakoff_website(self.URL)
                except:
                    pass
                finally:
                    print(f"账号{n}，提取完成！")
                time.sleep(5)

                # 扣除积分
                # if not request_deduction_point(token):
                #     print("积分不够，请前往个人中心充值!")
                #     break

                if n >= end_account:
                    break

                # 切换账号
                n += 1
                self.instance.change_account(n)

        except:
            try:
                self.instance.breakoff_website(self.URL)
            except:
                pass

            if n < end_account:
                print("运行失败请重新启动程序！")
            else:
                print("所有账号全部完成提取！")


def run():
    try:
        with open("./constant.txt", "r") as f:
            reader = f.readlines()
            deposit_num = str(reader[0]).rstrip("\n").split("=")[1]
            withdraw_num = str(reader[1]).rstrip("\n").split("=")[1]
            token = str(reader[2]).rstrip("\n").split("=")[1]
            start_account = str(reader[3]).rstrip("\n").split("=")[1]
            end_account = str(reader[4]).rstrip("\n").split("=")[1]
            if len(deposit_num) == 0:
                print("请输入存款金额！")
                return

            if len(withdraw_num) == 0:
                print("请输入取款金额！")
                return

            if len(token) == 0:
                print("请输入token！")
                return

            if len(start_account) == 0:
                print("请输入开始账号编号！")
                return

            if len(end_account) == 0:
                print("请输入结束账号编号！")
                return

    except:
        print("请输入正确的存款金额、取款金额、token！")
        return

    sre = re.compile(r'[A-Za-z]', re.S)
    res = re.findall(sre, deposit_num)
    if len(res) > 0:
        print("请输入正确的存款金额！")
        return

    sre = re.compile(r'[A-Za-z]', re.S)
    res = re.findall(sre, withdraw_num)
    if len(res) > 0:
        print("请输入正确的取款金额！")
        return

    if not start_account.isdigit():
        print("请输入正确的账号数！")
        return

    # 校验token
    # if not request_verify_token(token):
    #     print("token校验失败！")
    #     return

    zg = Zigzag(deposit_num, withdraw_num)
    # zg.website_connect(int(start_account))

    # 存款
    # zg.deposit(int(start_account), int(end_account))
    #
    print("全部账号完成存款， 请等待10分钟，将自动进行取款！")

    # time.sleep(600)

    # 取款
    zg.withdraw(int(start_account), int(end_account), token)


def request_verify_token(token: str) -> bool:
    try:
        headers = {'Content-Type': 'application/json'}
        json = {"verification": token}
        res = requests.post(VERIFY_RPC, headers=headers, json=json)
        return res.json()["status"]
    except:
        return False


def request_deduction_point(token: str) -> bool:
    try:
        headers = {'Content-Type': 'application/json'}
        json = {"verification": token, "pid": PROJECT_ID}
        res = requests.post(SUB_POINT_RPC, headers=headers, json=json)
        return res.json()["status"]
    except:
        return False


if __name__ == '__main__':
    run()
