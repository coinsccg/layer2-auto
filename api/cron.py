import os
import time
import constant
import requests
import schedule
from loguru import logger
from web3 import Web3

nRPC = "http://192.168.120.164:9991/api/F_User/rechargeIntegral"
verification = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIxMDAwMDAwIiwiaWF0IjoiMTY1MTgzMTQyMCIsIm5iZiI6IjE2NTE4MzE0MjAiLCJleHAiOiIxNjUxODM4NjIwIiwiaXNzIjoidm9sLmNvcmUub3duZXIiLCJhdWQiOiJ2b2wuY29yZSJ9.McQKlFl3c7N4sL9zLLRZOM7e41r_CYedy9Kk4cqyp10"

def job():
    dir = os.walk("wallets")
    for _, _, f in dir:
        for i in f:
            try:
                url = constant.BSC_RPC + f"&address={i}"
                resp = requests.get(url)
                result = resp.json()
                if resp.status_code != 200:
                    logger.info(result)
                    continue
                req_list = []
                for v in result["result"]:
                    to = v["to"]
                    if to == i.lower():
                        tx_hash = v["hash"]
                        timestamp = v["timeStamp"]
                        sender = v["from"]
                        blockNumber = v["blockNumber"]
                        gas = v["gas"]
                        gasPrice = v["gasPrice"]
                        nonce = v["nonce"]
                        blockHash = v["blockHash"]
                        value = float(Web3.fromWei(int(v["value"]), 'ether'))
                        req = {
                            "verification": verification,
                            "hash": tx_hash,
                            "blockHash": blockHash,
                            "timeStamp": timestamp,
                            "from": sender,
                            "to": i,
                            "blockNumber": blockNumber,
                            "gas": gas,
                            "gasPrice": gasPrice,
                            "value": value,
                            "nonce": nonce
                        }
                        req_list.append(req)
                if len(req_list) > 0:
                    headers = {'Content-Type': 'application/json'}
                    res = requests.post(nRPC, headers=headers, json=req_list)
            except Exception as e:
                logger.info(e)


def timer():
    # schedule.every(5).minutes.do(job)
    schedule.every(20).seconds.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    timer()
