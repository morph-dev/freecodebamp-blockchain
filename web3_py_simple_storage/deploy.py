from itertools import chain
import json
from lib2to3.pgen2.literals import simple_escapes
from solcx import compile_standard, install_solc
from web3 import Web3

solc_version = "0.8.7"
install_solc(solc_version)


def read_file(path):
    with open(path, "r") as file:
        return file.read()


def write_file_json(path, data):
    with open(path, "w") as file:
        json.dump(data, file)


simple_storage_file = read_file("./SimpleStorage.sol")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "SimpleStorage.sol": {"content": simple_storage_file},
        },
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version=solc_version,
)

write_file_json("compiled_sol.json", compiled_sol)

compiled_contract = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]

abi = compiled_contract["abi"]
bytecode = compiled_contract["evm"]["bytecode"]["object"]

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
my_private_key = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

contract_tx = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": w3.eth.getTransactionCount(my_address),
        "gasPrice": w3.eth.gas_price,
    }
)

contract_tx_signed = w3.eth.account.sign_transaction(contract_tx, my_private_key)
contract_tx_hash = w3.eth.send_raw_transaction(contract_tx_signed.rawTransaction)
contract_tx_receipt = w3.eth.wait_for_transaction_receipt(contract_tx_hash)

simple_storage = w3.eth.contract(
    address=contract_tx_receipt["contractAddress"], abi=abi
)


print(simple_storage.functions.retrieve().call())
store_tx = simple_storage.functions.store(18).buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": w3.eth.getTransactionCount(my_address),
        "gasPrice": w3.eth.gas_price,
    }
)
store_tx_signed = w3.eth.account.sign_transaction(store_tx, my_private_key)
store_tx_hash = w3.eth.send_raw_transaction(store_tx_signed.rawTransaction)
store_tx_receipt = w3.eth.wait_for_transaction_receipt(store_tx_hash)

print(simple_storage.functions.retrieve().call())
