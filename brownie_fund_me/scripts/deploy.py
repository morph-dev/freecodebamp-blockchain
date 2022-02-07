from brownie import network, config, FundMe, MockV3Aggregator

from scripts.helpful_scripts import get_account, maybe_deploy_mocks
from web3 import Web3


def deploy_fund_me():
    account = get_account()
    print(account)

    active_network_config = config["networks"][network.show_active()]
    if active_network_config["deploy_mocks"]:
        price_feed_address = MockV3Aggregator[-1].address
    else:
        price_feed_address = active_network_config["eth_usd_price_feed"]

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=active_network_config["publish_source"],
    )
    print(f"Contract deployed to: {fund_me.address}")
    return fund_me


def main():
    maybe_deploy_mocks()
    deploy_fund_me()
