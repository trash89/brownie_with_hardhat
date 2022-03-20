# Basic Sample Hardhat Project with brownie

This project demonstrates how to use brownie with the hardhat network in order to be able to include console.log() solidity contracts, for debugging.

## Installing hardhat

Create a folder:

```bash
mkdir brownie_with_hardhat
cd brownie_with_hardhat/
```

Install hardhat:

```bash
npm init -y
```

```bash
npm install --save-dev hardhat
```

Create a basic project in hardhat:

```bash
npx hardhat
```

```
Welcome to Hardhat v2.8.4

✔ What do you want to do? · Create a basic sample project
✔ Hardhat project root: · /brownie_with_hardhat

✔ Do you want to add a .gitignore? (Y/n) · y
✔ Do you want to install this sample project's dependencies with npm (@nomiclabs/hardhat-waffle ethereum-waffle chai @nomiclabs/hardhat-ethers ethers)? (Y/n) · y

Project created
See the README.md file for some example tasks you can run.
```

Modify hardhat.config.js to setup the hardhat network:

```bash
vi hardhat.config.js
```

```javascript
module.exports = {
  defaultNetwork: "hardhat",
  networks: {
    hardhat: {
      initialBaseFeePerGas: 0,
      accounts: {
        mnemonic: "test test test test test test test test test test test junk",
        path: "m/44'/60'/0'/0",
        count: 10,
        accountsBalance: "1000000000000000000000",
      },
    },
};
```

This configures the hardhat network to create 10 accounts with 1000 ETH each, using the default hardhat mnemonic, in order to have the same accounts generated at each execution.

Now, we can start the hardhat network in this folder:

```bash
npx hardhat node
```

## Connecting brownie to the hardhat network

Initialize a brownie project in a separate folder:

```bash
mkdir brownie_test
cd brownie_test
brownie init
```

By default, brownie tries to connect to http://127.0.0.1:8545 when the default network is development, so when running brownie commands without specifying a network, it will connect and use the hardhat network started previously.

```bash
brownie console
```

```python
Brownie v1.18.1 - Python development framework for Ethereum

Compiling contracts...
  Solc version: 0.8.13
  Optimizer: Enabled  Runs: 200
  EVM Version: Istanbul
Generating build data...
 - Greeter
 - console

BrownieWithHardhatProject is the active project.
Attached to local RPC client listening at '127.0.0.1:8545'...
Brownie environment is ready.
```

## Utilisation of console.log in solidity contracts with brownie

Inside the brownie project, in the contracts folder, copy the console.sol file from the hardhat installation folder and the sample Greeter.sol contract.

In contracts/Greeter.sol, insert the import console.sol statement:

```solidity
//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.0;

import "./console.sol";

contract Greeter {
    string private greeting;
    constructor(string memory _greeting) {
        console.log("Deploying a Greeter with greeting:", _greeting);
        greeting = _greeting;
    }
    function greet() public view returns (string memory) {
        return greeting;
    }
    function setGreeting(string memory _greeting) public {
        console.log("Changing greeting from '%s' to '%s'", greeting, _greeting);
        greeting = _greeting;
    }
}
```

Compile the Greeter contract:

```bash
brownie compile
```

```bash
Brownie v1.18.1 - Python development framework for Ethereum

Compiling contracts...
  Solc version: 0.8.13
  Optimizer: Enabled  Runs: 200
  EVM Version: Istanbul
Generating build data...
 - Greeter
 - console

Project has been compiled. Build artifacts saved at /brownie_with_hardhat/build/contracts
```

In the scripts folder, create the deployment script deploy.py:

```python
from brownie import accounts, Greeter

def main():
    greeter = Greeter.deploy("Hello",{"from": accounts[0]})
    print(f"Greeter deployed at {greeter}")
```

Deploy with brownie:

```bash
brownie run scripts/deploy.py
```

```bash
Brownie v1.18.1 - Python development framework for Ethereum

BrownieWithHardhatProject is the active project.
Attached to local RPC client listening at '127.0.0.1:8545'...

Running 'scripts/deploy.py::main'...
Transaction sent: 0x3b1a6a96166150370b0e53982449424fb4b286aa0d4d564223b5e4a37249509a
  Gas price: 0.0 gwei   Gas limit: 30000000   Nonce: 0
  Greeter.constructor confirmed   Block: 1   Gas used: 383178 (1.28%)
  Greeter deployed at: 0x5FbDB2315678afecb367f032d93F642f64180aa3

Greeter deployed at 0x5FbDB2315678afecb367f032d93F642f64180aa3
```

See in the terminal where hardhat network has been launched:

```bash
  Contract deployment: <UnrecognizedContract>
  Contract address:    0x5fbdb2315678afecb367f032d93f642f64180aa3
  Transaction:         0x3b1a6a96166150370b0e53982449424fb4b286aa0d4d564223b5e4a37249509a
  From:                0xf39fd6e51aad88f6f4ce6ab8827279cfffb92266
  Value:               0 ETH
  Gas used:            383178 of 30000000
  Block #1:            0x82b5f14636b9eff5a4efea6417523112e605ab6db4d0d02d19469b803d552ab9

  console.log:
    Deploying a Greeter with greeting: Hello
```

Interact with the deployed contract from the brownie console:

```bash
brownie console
```

```python
>>> greeter = Greeter.deploy("Hello", {"from": accounts[0]})
Transaction sent: 0x9fb8ca22636848bcbca4b0e84f10a991c227440082e56dac4db87cab305517a7
  Gas price: 0.0 gwei   Gas limit: 30000000   Nonce: 2
  Greeter.constructor confirmed   Block: 3   Gas used: 383178 (1.28%)
  Greeter deployed at: 0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0

>>> greeter.setGreeting("Hello brownie",{"from":accounts[0]})
Transaction sent: 0x418c5c98621a2cb97a7fc840d1e428adb5d7eb3fdd70222989ad46491b00cb15
  Gas price: 0.0 gwei   Gas limit: 30000000   Nonce: 3
  Greeter.setGreeting confirmed   Block: 4   Gas used: 34410 (0.11%)

<Transaction '0x418c5c98621a2cb97a7fc840d1e428adb5d7eb3fdd70222989ad46491b00cb15'>
```

See in the terminal where hardhat network has been launched:

```python
  Contract call:       <UnrecognizedContract>
  Transaction:         0x418c5c98621a2cb97a7fc840d1e428adb5d7eb3fdd70222989ad46491b00cb15
  From:                0xf39fd6e51aad88f6f4ce6ab8827279cfffb92266
  To:                  0x9fe46736679d2d9a65f0992f2272de9f3c7fa6e0
  Value:               0 ETH
  Gas used:            34410 of 30000000
  Block #4:            0x78087590fdd22bfd49e8b80c451b525312e3a8228d6bc90543a020d8433b9ad6

  console.log:
    Changing greeting from 'Hello' to 'Hello brownie'
```

So now we can debug smart contracts by adding console.log() in the Solidity code and deploy,test and interact with contracts from brownie.
