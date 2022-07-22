import os
import time
import requests
from web3 import Web3
from loguru import logger
from web3.middleware import geth_poa_middleware

nRPC = "http://192.168.120.164:9991/api/F_User/rechargeIntegral"
verification = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIxMDAwMDAwIiwiaWF0IjoiMTY1MTgzMTQyMCIsIm5iZiI6IjE2NTE4MzE0MjAiLCJleHAiOiIxNjUxODM4NjIwIiwiaXNzIjoidm9sLmNvcmUub3duZXIiLCJhdWQiOiJ2b2wuY29yZSJ9.McQKlFl3c7N4sL9zLLRZOM7e41r_CYedy9Kk4cqyp10"


def run():
    w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org/'))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    while True:
        time.sleep(3)
        with open("last_block.txt") as f:
            lastBlockNumber = f.readlines()[0]

        # 获取最新区块
        lastBlock = w3.eth.get_block("latest")
        number = lastBlock.get("number")

        if int(lastBlockNumber) <= number:
            try:
                block = w3.eth.get_block(int(lastBlockNumber))
                timestamp = block.get("timestamp")

                # 筛选事件
                filter = w3.eth.filter(
                    {'fromBlock': block.get("number"), 'toBlock': block.get("number"),
                     'address': '0x55d398326f99059fF775485246999027B3197955'})
                events = w3.eth.get_filter_logs(filter.filter_id)

                # 遍历钱包目录
                dir = os.walk("wallets")
                for _, _, f in dir:
                    for i in f:
                        topic0 = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
                        req_list = []
                        for e in events:
                            event = dict(e)
                            topic = event["topics"]
                            to = "0x" + topic[2].hex()[-40:]
                            tx_hash = event["transactionHash"].hex()

                            # 事件中的接受地址要等于钱包地址
                            if topic[0].hex() == topic0 and to == i.lower():
                                result = w3.eth.get_transaction(tx_hash)
                                resp = dict(result)
                                method_id = resp["input"][:10]
                                blockHash = resp["blockHash"].hex()
                                sender = resp["from"]
                                blockNumber = resp["blockNumber"]
                                gas = resp["gas"]
                                gasPrice = resp["gasPrice"]
                                value = Web3.toInt(hexstr=event["data"])
                                nonce = resp["nonce"]

                                # 事件为transfer事件
                                if method_id == "0xa9059cbb":
                                    req = {
                                        "verification": verification,
                                        "hash": tx_hash,
                                        "blockHash": blockHash,
                                        "timeStamp": str(timestamp),
                                        "from": sender,
                                        "to": i,
                                        "blockNumber": str(blockNumber),
                                        "gas": str(gas),
                                        "gasPrice": str(gasPrice),
                                        "value": float(Web3.fromWei(int(value), 'ether')),
                                        "nonce": str(nonce)
                                    }
                                    req_list.append(req)

                        # 向充值服务器发送数据
                        if len(req_list) > 0:
                            headers = {'Content-Type': 'application/json'}
                            res = requests.post(nRPC, headers=headers, json=req_list)
                            print(res.status_code)
            except Exception as e:
                logger.info(e)

            # 记录区块
            with open("last_block.txt", "w") as f:
                print(str(int(lastBlockNumber) + 1))
                f.write(str(int(lastBlockNumber) + 1))


if __name__ == '__main__':
    run()
