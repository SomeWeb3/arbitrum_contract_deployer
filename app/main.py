"""
Dev: https://t.me/python_web3
"""

import json
from pathlib import Path
from random import randint, uniform
from time import sleep

from eth_account.signers.local import LocalAccount
from hexbytes import HexBytes
from loguru import logger
from web3 import Account, Web3
from web3.contract import Contract
from web3.types import ABI

from app.config import AMOUNT_HIGH, AMOUNT_LOW, ARBITRUM_URL

logger.add(
    "log/debug.log",
    format="{time} | {level} | {message}",
    level="DEBUG",
)

w3 = Web3(Web3.HTTPProvider(ARBITRUM_URL))


def deploy_contract(wallet: LocalAccount, contract: type[Contract]) -> HexBytes:
    """Деплой контракта."""

    transaction = contract.constructor().buildTransaction(
        {
            "chainId": w3.eth.chain_id,
            "gasPrice": w3.eth.gas_price,
            "gas": 500_000,
            "from": wallet.address,
            "value": 0,
            "nonce": w3.eth.getTransactionCount(wallet.address)
        }
    )

    signed_txn = wallet.sign_transaction(transaction)

    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    logger.info(
        f"Deploy contract by {wallet.address}, transaction: {txn_hash.hex()}.")
    return txn_hash


def send_eth_to_contract(wallet: LocalAccount, to_address: str, amount: float) -> None:
    """Отправка указанного количества эфиров на контракт."""

    dict_transaction = {
        "chainId": w3.eth.chain_id,
        "from": wallet.address,
        "to": w3.toChecksumAddress(to_address),
        "value": w3.toWei(amount, "ether"),
        "gas": 300_000,
        "gasPrice": w3.eth.gas_price,
        "nonce": w3.eth.getTransactionCount(wallet.address),
    }

    signed_txn = wallet.sign_transaction(dict_transaction)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    logger.info(
        f"Send {amount} eth to {to_address}, transaction: {txn_hash.hex()}")


def return_eth_from_contract(
    wallet: LocalAccount, contract_address: str, abi: ABI
) -> None:
    """Возврат всего баланса из контракта на кошелёк-создатель."""

    dict_transaction = {
        "chainId": w3.eth.chain_id,
        "from": wallet.address,
        "value": 0,
        "gas": 500_000,
        "gasPrice": w3.eth.gas_price,
        "nonce": w3.eth.getTransactionCount(wallet.address),
    }

    contract = w3.eth.contract(
        address=w3.toChecksumAddress(contract_address), abi=abi)

    transaction = contract.functions.MoneyBack().buildTransaction(dict_transaction)
    signed_txn = wallet.sign_transaction(transaction)

    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    logger.info(
        f"Return balance from contract, transaction: {txn_hash.hex()}.")


def load_wallets() -> list[LocalAccount]:
    """Загрузка кошельков из текстовика."""

    file = Path("./wallets.txt").open()
    return [Account.from_key(line.replace("\n", "")) for line in file.readlines()]


def load_bytecode() -> str:
    """Загрузка байткода контракта для деплоя."""

    return Path("./contract/contract_byte_code.txt").open().readline()


def main() -> None:
    logger.info("Start.")

    wallets = load_wallets()
    logger.info("Load wallets.")

    bytecode = load_bytecode()
    logger.info("Load bytecode.")

    contract = w3.eth.contract(
        bytecode=bytecode,
        abi=json.load(Path("./contract/contract_abi.json").open())
    )

    for i, wallet in enumerate(wallets):
        txn_hash = deploy_contract(wallet, contract)
        sleep(randint(20, 40))

        contract_address = w3.eth.get_transaction_receipt(
            txn_hash).contractAddress

        send_eth_to_contract(
            wallet=wallet,
            to_address=contract_address,
            amount=uniform(AMOUNT_LOW, AMOUNT_HIGH),
        )

        sleep(randint(10, 20))

        return_eth_from_contract(wallet, contract_address, contract.abi)

        logger.success(f"{i+1}/{len(wallets)}")

    logger.success("Finish.")
