# -*- coding: gbk -*-
import re
import time
import requests
from auto_metamask.auto_metamask import *
from selenium.webdriver.common.by import By


class Phezzan:
    URL = "https://testnet.phezzan.xyz/"
    chrome_driver_path = "\\tool\chrome\chromedriver.exe"

    def __init__(self):
        try:
            self.instance = ChromAndMetamask(self.chrome_driver_path)
            self.driver = self.instance.driver
        except:
            print("chromedriver驱动路径不正确！")

    def connect_website(self, n: int) -> None:
        try:
            # 切换到账号1
            self.instance.change_account(n)
            # 切换网络
            self.instance.change_network("Rinkeby 测试网络")
            time.sleep(3)
            self.driver.get('https://testnet.phezzan.xyz/')
            time.sleep(3)
            self.driver.find_element(By.XPATH, '//button[text()="Connect Wallet"]').click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//div[text()="Metamask"]').click()

            self.instance.connect_to_website()
        except Exception as e:
            print(e)

    def claim_usdt(self) -> None:
        time.sleep(2)

        while True:
            text = self.driver.find_element(By.XPATH,
                                            '//*[@id="root"]/div/div[2]/div/div[1]/div/div[1]/div[2]/div/div/div[3]/div[1]/div/p').text
            if text != "$-,---":
                break
        self.driver.find_element(By.XPATH, '//button[text()="Deposit"]').click()
        time.sleep(2)
        self.driver.find_element(By.XPATH,
                                 '//button[text()="Claim aUST"]').click()  # 领取USDT
        time.sleep(3)
        self.instance.confirm_approval_from_metamask()
        time.sleep(20)

    def approve_deposit(self) -> None:
        n = 0
        while n < 2:
            self.driver.get('https://testnet.phezzan.xyz/')
            time.sleep(5)
            self.driver.find_element(By.XPATH, '//div[contains(@class, "css-1n5ssgg")]//button[1]').click()
            time.sleep(2)
            self.driver.find_element(By.XPATH,
                                     '//*[@id="chakra-modal--body-18"]/div/div[2]/input').send_keys(
                "50000")  # 授权
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//div[contains(@class, "chakra-stack css-1mslgq2")]/p').click()
            time.sleep(1)

            self.driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-vt9cpy")]').click()

            time.sleep(2)
            self.instance.confirm_approval_from_metamask()
            self.driver.find_element(By.XPATH,
                                     '//button[contains(@class, "chakra-modal__close-btn css-xipghn")]').click()
            time.sleep(5)
            n += 1

    def withdraw_usdt(self) -> None:
        self.driver.get('https://testnet.phezzan.xyz/')
        time.sleep(5)
        self.driver.find_element(By.XPATH, '//div[contains(@class, "css-1n5ssgg")]//button[2]').click()
        self.driver.find_element(By.XPATH, '//div[contains(@class, "chakra-numberinput css-5eudyr")]/input').send_keys(
            "100")  # 授权
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//div[contains(@class, "chakra-stack css-o5l3sd")]/p').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-1enp6rw")]').click()
        time.sleep(5)
        self.instance.confirm_approval_from_metamask()
        time.sleep(2)
        self.driver.find_element(By.XPATH,
                                 '//button[contains(@class, "chakra-modal__close-btn css-xipghn")]').click()  # 关闭

    def trade(self) -> None:
        self.driver.get("https://testnet.phezzan.xyz/")
        time.sleep(10)
        self.driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-1x2v19b")]').click()
        self.driver.find_element(By.XPATH,
                                 '//div[contains(@class,"css-vp1cdf")]//div[contains(@class, "chakra-linkbox css-thxllp")][1]').click()
        self.driver.find_element(By.XPATH,
                                 '//div[contains(@class, "css-r4izcz")][2]//div[contains(@class, "chakra-numberinput css-5eudyr")]/input').send_keys(
            "100")

        time.sleep(2)
        self.driver.find_element(By.XPATH,
                                 '//div[contains(@class, "chakra-stack css-1sigv9r")][1]/p[contains(@class, "chakra-text css-1ex7rpw")][1]').click()
        time.sleep(5)
        self.driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-1vbn212")]').click()  # 确认交易
        time.sleep(5)
        self.instance.confirm_approval_from_metamask()
        time.sleep(10)

    def close_position(self) -> None:
        self.driver.get("https://testnet.phezzan.xyz/")
        time.sleep(5)
        self.driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-1x2v19b")]').click()
        self.driver.find_element(By.XPATH,
                                 '//div[contains(@class,"css-vp1cdf")]//div[contains(@class, "chakra-linkbox css-thxllp")][1]').click()
        time.sleep(10)
        self.driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-o31yjj")]').click()
        time.sleep(3)
        self.driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-1qeu6q2")]').click()
        time.sleep(3)
        self.instance.confirm_approval_from_metamask()
        self.driver.find_element(By.XPATH, '//button[contains(@class, "chakra-modal__close-btn css-xipghn")]').click()

    def add_liquidity(self, n: int) -> None:
        self.driver.get("https://testnet.phezzan.xyz/")
        time.sleep(5)
        self.driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-1hsas4s")]').click()
        time.sleep(2)
        self.driver.find_element(By.XPATH,
                                 '//div[contains(@class,"css-vp1cdf")]//div[contains(@class, "chakra-linkbox css-thxllp")][1]').click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-18huy1h")]').click()
        time.sleep(2)
        self.driver.find_element(By.XPATH,
                                 '//div[contains(@class, "css-r4izcz")][2]//div[contains(@class, "chakra-numberinput css-5eudyr")]/input').send_keys(
            "1000")
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-1ukn01m")]').click()  # 确认添加流动性
        self.instance.confirm_approval_from_metamask()
        time.sleep(2)

        # 断开网站
        try:
            self.instance.breakoff_website()
        except:
            pass
        finally:
            print(f"账号{n}，操作完成！")
        time.sleep(5)


def run():
    # 读取pk
    ph = Phezzan()
    for i in range(7, 10):
        # 连接网站
        ph.connect_website(i)
        # 领取usdt
        ph.claim_usdt()
        # 授权和质押
        ph.approve_deposit()
        # 提取usdt
        ph.withdraw_usdt()
        # 交易
        ph.trade()
        # 平仓
        ph.close_position()
        # 添加流动性
        ph.add_liquidity(i)


if __name__ == '__main__':
    run()
