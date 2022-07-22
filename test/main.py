# -*- coding: gbk -*-
from utils.web import *
from auto_metamask import *


def run(pk: str):
    instance = ChromAndMetamask("C:\chrome\chromedriver.exe")
    driver = instance.driver
    driver.get('https://testnet.phezzan.xyz/')

    # 导入助记词

    seed = ["breeze ", "resemble ", "flash ", "increase ", "emerge ", "illness ", "pass ", "grace ", "upper ", "idle ",
            "addict ", "soft"]
    password = "12345678"
    instance.metamask_setup(seed, password)

    # 切换到测试网络
    network_name = "Rinkeby 测试网络"
    instance.change_metamask_network(network_name, pk)

    # 网站连接钱包
    driver.switch_to.window(driver.window_handles[0])
    driver.find_element(By.XPATH, '//div[contains(@class, "css-xs1ht3")]//button').click()
    driver.switch_to.window(driver.window_handles[0])
    driver.find_element(By.XPATH, '//div[text()="Metamask"]').click()

    instance.connect_to_website()

    # 领取USDT
    time.sleep(2)
    driver.find_element(By.XPATH, '//div[contains(@class, "css-1n5ssgg")]//button[1]').click()
    driver.switch_to.window(driver.window_handles[-1])
    driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-zcthtw")][2]').click()  # 领取USDT
    instance.confirm_approval_from_metamask()
    time.sleep(20)

    # 授权和质押
    n = 0
    while n < 2:
        driver.get('https://testnet.phezzan.xyz/')
        time.sleep(5)
        driver.find_element(By.XPATH, '//div[contains(@class, "css-1n5ssgg")]//button[1]').click()
        driver.switch_to.window(driver.window_handles[-1])
        driver.find_element(By.XPATH, '//div[contains(@class, "chakra-numberinput css-5eudyr")]/input').send_keys(
            "50000")  # 授权
        time.sleep(1)
        driver.find_element(By.XPATH, '//div[contains(@class, "chakra-stack css-1mslgq2")]/p').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-vt9cpy")]').click()
        instance.confirm_approval_from_metamask()
        driver.find_element(By.XPATH, '//button[contains(@class, "chakra-modal__close-btn css-xipghn")]').click()  # 关闭
        time.sleep(5)
        n += 1

    # 提取
    driver.get('https://testnet.phezzan.xyz/')
    time.sleep(5)
    driver.find_element(By.XPATH, '//div[contains(@class, "css-1n5ssgg")]//button[2]').click()
    driver.switch_to.window(driver.window_handles[-1])
    driver.find_element(By.XPATH, '//div[contains(@class, "chakra-numberinput css-5eudyr")]/input').send_keys(
        "100")  # 授权
    time.sleep(1)
    driver.find_element(By.XPATH, '//div[contains(@class, "chakra-stack css-o5l3sd")]/p').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-1enp6rw")]').click()
    time.sleep(5)
    instance.confirm_approval_from_metamask()
    driver.find_element(By.XPATH, '//button[contains(@class, "chakra-modal__close-btn css-xipghn")]').click()  # 关闭

    # 交易
    driver.get("https://testnet.phezzan.xyz/")
    time.sleep(5)
    driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-1x2v19b")]').click()
    driver.find_element(By.XPATH,
                        '//div[contains(@class,"css-vp1cdf")]//div[contains(@class, "chakra-linkbox css-thxllp")][1]').click()
    driver.find_element(By.XPATH,
                        '//div[contains(@class, "css-r4izcz")][2]//div[contains(@class, "chakra-numberinput css-5eudyr")]/input').send_keys(
        "100")
    driver.find_element(By.XPATH,
                        '//div[contains(@class, "chakra-stack css-1sigv9r")][1]/p[contains(@class, "chakra-text css-1ex7rpw")][1]').click()
    time.sleep(2)
    driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-1vbn212")]').click()  # 确认交易
    instance.confirm_approval_from_metamask()
    time.sleep(20)

    # 平仓
    driver.get("https://testnet.phezzan.xyz/")
    time.sleep(10)
    driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-1x2v19b")]').click()
    driver.find_element(By.XPATH,
                        '//div[contains(@class,"css-vp1cdf")]//div[contains(@class, "chakra-linkbox css-thxllp")][1]').click()
    time.sleep(5)
    driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-o31yjj")]').click()
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(3)
    driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-1qeu6q2")]').click()
    instance.confirm_approval_from_metamask()
    driver.find_element(By.XPATH, '//button[contains(@class, "chakra-modal__close-btn css-xipghn")]').click()

    # 添加流动性
    driver.get("https://testnet.phezzan.xyz/")
    time.sleep(5)
    driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-1hsas4s")]').click()
    driver.find_element(By.XPATH,
                        '//div[contains(@class,"css-vp1cdf")]//div[contains(@class, "chakra-linkbox css-thxllp")][1]').click()
    driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-18huy1h")]').click()

    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(2)
    driver.find_element(By.XPATH,
                        '//div[contains(@class, "css-r4izcz")][2]//div[contains(@class, "chakra-numberinput css-5eudyr")]/input').send_keys(
        "1000")
    time.sleep(2)
    driver.find_element(By.XPATH, '//button[contains(@class, "chakra-button css-1ukn01m")]').click()  # 确认添加流动性
    instance.confirm_approval_from_metamask()

    driver.close()


if __name__ == '__main__':
    # 读取pk
    pks = read_wallet_private_key()

    for i, pk in enumerate(pks[2:]):
        print(i, pk)
        run(pk)
