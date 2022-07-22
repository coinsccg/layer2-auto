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


class SynFutures:
    URL = "https://v2-testnet.synfutures.com/usd/trade"
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
            time.sleep(3)
            self.driver.find_element(By.XPATH,
                                     '//*[@id="root"]/div/div/section/div/header/div/div[2]/button[2]/span').click()
            time.sleep(1)
            self.driver.find_element(By.XPATH,
                                     '/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div').click()
            time.sleep(1)
            self.instance.connect_to_website()
        except:
            pass

    def deposit(self, start_account: 1, end_account: int, token: str):
        n = start_account
        try:
            while True:
                if n >= start_account + 1:
                    # �л��˺�
                    try:
                        time.sleep(3)
                        self.website_connect(n)
                    except:
                        pass

                # �������
                self.driver.find_element(By.XPATH,
                                         '//*[@id="root"]/div/div/section/div/header/div/div[2]/button[1]/span').click()
                time.sleep(1)
                self.driver.find_element(By.XPATH,
                                         '/html/body/div[2]/div/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[4]/div[2]/a[1]').click()
                time.sleep(2)
                # Ǯ��ȷ���������
                self.instance.confirm_approval_from_metamask()

                # �ȴ����ҵ���
                while True:
                    text = self.driver.find_element(By.XPATH,
                                                    '/html/body/div[2]/div/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[4]/div[1]/div[2]/span').text
                    if text != "0.0000":
                        break

                # ����eth/usdc
                self.driver.get(
                    "https://v2-testnet.synfutures.com/usd/trade/0x33c78bb3dbe5ceb91d7b7e2b690aa4ea3c139f53/0")

                # ѡ����
                self.driver.find_element(By.XPATH,
                                         '//*[@id="root"]/div/div/section/main/div/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/form/div[2]/div/div/div[1]/div[3]/div/div/div/dl/dd/div[1]/div/button').click()

                self.driver.find_element(By.XPATH,
                                         '//*[@id="root"]/div/div/section/main/div/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/form/div[2]/div/div/div[1]/div[3]/div/div/div/div/div/div/div/div/div[4]/span').click()

                # ����eth
                self.driver.find_element(By.XPATH,
                                         '//*[@id="root"]/div/div/section/main/div/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/form/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div/span/input').send_keys(0.5)
                time.sleep(2)
                self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/section/main/div/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/form/div[2]/div/div/div[2]/button/span').click()

                # ȷ�Ϲ���
                self.instance.confirm_approval_from_metamask()

                # ��ӳ���
                self.driver.get('https://v2-testnet.synfutures.com/usd/pool/0x33c78bb3dbe5ceb91d7b7e2b690aa4ea3c139f53/1656057600')
                self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/section/main/div/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/form/div[2]/div/div/div[1]/div/div/div[2]/div/div/span/input').send_keys(1000)
                self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/section/main/div/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/form/div[2]/div/div/div[2]/button').click()
                WebDriverWait(self.driver, 300).until(EC.presence_of_element_located((By.XPATH,
                                                                                      '//*[@id="root"]/div/div/section/main/div/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/form/div[1]/div[2]')))

                self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/section/main/div/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/form/div[1]/div[2]').click()
                self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/section/main/div/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/form/div[2]/div/div/div[1]/div[2]/div[1]/div[1]/div[1]').click()


                self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/section/main/div/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/form/div[2]/div/div/div[2]/button').click()
                # ȷ�Ϸ���
                self.instance.confirm_approval_from_metamask()

                # �Ͽ���վ
                try:
                    self.instance.breakoff_website(self.URL)
                except:
                    pass
                finally:
                    print(f"�˺�{n}������ɣ�")
                time.sleep(5)

                # if not request_deduction_point(token):
                #     print("���ֲ�������ǰ���������ĳ�ֵ!")
                #     break

                if n >= end_account:
                    break

                # �л��˺�
                n += 1
        except:
            try:
                self.instance.breakoff_website(self.URL)
            except:
                pass

            if n < end_account:
                print("����ʧ����������������")
            else:
                print("�����˺�ȫ�����")


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
    # if not request_verify_token(token):
    #     print("tokenУ��ʧ�ܣ�")
    #     return

    # ��ȡchrome.bat�ļ�
    chrome = Chrome(exec_path, profi_path)
    chrome.exec_chrome_bat()

    ob = SynFutures(deposit_num, withdraw_num)
    ob.login_metamask(password)
    ob.change_network("Kovan ��������")
    ob.website_connect(int(start_account))

    # ���
    ob.deposit(int(start_account), int(end_account), token)

    print("ȫ���˺���ɴ� ��ȴ�10���ӣ����Զ�����ȡ�")

    time.sleep(5)
    ob.close_chrome()


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
