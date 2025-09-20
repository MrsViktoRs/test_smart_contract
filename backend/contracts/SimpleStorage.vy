# @version ^0.4.0
from web3.tools.pytest_ethereum.linker import deploy

name: public(String[64])
balances: HashMap[address, uint256]


@external
@payable
def deposit():
    return