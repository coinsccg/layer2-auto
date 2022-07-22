# -*- coding: gbk -*-
import sys
import re
import time
import requests
from auto_metamask.auto_metamask import *

PROJECT_ID = 1
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
            print("chromedriver����·������ȷ��")

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
        # �л����˺�1
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

    def withdraw(self, start_account: int, end_account: int):
        n = start_account
        try:
            while True:
                # �л�����ʼ�˺�
                self.instance.change_account(n)

                # ������վ
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

                # ��Ѻ
                self.driver.get('https://bridge.arbitrum.io/')

                if n == start_account:
                    WebDriverWait(self.driver, 200).until(EC.presence_of_element_located((By.XPATH,
                                                                                         '//*[@id="root"]/div/main/div/div/div[3]/div[1]/div[1]/div/div[1]/div[1]/div/span/div/span[1]')))
                    self.driver.find_element(By.XPATH,
                                             '//*[@id="root"]/div/main/div/div/div[3]/div[1]/div[2]/div/div/button').click()

                if n >= start_account + 1:
                    WebDriverWait(self.driver, 200).until(EC.presence_of_element_located((By.XPATH,
                                                                                         '//*[@id="root"]/div/main/div/div/div[3]/div[1]/div[3]/div/div[1]/div[1]/div/span/div/span[1]')))

                time.sleep(2)
                self.driver.find_element(By.XPATH,
                                         '//*[@id="root"]/div/main/div/div/div[3]/div[1]/div[3]/div/div[2]/div/input').send_keys(
                    self.withdraw_num)  # ��Ȩ

                time.sleep(3)
                self.driver.find_element(By.XPATH, '//button[text()="Withdraw"]').click()  # ��ȡ
                time.sleep(2)
                self.driver.find_element(By.XPATH, '//button[text()="MOVE FUNDS TO ETHEREUM"]').click()  # ��ȡ
                time.sleep(3)
                # �л�����
                try:
                    self.instance.approve_add_network()
                    time.sleep(10)
                except:
                    pass

                self.instance.confirm_approval_from_metamask()

                # �Ͽ���վ
                try:
                    self.instance.breakoff_website(self.URL)
                except:
                    pass
                finally:
                    print(f"�˺�{n}����ȡ��ɣ�")
                time.sleep(5)

                if n >= end_account:
                    break

                # �л��˺�
                n += 1
                self.instance.change_account(n)

        except:
            try:
                self.instance.breakoff_website(self.URL)
            except:
                pass

            if n < end_account:
                print("����ʧ����������������")
            else:
                print("�����˺�ȫ�������ȡ��")


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
                print("���������")
                return

            if len(withdraw_num) == 0:
                print("������ȡ���")
                return

            if len(token) == 0:
                print("������token��")
                return

            if len(start_account) == 0:
                print("�����뿪ʼ�˺ű�ţ�")
                return

            if len(end_account) == 0:
                print("����������˺ű�ţ�")
                return

    except:
        print("������contant.txt�����ļ���")
        return

    sre = re.compile(r'[A-Za-z]', re.S)
    res = re.findall(sre, deposit_num)
    if len(res) > 0:
        print("��������ȷ�Ĵ���")
        return

    sre = re.compile(r'[A-Za-z]', re.S)
    res = re.findall(sre, withdraw_num)
    if len(res) > 0:
        print("��������ȷ��ȡ���")
        return

    if not start_account.isdigit():
        print("��������ȷ���˺�����")
        return

    # У��token
    if not request_verify_token(token):
        print("tokenУ��ʧ�ܣ�")
        return

    # ��ȡchrome.bat�ļ�
    chrome = Chrome(exec_path, profi_path)
    chrome.exec_chrome_bat()

    ab = Arbitrum(deposit_num, withdraw_num)

    ab.login_metamask(password)
    ab.change_network("��̫�� Ethereum ������")
    # ȡ��
    ab.withdraw(int(start_account), int(end_account))

    print("�����˺������ɣ�")

    time.sleep(5)
    ab.close_chrome()


def request_verify_token(token: str) -> bool:
    try:
        headers = {'Content-Type': 'application/json'}
        json = {"verification": token}
        res = requests.post(VERIFY_RPC, headers=headers, json=json)
        return res.json()["status"]
    except:
        return False


if __name__ == '__main__':
    run()
