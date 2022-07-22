# -*- coding: gbk -*-
import re
import time
import requests
from auto_metamask.auto_metamask import *

PROJECT_ID = 3
VERIFY_RPC = "http://api.adpg.xyz/api/F_User/authorizationcodeverification"
SUB_POINT_RPC = "http://api.adpg.xyz/api/F_User/consumeIntegral"


class StarkGate:
    URL = "https://goerli.starkgate.starknet.io/"
    # URL = "https://starkgate.starknet.io/"
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
        # metamask钱包切换到开始账号
        self.instance.change_account(start_account)

        # argent钱包切换到开始账号
        self.instance.argent_change_account(start_account)
        time.sleep(3)

        # 同意协议
        try:
            self.driver.get(self.URL)
            time.sleep(2)
            # 设置localstorage
            self.driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);",
                                       "STARKGATE_ACCEPT_TERMS",
                                       "eyIwIjoiZEE9PSIsIjEiOiJjZz09IiwiMiI6ImRRPT0iLCIzIjoiWlE9PSJ9")

            self.driver.get(self.URL)

        except Exception as e:
            print(e)
            pass

        # 登录metamask
        try:
            self.driver.find_element(By.XPATH,
                                     '//*[@id="root"]/div/div[2]/div/div[1]/div[2]/div[1]/div/div/div[1]').click()
        except:
            pass

        try:
            time.sleep(3)
            self.instance.connect_to_website()
            time.sleep(3)
            self.driver.find_element(By.XPATH, '//*[@id="headlessui-dialog-5"]/div/div[2]/div[2]/button').click()
        except:
            pass

        # 登录argent
        try:
            time.sleep(2)
            self.driver.find_element(By.XPATH,
                                     '//*[@id="root"]/div/div[2]/div/div[1]/div[2]/div[1]/div/div/div[1]').click()
            time.sleep(2)
            self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div[1]/div/div[1]').click()
        except:
            pass

        # 关闭弹窗
        try:
            time.sleep(2)
            self.driver.find_element(By.XPATH,
                                     '/html/body/div[2]/div/div[3]/button').click()
        except:
            pass

    def deposit(self, start_account: int, end_account: int):
        n = start_account
        try:
            while 1:
                # 切换网络
                try:
                    self.website_connect(n)
                except:
                    pass

                # ethereum -> starknet
                time.sleep(2)
                text = self.driver.find_element(By.XPATH,
                                                '//*[@id="root"]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div').text.split(
                    "\n")
                while True:
                    if len(text) > 1:
                        break
                    text = self.driver.find_element(By.XPATH,
                                                    '//*[@id="root"]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div').text.split(
                        "\n")

                self.driver.find_element(By.XPATH,
                                         '//*[@id="root"]/div/div[2]/div/div/div[2]/div/div[2]/div[3]/div/input').send_keys(
                    self.deposit_num)
                time.sleep(2)
                self.driver.find_element(By.XPATH,
                                         '//*[@id="root"]/div/div[2]/div/div/div[2]/div/div[2]/div[3]/button').click()
                time.sleep(2)

                self.instance.confirm_approval_from_metamask()
                WebDriverWait(self.driver, 300).until(EC.presence_of_element_located((By.XPATH,
                                                                                      '/html/body/div[2]/div/div[3]/button')))
                try:
                    time.sleep(5)
                    self.instance.argent_approve_add_token()  # 初次钱包添加eth
                except:
                    pass

                # 关闭弹窗
                self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/button').click()

                # 断开网站
                try:
                    self.instance.breakoff_website(self.URL)
                except:
                    pass
                finally:
                    print(f"账号{n}存款完成！")
                time.sleep(5)

                if n >= end_account:
                    break

                # 切换网络
                n += 1
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
            while 1:
                # 切换网络
                try:
                    self.website_connect(n)
                except:
                    pass

                # startknet -> ethereum
                time.sleep(3)
                self.driver.find_element(By.XPATH,
                                         '//*[@id="root"]/div/div[2]/div/div/div[2]/div/div[1]/div[2]').click()

                time.sleep(3)
                self.driver.find_element(By.XPATH,
                                         '//*[@id="root"]/div/div[2]/div/div/div[2]/div/div[2]/div[3]/div/input').send_keys(
                    self.withdraw_num)

                self.driver.find_element(By.XPATH,
                                         '//*[@id="root"]/div/div[2]/div/div/div[2]/div/div[2]/div[3]/button').click()

                self.instance.confirm_approval_from_argent()
                WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH,
                                                                                      '/html/body/div[2]/div/div[3]/button')))

                # 断开网站
                try:
                    self.instance.breakoff_website(self.URL)
                except:
                    pass
                finally:
                    print(f"账号{n}取款完成！")
                time.sleep(5)

                # 扣除积分
                if not request_deduction_point(token):
                    print("积分不够，请前往个人中心充值!")
                    break

                if n >= end_account:
                    break

                # 切换网络
                n += 1
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

    ab = StarkGate(deposit_num, withdraw_num)
    # 转账
    ab.deposit(int(start_account), int(end_account))

    print("全部账号完成存款， 请等待5分钟，将自动进行取款！")

    time.sleep(300)

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
