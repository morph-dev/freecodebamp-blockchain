from web3 import Web3
from brownie import accounts, config, network, MockV3Aggregator

DECIMALS = 8
STARTING_PRICE_USD = 3080 * 10**DECIMALS


def get_account():
    active_network = network.show_active()
    if active_network == "development":
        return accounts[0]
    if active_network == "ganache-local":
        return accounts[0]
    if active_network == "my-fork":
        return accounts[0]
    if active_network in ["rinkeby", "kovan"]:
        return accounts.add(config["wallets"]["from_key"])
    # if active_network == "mainnet":
    #     return  accounts.load("testnet_metamask")
    raise ValueError("Unexpected active network: " + active_network)


def maybe_deploy_mocks():
    active_network_config = config["networks"][network.show_active()]
    if active_network_config["deploy_mocks"]:
        if len(MockV3Aggregator) == 0:
            MockV3Aggregator.deploy(
                DECIMALS, STARTING_PRICE_USD, {"from": get_account()}
            )
