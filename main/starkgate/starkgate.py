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
            print("chromedriver����·������ȷ��")

    def website_connect(self, start_account: int):
        # metamaskǮ���л�����ʼ�˺�
        self.instance.change_account(start_account)

        # argentǮ���л�����ʼ�˺�
        self.instance.argent_change_account(start_account)
        time.sleep(3)

        # ͬ��Э��
        try:
            self.driver.get(self.URL)
            time.sleep(2)
            # ����localstorage
            self.driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);",
                                       "STARKGATE_ACCEPT_TERMS",
                                       "eyIwIjoiZEE9PSIsIjEiOiJjZz09IiwiMiI6ImRRPT0iLCIzIjoiWlE9PSJ9")

            self.driver.get(self.URL)

        except Exception as e:
            print(e)
            pass

        # ��¼metamask
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

        # ��¼argent
        try:
            time.sleep(2)
            self.driver.find_element(By.XPATH,
                                     '//*[@id="root"]/div/div[2]/div/div[1]/div[2]/div[1]/div/div/div[1]').click()
            time.sleep(2)
            self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div[1]/div/div[1]').click()
        except:
            pass

        # �رյ���
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
                # �л�����
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
                    self.instance.argent_approve_add_token()  # ����Ǯ�����eth
                except:
                    pass

                # �رյ���
                self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/button').click()

                # �Ͽ���վ
                try:
                    self.instance.breakoff_website(self.URL)
                except:
                    pass
                finally:
                    print(f"�˺�{n}�����ɣ�")
                time.sleep(5)

                if n >= end_account:
                    break

                # �л�����
                n += 1
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
            while 1:
                # �л�����
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

                # �Ͽ���վ
                try:
                    self.instance.breakoff_website(self.URL)
                except:
                    pass
                finally:
                    print(f"�˺�{n}ȡ����ɣ�")
                time.sleep(5)

                # �۳�����
                if not request_deduction_point(token):
                    print("���ֲ�������ǰ���������ĳ�ֵ!")
                    break

                if n >= end_account:
                    break

                # �л�����
                n += 1
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

    ab = StarkGate(deposit_num, withdraw_num)
    # ת��
    ab.deposit(int(start_account), int(end_account))

    print("ȫ���˺���ɴ� ��ȴ�5���ӣ����Զ�����ȡ�")

    time.sleep(300)

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
