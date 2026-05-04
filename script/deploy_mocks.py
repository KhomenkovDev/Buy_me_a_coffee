from src.mocks import mock_v3_aggregator
from eth_utils import to_wei
from moccasin.boa_tools import VyperContract 


STARTING_DECIMALS = 8
STARTING_PRICE = int(2000e8)


def deploy_feed() -> VyperContract:
    return mock_v3_aggregator.deploy(STARTING_DECIMALS, STARTING_PRICE)


def moccasin_main() -> VyperContract:
    contract = deploy_feed()
    print(f"DEBUG type: {type(contract)}, value: {contract}")
    return contract