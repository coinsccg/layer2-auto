# -*- coding: utf-8 -*-
import os
import util
import constant
from collection import Collection
from loguru import logger
from flask import Blueprint, make_response, jsonify, request

url = "/api/v1"
wallet_router = Blueprint("wallet", __name__, url_prefix="")


# 创建钱包
@wallet_router.route(f"{url}/create", methods=["GET"])
def create_wallet():
    try:
        wallet = list(util.create_wallet(1)[0])
        with open(f"wallets/{wallet[1]}", "w") as f:
            f.write(str(wallet[2]))
        return make_response(f"{wallet[1]}", 200)
    except Exception as e:
        logger.info(e)
        return make_response("create wallet error", 400)


# 归集钱包
@wallet_router.route(f"{url}/transfer", methods=["GET"])
def eth_transfer():
    try:
        coll = Collection(constant.SENDER, constant.PRIVATE_KEY)
        coll.transfer_eth_by_main_account()
        coll.transfer_usdt_to_main_account(constant.COLLECTION)
        return make_response(200)
    except Exception as e:
        logger.info(e)
        return make_response("transfer error", 400)


# 提现
@wallet_router.route(f"{url}/withdraw", methods=["POST"])
def usdt_transfer():
    try:
        accounts = request.json.get("accounts")
        ip = request.remote_addr
        if ip != "127.0.0.1":
            raise Exception(f"The interface is not open to the public, this request ip address: {ip}")
        coll = Collection(constant.SENDER, constant.PRIVATE_KEY)
        nonce = 0
        resp = []
        for i in accounts:
            nonce, tx_hash = coll.usdt_transfer(constant.SENDER, i["address"], i["amount"], nonce)
            resp.append({"address": i, "tx_hash": tx_hash})
        return make_response(jsonify(resp), 200)
    except Exception as e:
        logger.info(e)
        return make_response("withdraw error", 500)
