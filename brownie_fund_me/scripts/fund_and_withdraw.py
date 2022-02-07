from brownie import FundMe, network, accounts
from scripts.helpful_scripts import get_account
from web3 import Web3


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    tx = fund_me.fund({"from": account, "value": Web3.toWei(0.1, "ether")})
    tx.wait(1)


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    tx = fund_me.withdraw({"from": account})
    tx.wait(1)


def main():
    def print_balances():
        def balance(acc):
            return Web3.fromWei(acc.balance(), "ether")

        print(f"account:  {balance(get_account()):.4f}")
        print(f"contract: {balance(FundMe[-1]):.4f}")

    print_balances()
    fund()
    print_balances()
    withdraw()
    print_balances()
