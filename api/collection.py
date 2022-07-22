import os
from web3 import Web3
from web3.middleware import geth_poa_middleware

# testnet
# bsc_rpc = "https://data-seed-prebsc-1-s1.binance.org:8545/"
# contract = "0xF307e7Dbb1307F1E61811fD63d0EAaDd6771BA00"

# mainnet
bsc_rpc = "https://bsc-dataseed1.binance.org/"
contract = "0x55d398326f99059fF775485246999027B3197955"

abi = [{"inputs": [], "payable": False, "stateMutability": "nonpayable", "type": "constructor"},
       {"anonymous": False,
        "inputs": [{"indexed": True, "internalType": "address", "name": "owner", "type": "address"},
                   {"indexed": True, "internalType": "address", "name": "spender", "type": "address"},
                   {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"}],
        "name": "Approval", "type": "event"}, {"anonymous": False, "inputs": [
        {"indexed": True, "internalType": "address", "name": "previousOwner", "type": "address"},
        {"indexed": True, "internalType": "address", "name": "newOwner", "type": "address"}],
                                               "name": "OwnershipTransferred", "type": "event"},
       {"anonymous": False,
        "inputs": [{"indexed": True, "internalType": "address", "name": "from", "type": "address"},
                   {"indexed": True, "internalType": "address", "name": "to", "type": "address"},
                   {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"}],
        "name": "Transfer", "type": "event"}, {"constant": True, "inputs": [], "name": "_decimals",
                                               "outputs": [
                                                   {"internalType": "uint8", "name": "", "type": "uint8"}],
                                               "payable": False, "stateMutability": "view", "type": "function"},
       {"constant": True, "inputs": [], "name": "_name",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False,
        "stateMutability": "view", "type": "function"}, {"constant": True, "inputs": [], "name": "_symbol",
                                                         "outputs": [{"internalType": "string", "name": "",
                                                                      "type": "string"}], "payable": False,
                                                         "stateMutability": "view", "type": "function"},
       {"constant": True, "inputs": [{"internalType": "address", "name": "owner", "type": "address"},
                                     {"internalType": "address", "name": "spender", "type": "address"}],
        "name": "allowance", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False, "stateMutability": "view", "type": "function"}, {"constant": False, "inputs": [
        {"internalType": "address", "name": "spender", "type": "address"},
        {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "approve", "outputs": [
        {"internalType": "bool", "name": "", "type": "bool"}], "payable": False,
                                                                           "stateMutability": "nonpayable",
                                                                           "type": "function"},
       {"constant": True, "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False, "stateMutability": "view", "type": "function"},
       {"constant": False, "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}],
        "name": "burn", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False,
        "stateMutability": "nonpayable", "type": "function"},
       {"constant": True, "inputs": [], "name": "decimals",
        "outputs": [{"internalType": "uint8", "name": "",
                     "type": "uint8"}], "payable": False,
        "stateMutability": "view", "type": "function"},
       {"constant": False, "inputs": [{"internalType": "address", "name": "spender", "type": "address"},
                                      {"internalType": "uint256", "name": "subtractedValue",
                                       "type": "uint256"}],
        "name": "decreaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False, "stateMutability": "nonpayable", "type": "function"},
       {"constant": True, "inputs": [], "name": "getOwner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}], "payable": False,
        "stateMutability": "view", "type": "function"}, {"constant": False, "inputs": [
        {"internalType": "address", "name": "spender", "type": "address"},
        {"internalType": "uint256", "name": "addedValue", "type": "uint256"}], "name": "increaseAllowance",
                                                         "outputs": [
                                                             {"internalType": "bool", "name": "",
                                                              "type": "bool"}],
                                                         "payable": False, "stateMutability": "nonpayable",
                                                         "type": "function"},
       {"constant": False, "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}],
        "name": "mint", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False,
        "stateMutability": "nonpayable", "type": "function"}, {"constant": True, "inputs": [], "name": "name",
                                                               "outputs": [
                                                                   {"internalType": "string", "name": "",
                                                                    "type": "string"}], "payable": False,
                                                               "stateMutability": "view", "type": "function"},
       {"constant": True, "inputs": [], "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}], "payable": False,
        "stateMutability": "view", "type": "function"},
       {"constant": False, "inputs": [], "name": "renounceOwnership", "outputs": [], "payable": False,
        "stateMutability": "nonpayable", "type": "function"}, {"constant": True, "inputs": [], "name": "symbol",
                                                               "outputs": [
                                                                   {"internalType": "string", "name": "",
                                                                    "type": "string"}], "payable": False,
                                                               "stateMutability": "view", "type": "function"},
       {"constant": True, "inputs": [], "name": "totalSupply",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False,
        "stateMutability": "view", "type": "function"}, {"constant": False, "inputs": [
        {"internalType": "address", "name": "recipient", "type": "address"},
        {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "transfer", "outputs": [
        {"internalType": "bool", "name": "", "type": "bool"}], "payable": False,
                                                         "stateMutability": "nonpayable",
                                                         "type": "function"}, {"constant": False, "inputs": [
        {"internalType": "address", "name": "sender", "type": "address"},
        {"internalType": "address", "name": "recipient", "type": "address"},
        {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "transferFrom", "outputs": [
        {"internalType": "bool", "name": "", "type": "bool"}], "payable": False,
                                                                               "stateMutability": "nonpayable",
                                                                               "type": "function"},
       {"constant": False, "inputs": [{"internalType": "address", "name": "newOwner", "type": "address"}],
        "name": "transferOwnership", "outputs": [], "payable": False, "stateMutability": "nonpayable",
        "type": "function"}]


class Collection:

    def __init__(self, tmp_account: str, private_key: str):
        self.w3 = Web3(Web3.HTTPProvider(bsc_rpc))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.instance = self.w3.eth.contract(address=contract, abi=abi)
        self.tmp_account = tmp_account
        self.private_key = private_key

    def usdt_transfer(
            self,
            sender: str,
            recipient: str,
            amount: int,
            nonce: int
    ) -> (int, str):
        # 查询余额
        sender = Web3.toChecksumAddress(sender)
        balance = self.instance.functions.balanceOf(sender).call()
        if nonce <= 0:
            nonce = self.w3.eth.get_transaction_count(sender)
        try:
            # 归集
            amount = Web3.toWei(amount, "ether")
            if balance < amount:
                return nonce, ""
            recipient = Web3.toChecksumAddress(recipient)
            gas_price = self.w3.eth.gas_price
            tx = self.instance.functions.transfer(recipient, amount).buildTransaction({
                "nonce": nonce,
                "gasPrice": gas_price,
                "gas": 100000,
            })
            sign_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
            res = self.w3.eth.send_raw_transaction(sign_tx.rawTransaction)
            print(res.hex())
            nonce += 1
            return nonce, res.hex()
        except:
            return nonce, ""

    # 给存在usdt的账户转入gas费
    def eth_transfer(self, recipient: str, nonce: int) -> int:
        # 查询余额
        recipient = Web3.toChecksumAddress(recipient)
        usdt_balance = self.instance.functions.balanceOf(recipient).call()
        if nonce <= 0:
            nonce = self.w3.eth.get_transaction_count(self.tmp_account)
        if usdt_balance > 0:
            gas_price = self.w3.eth.gas_price
            min_balance = Web3.toWei(0.0002, "ether")
            balance = self.w3.eth.get_balance(recipient)
            # 余额不够支付gas, 需要充值
            if balance <= min_balance:
                tx = {
                    "from": self.tmp_account,
                    "to": recipient,
                    "nonce": nonce,
                    "gasPrice": gas_price,
                    "gas": 100000,
                    "value": Web3.toWei(0.002, "ether"),
                    "data": "",
                }
                sign_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
                res = self.w3.eth.send_raw_transaction(sign_tx.rawTransaction)
                self.w3.eth.wait_for_transaction_receipt(res)
                print(res.hex())
                nonce += 1
        return nonce

    # 归集usdt
    def focus_usdt(self, sender: str, recipient: str, private_key: str):
        # 查询余额
        recipient = Web3.toChecksumAddress(recipient)
        sender = Web3.toChecksumAddress(sender)
        usdt_balance = self.instance.functions.balanceOf(sender).call()
        if usdt_balance > 0:
            # 归集
            gas_price = self.w3.eth.gas_price
            nonce = self.w3.eth.get_transaction_count(sender)
            tx = self.instance.functions.transfer(recipient, usdt_balance). \
                buildTransaction({
                "nonce": nonce,
                "gasPrice": gas_price,
                "gas": 100000,
            })
            sign_tx = self.w3.eth.account.sign_transaction(tx, private_key)
            res = self.w3.eth.send_raw_transaction(sign_tx.rawTransaction)
            print(res.hex())

    @staticmethod
    def loop_wallet_dir() -> [str]:
        dirs = os.walk("wallets")
        wallets = []
        for _, _, f in dirs:
            for i in f:
                wallets.append(i)
        return wallets

    """
    向所有usdt代表余额大于0的账号转入gas
    """

    def transfer_eth_by_main_account(self):
        nonce = 0
        wallets = self.loop_wallet_dir()

        for i in wallets:
            nonce = self.eth_transfer(i, nonce)

    """
    归集所有账号的usdt代币到主账号
    """

    def transfer_usdt_to_main_account(self, to: str):
        wallets = self.loop_wallet_dir()
        for i in wallets:
            with open(f"wallets/{i}") as f:
                private_key = f.readlines()[0]
            self.focus_usdt(i, to, private_key)


if __name__ == '__main__':
    # testnet
    # from_account = "0x7cD1CB03FAE64CBab525C3263DBeB821Afd64483"
    # pk = ""

    # mainnet
    from_account = "0x7b184160dac2128a7a41c7c2c77b16e6B1f719d3"
    pk = ""

    collection_address = "0x6Cc1072A48A6E1C19a07a2F668bDa4e588DF878d"

    coll = Collection(from_account, pk)
    coll.transfer_eth_by_main_account()
    coll.transfer_usdt_to_main_account(collection_address)
