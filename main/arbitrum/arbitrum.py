# -*- coding: gbk -*-
import re
import time
import requests
from auto_metamask.auto_metamask import *

PROJECT_ID = 1
VERIFY_RPC = "http://api.adpg.xyz/api/F_User/authorizationcodeverification"
SUB_POINT_RPC = "http://api.adpg.xyz/api/F_User/consumeIntegral"


class Arbitrum:
    URL = "https://bridge.arbitrum.io/"
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
            self.driver.find_element(By.XPATH, '//div[text()="MetaMask"]').click()
        except:
            pass

        try:
            time.sleep(3)
            self.instance.connect_to_website()
            time.sleep(3)
            self.driver.find_element(By.XPATH, '//*[@id="headlessui-dialog-5"]/div/div[2]/div[2]/button').click()
        except:
            pass

    def deposit(self, start_account: int, end_account: int):
        n = start_account
        try:
            while True:
                if n >= start_account + 1:
                    # 切换网络
                    self.driver.get('https://bridge.arbitrum.io/')
                    try:
                        time.sleep(3)
                        self.instance.connect_to_website()
                    except:
                        pass

                # 质押
                self.driver.get('https://bridge.arbitrum.io/')
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/main/div/div/div[3]/div[1]/div[1]/div/div[1]/div[1]/div/span/div/span[1]')))
                self.driver.find_element(By.XPATH,
                                         '//*[@id="root"]/div/main/div/div/div[3]/div[1]/div[1]/div/div[2]/div/input').send_keys(
                    self.deposit_num)  # 授权
                time.sleep(3)
                self.driver.find_element(By.XPATH, '//button[text()="Deposit"]').click()  # 质押
                time.sleep(4)
                self.driver.find_element(By.XPATH, '//button[text()="MOVE FUNDS TO ARBITRUM"]').click()  # 质押
                time.sleep(3)
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
                # 切换到开始账号
                self.instance.change_account(n)

                # 连接网站
                try:
                    self.driver.get(self.URL)
                    self.driver.find_element(By.XPATH, '//div[text()="MetaMask"]').click()
                except:
                    pass

                try:
                    time.sleep(3)
                    self.instance.connect_to_website()
                except:
                    pass

                # 质押
                self.driver.get('https://bridge.arbitrum.io/')

                if n == 1:
                    WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH,
                                                                                         '//*[@id="root"]/div/main/div/div/div[3]/div[1]/div[1]/div/div[1]/div[1]/div/span/div/span[1]')))
                    self.driver.find_element(By.XPATH,
                                             '//*[@id="root"]/div/main/div/div/div[3]/div[1]/div[2]/div/div/button').click()

                if n >= 2:
                    WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH,
                                                                                     '//*[@id="root"]/div/main/div/div/div[3]/div[1]/div[3]/div/div[1]/div[1]/div/span/div/span[1]')))

                time.sleep(2)
                self.driver.find_element(By.XPATH,
                                         '//*[@id="root"]/div/main/div/div/div[3]/div[1]/div[3]/div/div[2]/div/input').send_keys(
                    self.withdraw_num)  # 授权

                time.sleep(5)
                self.driver.find_element(By.XPATH, '//button[text()="Withdraw"]').click()  # 提取
                time.sleep(4)
                self.driver.find_element(By.XPATH, '//button[text()="MOVE FUNDS TO ETHEREUM"]').click()  # 提取

                time.sleep(3)
                # 切换网络
                try:
                    self.instance.approve_add_network()
                    WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH,
                                                                                         '//*[@id="root"]/div/main/div/div/div[3]/div[1]/div[3]/div/div[1]/div[1]/div/span/div/span[1]')))

                    time.sleep(10)
                except:
                    pass

                self.instance.confirm_approval_from_metamask()

                # 断开网站
                try:
                    self.instance.breakoff_website(self.URL)
                except:
                    pass
                finally:
                    print(f"账号{n}，提取完成！")
                time.sleep(5)

                # 扣除积分
                if not request_deduction_point(token):
                    print("积分不够，请前往个人中心充值!")
                    break

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
    if not request_verify_token(token):
        print("token校验失败！")
        return

    ab = Arbitrum(deposit_num, withdraw_num)
    ab.website_connect(int(start_account))

    # 存款
    ab.deposit(int(start_account), int(end_account))

    print("全部账号完成存款， 请等待10分钟，将自动进行取款！")

    time.sleep(600)

    # 取款
    ab.withdraw(int(start_account), int(end_account), token)


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
