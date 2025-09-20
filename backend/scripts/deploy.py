import os
from dotenv import load_dotenv
from web3 import Web3
from vyper import compile_code

load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL", "http://127.0.0.1:8545")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

if not w3.is_connected():
    raise Exception("Failed to connect")

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

if PRIVATE_KEY:
    acct = w3.eth.account.from_key(PRIVATE_KEY)
    print(f"Used private key for wallet: {acct.address}")
else:
    acct = w3.eth.accounts[0]
    print(f"Used Ganache: {acct}")


def deploy_contract(contract_name: str, constructor_args=None):
    if constructor_args is None:
        constructor_args = []

    with open(f'{parent_dir}/contracts/{contract_name}.vy') as f:
        source = f.read()

    compiled = compile_code(source_code=source, output_formats=["abi", "bytecode"])
    abi = compiled["abi"]
    bytecode = compiled["bytecode"]

    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    gas_estimate = contract.constructor(*constructor_args).estimate_gas({"from": acct.address})
    gas_price = w3.eth.gas_price
    if w3.eth.get_balance(acct.address) < gas_estimate * gas_price:
        raise Exception(f"Shortage ETH")

    if PRIVATE_KEY:
        construct_txn = contract.constructor(*constructor_args).build_transaction({
            "from": acct.address,
            "nonce": w3.eth.get_transaction_count(acct.address),
            "gas": gas_estimate,
            "gasPrice": gas_price,
        })
        signed_txn = w3.eth.account.sign_transaction(construct_txn, private_key=PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    else:
        tx_hash = contract.constructor().transact({"from": acct})

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Smart-contract deploy at:", tx_receipt.contractAddress)

    import json
    os.makedirs("../build", exist_ok=True)
    with open(f"../build/{contract_name}.json", "w") as f:
        json.dump({"abi": abi, "bytecode": bytecode}, f, indent=4)
        print(f'Smart-contract "{contract_name}" compiled')


if __name__ == "__main__":
    deploy_contract('BaseContract')
    deploy_contract('Token')