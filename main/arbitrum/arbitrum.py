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
            print("chromedriver����·������ȷ��")

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

    def deposit(self, start_account: int, end_account: int):
        n = start_account
        try:
            while True:
                if n >= start_account + 1:
                    # �л�����
                    self.driver.get('https://bridge.arbitrum.io/')
                    try:
                        time.sleep(3)
                        self.instance.connect_to_website()
                    except:
                        pass

                # ��Ѻ
                self.driver.get('https://bridge.arbitrum.io/')
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/main/div/div/div[3]/div[1]/div[1]/div/div[1]/div[1]/div/span/div/span[1]')))
                self.driver.find_element(By.XPATH,
                                         '//*[@id="root"]/div/main/div/div/div[3]/div[1]/div[1]/div/div[2]/div/input').send_keys(
                    self.deposit_num)  # ��Ȩ
                time.sleep(3)
                self.driver.find_element(By.XPATH, '//button[text()="Deposit"]').click()  # ��Ѻ
                time.sleep(4)
                self.driver.find_element(By.XPATH, '//button[text()="MOVE FUNDS TO ARBITRUM"]').click()  # ��Ѻ
                time.sleep(3)
                self.instance.confirm_approval_from_metamask()

                # �Ͽ���վ
                try:
                    self.instance.breakoff_website(self.URL)
                except:
                    pass
                finally:
                    print(f"�˺�{n}����Ѻ��ɣ�")
                time.sleep(5)

                if n >= end_account:
                    break

                # �л�����
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
                print("�����˺�ȫ�������Ѻ��")

    def withdraw(self, start_account: int, end_account: int, token: str):
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
                    self.withdraw_num)  # ��Ȩ

                time.sleep(5)
                self.driver.find_element(By.XPATH, '//button[text()="Withdraw"]').click()  # ��ȡ
                time.sleep(4)
                self.driver.find_element(By.XPATH, '//button[text()="MOVE FUNDS TO ETHEREUM"]').click()  # ��ȡ

                time.sleep(3)
                # �л�����
                try:
                    self.instance.approve_add_network()
                    WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH,
                                                                                         '//*[@id="root"]/div/main/div/div/div[3]/div[1]/div[3]/div/div[1]/div[1]/div/span/div/span[1]')))

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

                # �۳�����
                if not request_deduction_point(token):
                    print("���ֲ�������ǰ���������ĳ�ֵ!")
                    break

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
            deposit_num = str(reader[0]).rstrip("\n").split("=")[1]
            withdraw_num = str(reader[1]).rstrip("\n").split("=")[1]
            token = str(reader[2]).rstrip("\n").split("=")[1]
            start_account = str(reader[3]).rstrip("\n").split("=")[1]
            end_account = str(reader[4]).rstrip("\n").split("=")[1]
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
        print("��������ȷ�Ĵ���ȡ���token��")
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

    ab = Arbitrum(deposit_num, withdraw_num)
    ab.website_connect(int(start_account))

    # ���
    ab.deposit(int(start_account), int(end_account))

    print("ȫ���˺���ɴ� ��ȴ�10���ӣ����Զ�����ȡ�")

    time.sleep(600)

    # ȡ��
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
