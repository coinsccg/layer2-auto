# -*- coding: gbk -*-
import re
import time
import requests
from auto_metamask.auto_metamask import *

PROJECT_ID = 4
VERIFY_RPC = "http://api.adpg.xyz/api/F_User/authorizationcodeverification"
SUB_POINT_RPC = "http://api.adpg.xyz/api/F_User/consumeIntegral"


class Chrome:
    def __init__(self, exec_path: str, profil_path: str):
        self.exec_path = exec_path
        self.profil_path = profil_path.replace("\Default", "", -1)

    def exec_chrome_bat(self):
        with open("./chrome.bat", "w") as f:
            f.write(f'"{self.exec_path}" --remote-debugging-port=9014 --user-data-dir="{self.profil_path}"')
        time.sleep(5)
        os.chdir(os.getcwd())
        os.popen("chrome.bat")


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

    def login_metamask(self, password: str):
        try:
            self.instance.login_metamask(password)
        except:
            pass

    def change_network(self, network: str):
        try:
            self.instance.change_network(network)
        except:
            pass

    def close_chrome(self):
        while True:
            self.driver.switch_to.window(self.driver.window_handles[0])
            self.driver.close()

    def website_connect(self, start_account: int):
        # 切换到账号1
        self.instance.change_account(start_account)
        time.sleep(3)

        try:
            self.driver.get(self.URL)
            self.driver.find_element(By.XPATH, '//*[@id="networkSelector"]').click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//*[@id="networkSelector"]/option[2]').click()
            self.driver.find_element(By.XPATH, '//*[@id="root"]/header/div[3]/div[2]/div[2]/button').click()
        except:
            pass

        try:
            time.sleep(2)
            self.instance.connect_to_website()
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//div[text()="MetaMask"]').click()
            time.sleep(2)
            self.instance.sign_confirm()
        except:
            pass

    def withdraw(self, start_account: int, end_account: int):
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

                # 交易
                self.driver.find_element(By.XPATH, '//*[@id="root"]/header/div[3]/div[1]/ul/li[1]/a').click()
                time.sleep(2)
                self.driver.find_element(By.XPATH,
                                         '//*[@id="root"]/div[1]/div/article/aside/div[4]/div/div[2]/div[1]/div/div[1]/span[2]').click()
                time.sleep(2)
                self.driver.find_element(By.XPATH,
                                         '//*[@id="root"]/div[1]/div/article/aside/div[4]/div/div[2]/div[1]/div/div[2]/form/div[3]/input').send_keys(self.withdraw_num)
                time.sleep(2)
                self.driver.find_element(By.XPATH,
                                         '//*[@id="root"]/div[1]/div/article/aside/div[4]/div/div[2]/div[1]/div/div[2]/form/div[5]/div[2]/button').click()
                time.sleep(2)
                self.instance.sign_confirm()

                # 断开网站
                try:
                    self.instance.breakoff_website(self.URL)
                except:
                    pass
                finally:
                    print(f"账号{n}，提取完成！")
                time.sleep(5)

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
            exec_path = str(reader[0]).rstrip("\n").split("=")[1]
            profi_path = str(reader[1]).rstrip("\n").split("=")[1]
            password = str(reader[2]).rstrip("\n").split("=")[1]
            deposit_num = str(reader[3]).rstrip("\n").split("=")[1]
            withdraw_num = str(reader[4]).rstrip("\n").split("=")[1]
            token = str(reader[5]).rstrip("\n").split("=")[1]
            start_account = str(reader[6]).rstrip("\n").split("=")[1]
            end_account = str(reader[7]).rstrip("\n").split("=")[1]
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

    # 获取chrome.bat文件
    chrome = Chrome(exec_path, profi_path)
    chrome.exec_chrome_bat()

    zg = Zigzag(deposit_num, withdraw_num)
    zg.login_metamask(password)
    zg.change_network("Rinkeby 测试网络")

    # 取款
    zg.withdraw(int(start_account), int(end_account))

    print("全部账号完成取款！")

    time.sleep(5)

    zg.close_chrome()


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
