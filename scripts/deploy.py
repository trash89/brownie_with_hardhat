from brownie import accounts, Greeter


def main():
    greeter = Greeter.deploy("Hello", {"from": accounts[0]})
    print(f"Greeter deployed at {greeter}")
