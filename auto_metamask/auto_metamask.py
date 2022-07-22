import os
import time
import urllib.request

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

EXTENSION_ID = 'nkbihfbeogaeaoehlefnkodbefgpgknn'
ARGENT_EXTENSION_ID = 'dlcobpjiigpikoobohmabehhmhfoodbb'
EXTENSION_PATH = os.path.abspath("") + '\main\\tool\metamask\extension_metamask.crx'


class ChromAndMetamask:
    driver = None

    def __init__(self, driver_path):
        chrome_options = Options()
        # chrome_options.add_extension(EXTENSION_PATH)
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9014")
        path = os.path.abspath("") + driver_path
        self.driver = webdriver.Chrome(options=chrome_options, executable_path=path)

    @staticmethod
    def download_metamask_extension():
        url = 'https://xord-testing.s3.amazonaws.com/selenium/10.0.2_0.crx'
        urllib.request.urlretrieve(url, os.getcwd() + '\extension_metamask.crx')

    def check_handles(self):
        handles_value = self.driver.window_handles
        if len(handles_value) > 1:
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            self.check_handles()

    def login_metamask(self, password: str):
        self.driver.execute_script("window.open();")
        self.driver.switch_to.window(self.driver.window_handles[1])
        n = 1
        while True:
            try:
                self.driver.get('chrome-extension://{}/home.html'.format(EXTENSION_ID))
                time.sleep(2)
                text = self.driver.find_element(By.XPATH, '//button[text()="解锁"]').text
                if text == "解锁":
                    break
                if n >= 4:
                    break
                n += 1
            except:
                pass

        self.driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//button[text()="解锁"]').click()
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def metamask_setup(self, phrase, password):
        self.driver.switch_to.window(self.driver.window_handles[0])

        self.driver.find_element(By.XPATH, '//button[text()="开始使用"]').click()
        self.driver.find_element(By.XPATH, '//button[text()="导入钱包"]').click()
        self.driver.find_element(By.XPATH, '//button[text()="我同意"]').click()

        time.sleep(3)

        inputs = self.driver.find_elements(By.XPATH, '//input')
        inputs[0].send_keys(phrase)
        inputs[1].send_keys(password)
        inputs[2].send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, '.first-time-flow__terms').click()
        self.driver.find_element(By.XPATH, '//button[text()="导入"]').click()

        # time.sleep(8)
        time.sleep(3)
        self.driver.find_element(By.XPATH, '//button[text()="全部完成"]').click()
        # time.sleep(2)

        # # closing the message popup after all done metamask screen
        # self.driver.find_element(By.XPATH,'//*[@id="popover-content"]/div/div/section/header/div/button').click()
        # time.sleep(2)
        print("Wallet has been imported successfully")
        # time.sleep(1)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def import_wallet_and_change_network(self, network_name, pk):
        # opening network
        print("Changing network")
        self.driver.execute_script("window.open();")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get('chrome-extension://{}/home.html'.format(EXTENSION_ID))
        time.sleep(3)

        try:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.find_element(By.XPATH, '//*[@id="popover-content"]/div/div/section/header/div/button').click()
        except Exception as e:
            print(e)

        # 添加新账号
        self.driver.find_element(By.XPATH, '//div[contains(@class, "identicon__address-wrapper")]').click()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.find_element(By.XPATH,
                                 '//div[contains(@class, "account-menu__item account-menu__item--clickable")][2]/div[contains(@class, "account-menu__item__text")]').click()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.find_element(By.XPATH,
                                 '//div[contains(@class, "new-account-import-form__private-key-password-container")]/input').send_keys(
            pk)
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//button[contains(@class, "btn-secondary")]').click()

        # 打开网络下拉框
        self.driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[1]/div/div[2]/div[1]/div/span').click()
        # 跳转开启测试网设置
        # self.driver.find_element(By.XPATH,'//*[@id="app-content"]/div/div[2]/div/div[1]/div[3]/span/a').click()

        # 显示测试网
        # self.driver.find_element(By.XPATH,
        #     '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/div[7]/div[2]/div/div/div[1]/div[2]/div').click()

        # 滑到最上方
        # self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")

        # 打开网络下拉框
        # self.driver.find_element(By.XPATH,'//*[@id="app-content"]/div/div[1]/div/div[2]/div[1]/div/span').click()
        print("opening network dropdown")
        time.sleep(2)
        # 以太坊 Ethereum 主网络
        # Ropsten 测试网络
        # Kovan 测试网络
        # Rinkeby 测试网络
        # Goerli 测试网络
        all_li = self.driver.find_elements(By.TAG_NAME, 'li')

        for li in all_li:
            text = li.text
            if text == network_name:
                li.click()
                print(text, "is selected")
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                return
        print("Please provide a valid network name")
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(3)

    def change_network(self, network_name: str):
        self.driver.execute_script("window.open();")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get('chrome-extension://{}/home.html'.format(EXTENSION_ID))
        time.sleep(2)

        # 打开网络下拉框
        self.driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[1]/div/div[2]/div[1]/div/span').click()
        time.sleep(1)

        all_li = self.driver.find_elements(By.TAG_NAME, 'li')
        for li in all_li:
            text = li.text
            if text == network_name:
                li.click()
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                return
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def add_and_change_network(self):
        time.sleep(5)
        self.driver.execute_script("window.open();")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get('chrome-extension://{}/home.html'.format(EXTENSION_ID))
        # self.driver.refresh()
        self.driver.find_element(By.XPATH, "//button[text()='批准']").click()
        self.driver.find_element(By.XPATH, "//button[text()='切换网络']").click()
        time.sleep(3)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def change_network_by_chain_list(self, network_name):
        time.sleep(5)
        print("切换指定网络开始")
        self.driver.execute_script("window.open();")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get('https://chainlist.org/')
        self.driver.find_element(By.XPATH, "//h5[text()='Connect Wallet']").click()
        # connect chainlist
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[2])
        self.driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
        self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
        time.sleep(3)
        self.driver.find_element(By.XPATH, '//button[text()="下一步"]').click()
        self.driver.find_element(By.XPATH, '//button[text()="连接"]').click()
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[1])
        # search Network
        self.driver.find_element(By.XPATH, "//span[text()='Testnets']").click()
        time.sleep(1)
        inputs = self.driver.find_elements(By.XPATH, '//input')
        inputs[0].send_keys(network_name)
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//span[text()='Add to Metamask']").click()
        # change Network
        time.sleep(3)
        self.driver.execute_script("window.open();")
        self.driver.switch_to.window(self.driver.window_handles[2])
        self.driver.get('chrome-extension://{}/home.html'.format(EXTENSION_ID))
        self.driver.find_element(By.XPATH, "//button[text()='批准']").click()
        self.driver.find_element(By.XPATH, "//button[text()='切换网络']").click()
        time.sleep(3)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def connect_to_website(self):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])

        n = 1
        while True:
            self.driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
            self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
            time.sleep(2)
            try:
                self.driver.find_element(By.XPATH, '//button[text()="下一步"]').click()
                time.sleep(2)
                self.driver.find_element(By.XPATH, '//button[text()="连接"]').click()
            except:
                try:
                    self.driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[3]/div[2]/button[2]').click()
                    time.sleep(1)
                    self.driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[2]/div[2]/div[2]/footer/button[2]').click()
                    break
                except:
                    pass
            if n >= 2:
                break
            n += 1
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def confirm_approval_from_metamask(self):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        n = 1
        while True:
            self.driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
            self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
            time.sleep(3)
            try:
                self.driver.find_element(By.XPATH, '//button[text()="确认"]').click()
                break
            except:
                n += 1
            if n >= 5:
                break
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def reject_approval_from_metamask(self):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])

        self.driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
        # time.sleep(10)
        self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
        # time.sleep(10)
        # confirm approval from metamask
        self.driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[4]/footer/button[1]').click()
        time.sleep(8)
        print("Approval transaction rejected")

        # switch to dafi
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(3)
        print("Reject approval from metamask")

    def confirm_transaction_from_metamask(self):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])

        self.driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
        time.sleep(2)
        self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
        time.sleep(2)

        # # confirm transaction from metamask
        self.driver.find_element(By.XPATH,
                                 '//*[@id="app-content"]/div/div[3]/div/div[3]/div[3]/footer/button[2]').click()
        time.sleep(2)
        print("Transaction confirmed")
        # switch to dafi
        self.driver.switch_to.window(self.driver.window_handles[0])

        time.sleep(3)

    def reject_transaction_from_metamask(self):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])

        self.driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
        time.sleep(5)
        self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
        time.sleep(5)
        # confirm approval from metamask
        self.driver.find_element(By.XPATH,
                                 '//*[@id="app-content"]/div/div[3]/div/div[3]/div[3]/footer/button[1]').click()
        time.sleep(2)
        print("Transaction rejected")

        # switch to web window
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(3)

    def add_token(self, token_address):
        # opening network
        print("Adding Token")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get('chrome-extension://{}/home.html'.format(EXTENSION_ID))
        print("closing popup")
        time.sleep(5)
        self.driver.find_element(By.XPATH, '//*[@id="popover-content"]/div/div/section/header/div/button').click()

        # self.driver.find_element(By.XPATH,'//*[@id="app-content"]/div/div[1]/div/div[2]/div[1]/div/span').click()
        # time.sleep(2)

        print("clicking add token button")
        self.driver.find_element(By.XPATH,
                                 '//*[@id="app-content"]/div/div[4]/div/div/div/div[3]/div/div[3]/button').click()
        time.sleep(2)
        # adding address
        self.driver.find_element("custom-address").send_keys(token_address)
        time.sleep(10)
        # clicking add
        self.driver.find_element(By.XPATH,
                                 '//*[@id="app-content"]/div/div[4]/div/div[2]/div[2]/footer/button[2]').click()
        time.sleep(2)
        # add tokens
        self.driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[4]/div/div[3]/footer/button[2]').click()
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(3)

    def sign_confirm(self):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        n = 1
        while True:
            text = ""
            try:
                self.driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
                time.sleep(2)
                text = self.driver.find_element(By.XPATH, '//button[text()="签名"]').text
            except:
                pass
            if text == "签名":
                self.driver.find_element(By.XPATH, '//button[text()="签名"]').click()
                break
            if n >= 2:
                break
            n += 1
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def sign_reject(self):
        time.sleep(3)

        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])

        self.driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
        time.sleep(5)
        self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
        time.sleep(3)
        self.driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[3]/button[1]').click()
        time.sleep(1)
        # self.driver.find_element(By.XPATH,'//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/footer/button[2]').click()
        # time.sleep(3)
        print('Sign rejected')
        print(self.driver.window_handles)
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(3)

    def change_account(self, id: int):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get('chrome-extension://{}/home.html'.format(EXTENSION_ID))
        time.sleep(2)
        # 切换账号
        self.driver.find_element(By.XPATH, '//div[contains(@class, "identicon__address-wrapper")]').click()
        time.sleep(1)
        try:
            self.driver.find_element(By.XPATH,
                                     f'//*[@id="app-content"]/div/div[3]/div[4]/div/div[{id}]/div[3]/div[1]').click()
        except:
            self.driver.find_element(By.XPATH,
                                     f'//*[@id="app-content"]/div/div[3]/div[4]/div[3]/div[{id}]/div[3]').click()

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def breakoff_website(self, url):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])

        self.driver.get('chrome-extension://{}/home.html'.format(EXTENSION_ID))
        time.sleep(2)

        # 断开网络
        self.driver.find_element(By.XPATH,
                                 '//button[contains(@class, "fas fa-ellipsis-v menu-bar__account-options")]').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//*[@id="popover-content"]/div[2]/button[3]').click()
        self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
        time.sleep(1)
        self.driver.find_element(By.XPATH,
                                 '//div[@class="connected-sites-list__content-row"][last()]/a').click()

        try:
            n = 1
            while True:
                text = self.driver.find_element(By.XPATH,
                                                f'//*[@id="popover-content"]/div/div/section/div[2]/main/div[{n}]/div/span').text
                if url.split("//")[-1] == text:
                    self.driver.find_element(By.XPATH,
                                             f'//*[@id="popover-content"]/div/div/section/div[2]/main/div[{n}]/a')
                    break
        except:
            pass

        time.sleep(1)
        self.driver.find_element(By.XPATH, '//*[@id="popover-content"]/div/div/section/div[2]/div/button[2]').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//button[@title="关闭"]').click()

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def approve_add_network(self):
        time.sleep(5)
        self.driver.switch_to.window(self.driver.window_handles[1])

        self.driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
        try:
            time.sleep(2)
            ele = self.driver.find_element(By.XPATH, '//button[text()="批准"]')
            self.driver.execute_script("arguments[0].click();", ele)
        except:
            pass

        try:
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//button[text()="切换网络"]').click()
        except:
            pass

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    # ------------------------------------------------------------------------------------------------------------------

    def argent_connect_to_website(self):
        time.sleep(2)

        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])

        self.driver.get('chrome-extension://{}/index.html'.format(ARGENT_EXTENSION_ID))
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//button[text()="下一步"]').click()
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def confirm_approval_from_argent(self):
        time.sleep(5)
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get('chrome-extension://{}/index.html'.format(ARGENT_EXTENSION_ID))
        time.sleep(3)

        try:
            n = 1
            while n <= 10:
                self.driver.find_element(By.XPATH, '//button[text()="Sign"]').click()
                n += 1
                time.sleep(1)
        except:
            pass

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def argent_approve_add_token(self):
        time.sleep(2)
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])

        self.driver.get('chrome-extension://{}/index.html'.format(ARGENT_EXTENSION_ID))
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH,
                                                                             '//*[@id="root"]/div/div/form/div[2]/label')))
        self.driver.find_element(By.XPATH, '//button[text()="Continue"]').click()
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def argent_change_account(self, num: int):
        time.sleep(2)
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])

        self.driver.get('chrome-extension://{}/index.html'.format(ARGENT_EXTENSION_ID))
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/header/a').click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, f'//*[@id="root"]/div/div/div[2]/div[{num}]/div').click()
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def login_argent(self, password: str):
        self.driver.execute_script("window.open();")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get('chrome-extension://{}/index.html'.format(ARGENT_EXTENSION_ID))
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(password)
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//button[text()="Unlock"]').click()
        time.sleep(5)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def argent_change_network(self, name):
        self.driver.execute_script("window.open();")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get('chrome-extension://{}/index.html'.format(ARGENT_EXTENSION_ID))
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/header/div/div[1]').click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, f'//span[text()="{name}"]').click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[1]/div').click()
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
