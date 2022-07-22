from eth_account import Account
from web3 import Web3
import csv
import constant

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
    with open('../main/tool/wallet/wallets.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["序号", "钱包地址", "私钥", "公钥"])
        csv_writer.writerows(json_data)


def read_wallet_and_eth_transfer():
    sender = "0x7cD1CB03FAE64CBab525C3263DBeB821Afd64483"
    pk = ""
    with open('../main/tool/wallet/wallets.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)

        n = 1
        nonce = 0
        for i in reader:
            if n > 2:
                nonce, _ = eth_transfer(sender, i[1], pk, nonce)
                nonce += 1
            n += 1


def read_wallet_private_key() -> [str]:
    wallets_private_key = []
    with open('../main/tool/wallet/wallets.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        n = 1
        for i in reader:
            if n > 1:
                wallets_private_key.append(i[2][2:])
            n += 1

    return wallets_private_key


def eth_transfer(sender: str, to: str, pk: str, nonce: int) -> (int, str):
    w3 = Web3(Web3.HTTPProvider(constant.INFURA_RPC))
    if nonce <= 0:
        nonce = w3.eth.get_transaction_count(sender) + 1
    gas_price = w3.eth.gasPrice
    tx = w3.eth.account.sign_transaction({
        "nonce": nonce,
        "gasPrice": gas_price,
        "gas": 100000,
        "from": sender,
        "to": to,
        "value": 2000000000000000,
        "chainId": 4,
        "data": b"",
    }, pk)
    tx_hash = w3.eth.send_raw_transaction(tx.rawTransaction)
    return nonce, tx_hash


def get_balance(account: str) -> float:
    w3 = Web3(Web3.HTTPProvider(constant.INFURA_RPC))
    balance = w3.eth.get_balance(account)
    return Web3.fromWei(balance, 'ether')


if __name__ == "__main__":
    # 创建钱包
    # wallets = create_wallet(200)
    # 保存至 csv 文件
    # write_wallet(wallets)
    #

    balance = get_balance("0x7cD1CB03FAE64CBab525C3263DBeB821Afd64483")
    print(balance)
