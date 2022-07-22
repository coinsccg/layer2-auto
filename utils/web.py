import time

import requests
from eth_account import Account
from web3 import Web3
import csv


# 安装： pip3 install eth_account
#       pip3 install web3

def create_wallet(num: int) -> [str]:
    wallets = []

    for i in range(num):
        # 添加一些随机性
        account = Account.create('Random  Seed' + str(i))

        # 私钥
        privateKey = account._key_obj

        # 公钥
        publicKey = privateKey.public_key

        # 地址
        address = publicKey.to_checksum_address()

        wallet = {
            "id": str(i),
            "address": address,
            "privateKey": privateKey,
            "publicKey": publicKey
        }
        wallets.append(wallet.values())

    return wallets


def write_wallet(json_data):
    with open('./wallets.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["序号", "钱包地址", "私钥", "公钥"])
        csv_writer.writerows(json_data)


def read_wallet() -> [str]:
    with open('./wallets.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        wallets = []
        for i in reader:
            wallets.append(i[1])
    return wallets[1:]


def read_wallet_private_key() -> [str]:
    wallets_private_key = []
    with open('./wallets.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        n = 1
        for i in reader:
            if n > 1:
                wallets_private_key.append(i[2][2:])
            n += 1

    return wallets_private_key


def eth_transfer(sender: str, private_key: str):
    w3 = Web3(Web3.HTTPProvider('https://kovan.infura.io/v3/'))
    nonce = w3.eth.get_transaction_count(sender)
    gasPrice = w3.eth.gasPrice
    balance = w3.eth.get_balance(sender)
    if balance > 0:
        tx = w3.eth.account.sign_transaction({
            "nonce": nonce,
            "gasPrice": gasPrice,
            "gas": 100000,
            "from": sender,
            "to": "0xd3dE9c47b917baAd93F68B2c0D6dEe857D20b015",
            "value": balance - 200000000000000,
            "data": b"",
        }, private_key)
        res = w3.eth.send_raw_transaction(tx.rawTransaction)
        print(res.hex())


def request_ropsten(address: str):
    url = "https://faucet.metamask.io/v0/request"
    headers = {"Content-Type": "application/rawdata"}
    n = 1
    while True:
        try:
            time.sleep(5)
            res = requests.post(url, headers=headers, data=address, timeout=3, verify=False)
            print(res)
        except Exception as e:
            print(e)
        if n >= 5:
            break
        n += 1


if __name__ == "__main__":
    # # 创建钱包
    wallets = create_wallet(500)
    # 保存至 csv 文件
    write_wallet(wallets)

    # 读取地址
    wallets = read_wallet()
    for i in wallets:
        print(i)
        request_ropsten(i)