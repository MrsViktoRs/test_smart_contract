import os
import pytest
from web3 import Web3
from vyper import compile_code

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
target_file = os.path.join(parent_dir, 'contracts/Token.vy')

@pytest.fixture
def w3():
    return Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

@pytest.fixture
def token_contract(w3):
    with open(target_file) as f:
        source = f.read()
    compiled = compile_code(source_code=source, output_formats=["abi", "bytecode"])
    abi = compiled["abi"]
    bytecode = compiled["bytecode"]

    acct = w3.eth.accounts[0]
    Token = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = Token.constructor().transact({"from": acct})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

def test_initial_balance(token_contract, w3):
    acct = w3.eth.accounts[0]
    balance = token_contract.functions.balanceOf(acct).call()
    assert balance == 1000 * 10**18

# def test_transfer(token_contract, w3):
#     acct1 = w3.eth.accounts[0]
#     acct2 = w3.eth.accounts[1]
#
#     tx = token_contract.functions.transfer(acct2, 100 * 10**18).transact({"from": acct1})
#     w3.eth.wait_for_transaction_receipt(tx)
#
#     balance1 = token_contract.functions.balanceOf(acct1).call()
#     balance2 = token_contract.functions.balanceOf(acct2).call()
#
#     assert balance1 == 900 * 10**18
#     assert balance2 == 100 * 10**18