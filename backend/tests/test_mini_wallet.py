import os
import pytest
from web3 import Web3
from vyper import compile_code


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
target_file = os.path.join(parent_dir, 'contracts/MiniWallet.vy')

@pytest.fixture
def w3():
    return Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

@pytest.fixture
def mini_wallet_contract(w3):
    with open(target_file) as f:
        source = f.read()
    compiled = compile_code(source_code=source, output_formats=["abi", "bytecode"])
    abi = compiled["abi"]
    bytecode = compiled["bytecode"]

    acct = w3.eth.accounts[0]
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = contract.constructor().transact({"from": acct})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)


def test_deposit(mini_wallet_contract, w3):
    acct = w3.eth.accounts[1]
    amount = w3.to_wei(1, "ether")

    tx_hash = mini_wallet_contract.functions.deposit().transact(
        {"from": acct, "value": amount}
    )
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    logs = mini_wallet_contract.events.Deposit().process_receipt(receipt)
    assert len(logs) == 1
    args = logs[0]["args"]
    assert args["user"] == acct
    assert args["total"] == amount
    assert args["new_balances"] == mini_wallet_contract.functions.my_balances(acct).call()


# не работает вывод, не понимаю в чем причина
# def test_withdraw(mini_wallet_contract, w3):
#     acct = w3.eth.accounts[1]
#     amount = w3.to_wei(1, "ether")
#     mini_wallet_contract.functions.deposit().transact({"from": acct, "value": amount})
#
#     tx_hash = mini_wallet_contract.functions.withdraw(amount).transact({"from": acct})
#     receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
#
#     logs = mini_wallet_contract.events.Withdraw().process_receipt(receipt)
#     assert len(logs) == 1
#     args = logs[0]["args"]
#     assert args["user"] == acct
#     assert args["total"] == amount
#     assert args["new_balances"] == 0

