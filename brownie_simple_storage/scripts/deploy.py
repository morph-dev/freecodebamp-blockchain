from brownie import accounts, config, network, SimpleStorage


def get_account():
    active_network = network.show_active()
    if active_network == "development":
        return accounts[0]
    if active_network in ["rinkeby", "kovan"]:
        return accounts.add(config["wallets"]["from_key"])
    # if active_network == "mainnet":
    #     return  accounts.load("testnet_metamask")
    raise ValueError("Unexpected active network: " + active_network)


def deploy_simple_storage():
    account = get_account()

    # deploy
    simple_storage = SimpleStorage.deploy({"from": account})

    print(simple_storage.retrieve())
    transaction = simple_storage.store(18, {"from": account})
    transaction.wait(1)
    print(simple_storage.retrieve())


def main():
    deploy_simple_storage()
