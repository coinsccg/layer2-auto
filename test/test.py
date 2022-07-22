# -*- coding: gbk -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from auto_confirm_metamask import *
from google_verify import *
import time

# �ҵ�chrome��װλ�ã�C:\Program Files\Google\Chrome\Application����Ȼ��ִ��һ�������һ����ҳ
# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9527 --user-data-dir="C:\Users\chunde01\AppData\Local\Google\Chrome\User Data"

# options = Options()
# options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")

# chromeMetamask = webdriver.Chrome(options=options, executable_path="C:\chromedriver\chromedriver.exe")
# chrome = webdriver.Chrome(options=options, executable_path="C:\chromedriver\chromedriver.exe")

def run():
        # ���ò���
        instance = ChromAndMetamask("C:\chromedriver\chromedriver.exe")
        driver = instance.driver
        driver.get('https://testnet.phezzan.xyz/')
        # driver.get('https://faucets.chain.link/rinkeby')
        # �������Ǵ�
        seed = ["split ", "pink ", "warm ", "eye ", "uniform ", "express ", "virus ", "brief ", "benefit ", "unveil ",
                "action ", "monkey"]
        instance.metamask_setup(seed, "qf112290")
        networkName = 'Rinkeby ��������'
        # �л�����������
        pk = ""
        instance.change_metamask_network(networkName, pk)

        # ��վ����Ǯ��
        driver.switch_to.window(driver.window_handles[0])
        driver.find_element(By.XPATH, '//div[contains(@class, "css-xs1ht3")]//button').click()
        driver.switch_to.window(driver.window_handles[0])
        driver.find_element(By.XPATH, '//div[text()="Metamask"]').click()

        instance.connect_to_website()

        # ��Ѻ
        time.sleep(2)
        driver.find_element(By.XPATH, '//div[contains(@class, "css-1n5ssgg")]//button[1]').click()
        driver.switch_to.window(driver.window_handles[-1])
        driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-zcthtw")][2]').click()  # ��ȡUSDT
        instance.confirm_approval_from_metamask()
        driver.find_element(By.XPATH, '//div[contains(@class, "chakra-numberinput css-5eudyr")]/input').send_keys(
                "5000")  # ��Ȩ
        driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-vt9cpy")]').click()
        instance.confirm_approval_from_metamask()
        driver.find_element(By.XPATH, '//button[contains(@class, "chakra-modal__close-btn css-xipghn")]').click()  # �ر�

        # ����
        driver.get("https://testnet.phezzan.xyz/")
        time.sleep(5)
        driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-1x2v19b")]').click()
        driver.find_element(By.XPATH,
                            '//div[contains(@class,"css-vp1cdf")]//div[contains(@class, "chakra-linkbox css-thxllp")][1]').click()
        driver.find_element(By.XPATH,
                            '//div[contains(@class, "css-r4izcz")][2]//div[contains(@class, "chakra-numberinput css-5eudyr")]/input').send_keys(
                "200")
        driver.find_element(By.XPATH,
                            '//div[contains(@class, "chakra-stack css-1sigv9r")][1]/p[contains(@class, "chakra-text css-1ex7rpw")][1]').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-1vbn212")]').click()  # ȷ�Ͻ���
        instance.confirm_approval_from_metamask()

        # ���������
        driver.get("https://testnet.phezzan.xyz/")
        time.sleep(5)
        driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-1hsas4s")]').click()
        driver.find_element(By.XPATH,
                            '//div[contains(@class,"css-vp1cdf")]//div[contains(@class, "chakra-linkbox css-thxllp")][1]').click()
        driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-18huy1h")]').click()

        driver.switch_to.window(driver.window_handles[-1])
        driver.find_element(By.XPATH,
                            '//div[contains(@class, "css-r4izcz")][2]//div[contains(@class, "chakra-numberinput css-5eudyr")]/input').send_keys(
                "200")
        time.sleep(2)
        driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-1ukn01m")]').click()  # ȷ�����������
        instance.confirm_approval_from_metamask()

        time.sleep(2)
        driver.close()

if __name__ == '__main__':
    for i in range(10):
            run()


"""

# ��¼metamask
# ele = chromeMetamask.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
# delay = 1  # seconds
# try:
#     WebDriverWait(chromeMetamask, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
#
#     s_pass = "qf112290"
#     chromeMetamask.find_element(By.XPATH, '//*[@id="password"]').send_keys(s_pass)
#     chromeMetamask.find_element(By.XPATH, '//button[contains(@class, "button btn--rounded btn-default")]').click()
#     time.sleep(3)
# except Exception as e:
#     print(e)
#
# # ɾ��֮ǰ���˺�
# try:
#     chromeMetamask.find_element(By.XPATH, '//button[contains(@class, "fas fa-ellipsis-v menu-bar__account-options")]').click()
#     new_wind = chromeMetamask.window_handles[-1]  #�ҵ��µĴ���
#     chromeMetamask.switch_to.window(new_wind)
#     chromeMetamask.find_element(By.XPATH, '//button[contains(@class, "menu-item")][4]/span').click()
#     new_wind = chromeMetamask.window_handles[-1]  #�ҵ��µĴ���
#     chromeMetamask.switch_to.window(new_wind)
#     chromeMetamask.find_element(By.XPATH, '//button[contains(@class, "btn-primary")]').click()
# except Exception as e:
#     print(e)
#
#
# # ������˺�
# chromeMetamask.find_element(By.XPATH, '//div[contains(@class, "identicon__address-wrapper")]').click()
# new_wind = chromeMetamask.window_handles[-1]  #�ҵ��µĴ���
# chromeMetamask.switch_to.window(new_wind)
# chromeMetamask.find_element(By.XPATH, '//div[contains(@class, "account-menu__item account-menu__item--clickable")][2]/div[contains(@class, "account-menu__item__text")]').click()
# new_wind = chromeMetamask.window_handles[-1]  #�ҵ��µĴ���
# chromeMetamask.switch_to.window(new_wind)
# chromeMetamask.find_element(By.XPATH, '//div[contains(@class, "new-account-import-form__private-key-password-container")]/input').send_keys("")
# chromeMetamask.find_element(By.XPATH, '//button[contains(@class, "btn-primary")]').click()
#
# try:
#     # ��һ�μ�����վ
#     chrome.get("https://testnet.phezzan.xyz/")
#     time.sleep(2)
#     # ��վ�Զ��������metamask
#     chrome.find_element(By.XPATH, '//div[contains(@class, "css-xs1ht3")]//button').click()
#     new_wind = chrome.window_handles[-1]  # �ҵ��µĴ���
#     chrome.switch_to.window(new_wind)
#     chrome.find_element(By.XPATH, '//div[text()="Metamask"]').click()
#
#     # metamask�Զ�ȷ������
#     chromeMetamask.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/notification.html#connect/')
#     WebDriverWait(chromeMetamask, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@class="permissions-connect-header__subtitle"]')))
#     chromeMetamask.find_element(By.XPATH, '//button[contains(@class, "btn-primary")]').click() # ��һ��
#     chromeMetamask.find_element(By.XPATH, '//button[contains(@class, "btn-primary")]').click()  # ����
#
#     # Ǯ�����Ӻ����¼�����վ
#     chrome.get("https://testnet.phezzan.xyz/")
#     time.sleep(2)
#     chrome.find_element(By.XPATH, '//div[contains(@class, "css-xs1ht3")]//button').click()
#     new_wind = chrome.window_handles[-1]  # �ҵ��µĴ���
#     chrome.switch_to.window(new_wind)
#     chrome.find_element(By.XPATH, '//div[text()="Metamask"]').click()
# except Exception as e:
#     print(e)
"""
