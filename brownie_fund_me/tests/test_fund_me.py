from web3 import Web3
from brownie import FundMe, MockV3Aggregator, accounts, exceptions
from scripts.helpful_scripts import get_account, maybe_deploy_mocks
from scripts.deploy import deploy_fund_me
import pytest


def test_can_fund_and_withdraw():
    maybe_deploy_mocks()
    account = get_account()
    fund_me = deploy_fund_me()
    fund_amount = Web3.toWei(0.1, "ether")
    tx = fund_me.fund({"from": account, "value": fund_amount})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account) == fund_amount

    tx = fund_me.withdraw({"from": account})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account) == 0


def test_only_owner_can_withdraw():
    maybe_deploy_mocks()
    fund_me = deploy_fund_me()
    other_account = accounts[1]
    with pytest.raises(AttributeError):
        fund_me.withdraw({"from": other_account})
