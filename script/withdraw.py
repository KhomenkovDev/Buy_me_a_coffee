import boa
from src import buy_me_a_coffee
from moccasin.config import get_active_network

def withdraw():
    active_network = get_active_network()
    coffee = active_network.manifest_named('buy_me_a_coffee')
    
    # Fund it first so there's something to withdraw
    coffee.fund(value=int(0.1 * 10**18))
    
    print(f'On network {active_network.name}, withdrawing from {coffee.address}')
    print(f'Balance before: {boa.env.get_balance(coffee.address)}')
    coffee.withdraw()
    print(f'Balance after:  {boa.env.get_balance(coffee.address)}')

def moccasin_main():
    return withdraw()


