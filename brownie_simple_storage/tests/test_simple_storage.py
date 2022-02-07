from brownie import accounts, SimpleStorage

def test_deploy():
    account = accounts[0]
    simpleStorage = SimpleStorage.deploy({"from": account})
    starting_value = simpleStorage.retrieve()

    assert starting_value == 0

def test_store():
    account = accounts[0]
    value = 18
    simpleStorage = SimpleStorage.deploy({"from": account})
    tx = simpleStorage.store(value, {"from": account})

    assert simpleStorage.retrieve() == value