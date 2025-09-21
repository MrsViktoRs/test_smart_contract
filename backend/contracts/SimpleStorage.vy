# @version ^0.4.0

owner: public(address)
stored_number: public(int256)


event ValueSet:
    owner: indexed(address)
    value: int256

@deploy
def __init__():
    self.owner = msg.sender
    self.stored_number = 10


@external
def set_value(new_value: int256) -> bool:
    assert msg.sender == self.owner, 'Not owner'
    self.stored_number = new_value
    log ValueSet(msg.sender, new_value)
    return True


@external
@view
def get_value() -> int256:
    return self.stored_number
