from typing import Tuple
import os
import unittest
from unittest.case import TestCase

from web3 import Web3
from eth_typing.evm import ChecksumAddress
from ..manage import deploy_ERC1155

from ..web3_util import (
    build_transaction,
    decode_transaction_input,
    get_nonce,
    submit_signed_raw_transaction,
    submit_transaction,
    wait_for_transaction_receipt,
)


def read_testnet_env_variables() -> Tuple[Web3, ChecksumAddress, str]:
    provider_path = os.environ.get("CENTIPEDE_TESTNET_PATH")
    if provider_path is None:
        raise ValueError("CENTIPEDE_TESTNET_PATH env variable is not set")
    raw_address = os.environ.get("CENTIPEDE_TEST_ETHEREUM_ADDRESS")
    if raw_address is None:
        raise ValueError("CENTIPEDE_TEST_ETHEREUM_ADDRESS env variable is not set")
    private_key = os.environ.get("CENTIPEDE_TEST_ETHEREUM_ADDRESS_PRIVATE_KEY")
    if raw_address is None:
        raise ValueError(
            "CENTIPEDE_TEST_ETHEREUM_ADDRESS_PRIVATE_KEY env variable is not set"
        )
    return (
        Web3(Web3.HTTPProvider(provider_path)),
        Web3.toChecksumAddress(raw_address),
        private_key,
    )


class CentipedeTestnetTestCase(TestCase):
    def setUp(self) -> None:
        self.basedir = os.path.dirname(os.path.dirname(__file__))
        try:
            (
                self.web3,
                self.test_address,
                self.test_address_pk,
            ) = read_testnet_env_variables()
        except Exception as e:
            raise unittest.SkipTest(f"Skipping test because of : {str(e)}")

    def _deploy_contract(self) -> ChecksumAddress:
        TOKEN_NAME = "CENTIPEDE-TEST"
        TOKEN_SYMBOL = "CNTPD"
        TOKEN_URI = "moonstream.to/centipede/"
        contract_address = deploy_ERC1155(
            self.web3,
            TOKEN_NAME,
            TOKEN_SYMBOL,
            TOKEN_URI,
            self.test_address,
            self.test_address,
            self.test_address_pk,
        )
        return contract_address

    def test_deployment(self) -> None:
        contract_address = self._deploy_contract()


if __name__ == "__main__":
    unittest.main()
