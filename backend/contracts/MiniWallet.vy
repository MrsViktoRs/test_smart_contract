# @version ^0.4.0

owner: public(address)
total: public(uint256)
balances: HashMap[address, uint256]


event Deposit:
    user: address
    total: uint256
    new_balances: uint256

event Withdraw:
    user: address
    total: uint256
    new_balances: uint256

@deploy
def __init__():
    self.total = 0
    self.owner = msg.sender
    self.balances[msg.sender] = self.total


@external
@payable
def deposit() -> bool:
    assert msg.value > 0, 'You not send ETH'
    self.balances[msg.sender] += msg.value
    self.total += msg.value
    log Deposit(msg.sender, msg.value, self.balances[msg.sender])
    return True


# @external
# @nonreentrant
# def withdraw(amount: uint256) -> bool:
#     assert self.balances[msg.sender] >= amount, 'Your balance is less than the withdrawal amount'
#     self.balances[msg.sender] -= amount
#     self.total -= amount
#     send(msg.sender, amount)
#     log Withdraw(msg.sender, amount, self.balances[msg.sender])
#     return True


@external
@view
def my_balances(user: address) -> uint256:
    return self.balances[user]