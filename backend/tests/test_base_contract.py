import os
import pytest
from web3 import Web3
from vyper import compile_code


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
target_file = os.path.join(parent_dir, 'contracts/BaseContract.vy')


@pytest.fixture
def w3():
    return Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))


@pytest.fixture
def base_contract(w3):
    with open(target_file) as f:
        source = f.read()
    compiled = compile_code(source_code=source, output_formats=["abi", "bytecode"])
    abi = compiled["abi"]
    bytecode = compiled["bytecode"]

    acct = w3.eth.accounts[0]
    token = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = token.constructor().transact({"from": acct})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)


def test_get_gas_price(base_contract):
    gas_price = base_contract.functions.getGasPrice().call()
    assert isinstance(gas_price, int)
    assert gas_price > 0


def test_get_caller(base_contract, w3):
    acct = w3.eth.accounts[0]
    caller = base_contract.functions.getCaller().call({"from": acct})
    assert caller == acct
