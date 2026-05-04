from eth_utils import to_wei
import boa 

SEND_VALUE = to_wei(1, 'ether')
RANDOM_USER = boa.env.generate_address('non-owner')

FAKE_USERS = [boa.env.generate_address() for _ in range(10)]
    

def test_price_feed_is_correct(coffee, eth_usd):
    assert coffee.PRICE_FEED() == eth_usd.address
    
def test_starting_values(coffee, account):
    assert coffee.MINIMUM_USD() == to_wei(5, 'ether')
    assert coffee.OWNER() == account.address
    
    
def test_fund_fails_without_enough_eth(coffee):
    with boa.reverts('You need to spend more ETH!'):
        coffee.fund()
        

def test_fund_with_money(coffee, account):
    # Arrange
    boa.env.set_balance(account.address, SEND_VALUE * 10)
    # Act
    coffee.fund(value=SEND_VALUE)
    # Asset
    funder = coffee.funders(0)
    assert funder == account.address
    assert coffee.address_to_amount_funded(funder) == SEND_VALUE
    
    
def test_non_owner_cannot_withdraw(coffee, account):
    boa.env.set_balance(account.address, SEND_VALUE)
    coffee.fund(value=SEND_VALUE)
    
    with boa.env.prank(RANDOM_USER):
        with boa.reverts('Not the contract owner'):
            coffee.withdraw()
            

def test_owner_can_withdraw(coffee):
    boa.env.set_balance(coffee.OWNER(), SEND_VALUE)
    with boa.env.prank(coffee.OWNER()):
        coffee.fund(value=SEND_VALUE)
        coffee.withdraw()
        assert boa.env.get_balance(coffee.address) == 0
        
    
    
    


def test_workshop_one(coffee):
    # Arrange: 10 different funders each fund the contract
    for user in FAKE_USERS:
        boa.env.set_balance(user, SEND_VALUE)
        with boa.env.prank(user):
            coffee.fund(value=SEND_VALUE)

    starting_owner_balance = boa.env.get_balance(coffee.OWNER())
    starting_contract_balance = boa.env.get_balance(coffee.address)

    # Act: owner withdraws
    with boa.env.prank(coffee.OWNER()):
        coffee.withdraw()

    # Assert
    assert boa.env.get_balance(coffee.address) == 0
    assert (
        boa.env.get_balance(coffee.OWNER())
        == starting_owner_balance + starting_contract_balance
    )


def test_get_rate(coffee):
    assert coffee.get_eth_to_usd_rate(SEND_VALUE) > 0
    
    
    
    
    
def test_get_version(coffee):
    # Act
    version = coffee.get_version()
    
    # Assert (MockV3Aggregator usually defaults to version 4)
    assert version == 4
    
def test_get_eth_to_usd_rate(coffee):
    # The mock price is usually $2000 (2000 * 10**8)
    # 1 ETH (10**18) should result in $2000 (10**18 precision)
    amount_to_convert = to_wei(1, "ether")
    expected_usd = 2000 * 10**18
    
    # Act
    actual_usd = coffee.get_eth_to_usd_rate(amount_to_convert)
    
    # Assert
    assert actual_usd == expected_usd

def test_get_funder(coffee_funded):
    # Arrange
    owner_address = coffee_funded.OWNER()
    
    # Act
    # Since coffee_funded pranks the OWNER to fund, index 0 is the owner
    funder_at_index_zero = coffee_funded.get_funder(0)
    
    # Assert
    assert funder_at_index_zero == owner_address
    
def test_get_owner(coffee, account):
    # Act / Assert
    assert coffee.get_owner() == account.address

def test_fund_updates_coordinates_and_price(coffee, account):
    # Arrange
    payment_amount = to_wei(1, "ether")
    
    # Act
    # Use account.address instead of the account object
    coffee.fund(value=payment_amount, sender=account.address)
    
    # Assert
    assert coffee.address_to_amount_funded(account.address) == payment_amount
    assert coffee.get_funder(0) == account.address


def test_coverage_for_price_feed_unpacking(coffee, account):
    # If ETH is $2000, $5 is 0.0025 ETH
    # We test exactly at the boundary to force the EVM to compute the unpacking
    min_eth_required = to_wei(0.0025, "ether") 
    
    # Act & Assert
    # 1. Test failure (just below $5)
    with boa.reverts("You need to spend more ETH!"):
        coffee.fund(value=min_eth_required - 1, sender=account.address)
    
    # 2. Test success (at or above $5)
    # This forces the contract to successfully unpack latestRoundData 
    # and finish the execution path.
    coffee.fund(value=min_eth_required, sender=account.address)
    
    assert coffee.address_to_amount_funded(account.address) == min_eth_required