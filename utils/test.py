import time

import requests
import csv
from eth_account import Account
from web3 import Web3
from web3.middleware import geth_poa_middleware



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
    with open('./wallets.csv', 'w', newline='', encoding="UTF-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["序号", "钱包地址", "私钥", "公钥"])
        csv_writer.writerows(json_data)


def read_wallet() -> [str]:
    with open('./wallets.csv', 'r', encoding="UTF-8") as csv_file:
        reader = csv.reader(csv_file)
        wallets = []
        for i in reader:
            wallets.append(i[1])
    return wallets[1:]


def read_wallet_private_key() -> [dict]:
    wallets_private_key = []
    with open('./wallets.csv', encoding='UTF-8') as csv_file:
        reader = csv.reader(csv_file)
        n = 1
        for i in reader:
            if n > 1:
                address = i[1]
                key = i[2]
                wallets_private_key.append({"address": address, "key": key})
            n += 1

    return wallets_private_key


def eth_transfer(sender: str, private_key: str):
    w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/'))
    nonce = w3.eth.get_transaction_count(sender)
    gasPrice = w3.eth.gasPrice
    balance = w3.eth.get_balance(sender)
    if balance > Web3.toWei(1, "ether"):
        print(balance, nonce, sender)
        tx = w3.eth.account.sign_transaction({
            "nonce": nonce,
            "gasPrice": gasPrice,
            "gas": 100000,
            "from": sender,
            "to": "0xd3dE9c47b917baAd93F68B2c0D6dEe857D20b015",
            "value": balance - 8000000000000000,
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
            res = requests.post(url, headers=headers, data=address, timeout=3)
            print(res)
        except Exception as e:
            print(e)
        if n >= 4:
            break
        n += 1

def run():
    w3 = Web3(Web3.HTTPProvider('https://data-seed-prebsc-2-s3.binance.org:8545/'))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    txs = w3.geth.txpool.content()
    pending = dict(txs)
    print(pending)
    to = pending["to"]
    print(to)
    print(dict(dict(txs["pending"])))


if __name__ == "__main__":
    # wallets = read_wallet_private_key()
    # for i in wallets:
    #     eth_transfer(i["address"], i["key"])
    run()
