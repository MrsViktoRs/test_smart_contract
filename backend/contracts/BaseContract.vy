# @version ^0.4.0


@external
@view
def getGasPrice() -> uint256:
    return block.basefee


@external
@view
def getCaller() -> address:
    return msg.sender