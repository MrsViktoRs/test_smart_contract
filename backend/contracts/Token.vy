# @version ^0.4.0

name: public(String[64])
symbol: public(String[32])
decimals: public(uint256)
total_supply: public(uint256)
balances: HashMap[address, uint256]

@deploy
def __init__():
    self.name = "MyToken"
    self.symbol = "MTK"
    self.decimals = 18
    self.total_supply = 1000 * 10 ** 18
    self.balances[msg.sender] = self.total_supply

@external
def transfer(_to: address, _value: uint256) -> bool:
    assert self.balances[msg.sender] >= _value, "Not enough balance"
    self.balances[msg.sender] -= _value
    self.balances[_to] += _value
    return True

@view
@external
def balanceOf(_owner: address) -> uint256:
    return self.balances[_owner]