import os
import pytest
from web3 import Web3
from vyper import compile_code


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
target_file = os.path.join(parent_dir, 'contracts/SimpleStorage.vy')

@pytest.fixture
def w3():
    return Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

@pytest.fixture
def simple_storage_contract(w3):
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


def test_get_value(simple_storage_contract):
    start_value = simple_storage_contract.functions.get_value().call()
    assert start_value == 10


def test_set_value(simple_storage_contract, w3):
    acct = w3.eth.accounts[0]
    tx_hash = simple_storage_contract.functions.set_value(100).transact({"from": acct})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    assert tx_receipt.status == 1

    logs = simple_storage_contract.events.ValueSet().process_receipt(tx_receipt)
    assert len(logs) == 1
    event_args = logs[0]["args"]
    assert  event_args["owner"] == acct
    assert  event_args["value"] == 100