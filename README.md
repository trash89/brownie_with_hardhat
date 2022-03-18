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

## Add a "Live" network in brownie, to connect to the hardhat network

In order to have the persistence accross contracts deployments:

```
brownie networks add Ethereum hardhat-local host=http://127.0.0.1:8545 chainid=31337
```

Create brownie-config.yaml and declare hardhat-local as a default network:

```bash
vi brownie-config.yaml
```

And declare it as follows:

```
networks:
default: hardhat-local
```

## Utilisation of console.log in solidity contracts with brownie

Inside the brownie project, in the contracts folder, copy the console.sol file from the hardhat installation folder and the sample Greeter.sol contract.

In contracts/Greeter.sol, insert the import console.sol statement:

```bash
vi contracts/Greeter.sol
```

```solidity
import "./console.sol";
```

Compile the Greeter contract:

```bash
brownie compile
```

```bash
Brownie v1.17.2 - Python development framework for Ethereum

Compiling contracts...
  Solc version: 0.8.12
  Optimizer: Enabled  Runs: 200
  EVM Version: Istanbul
Generating build data...
 - Greeter
 - console

Project has been compiled. Build artifacts saved at /brownie_with_hardhat/build/contracts
```

In the scripts folder, create the deployment script in brownie:

```bash
vi scripts/deploy.py
```

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
Brownie v1.17.2 - Python development framework for Ethereum

BrownieWithHardhatProject is the active project.

Running 'scripts/deploy.py::main'...
Transaction sent: 0x2228515667d0b69fae9fdb8cd0480fcffcad6d5ecc616b5eb0c7e5fbf92243d7
  Gas price: 1.0 gwei   Gas limit: 421741   Nonce: 0
  Greeter.constructor confirmed   Block: 1   Gas used: 383401 (90.91%)
  Greeter deployed at: 0x5FbDB2315678afecb367f032d93F642f64180aa3

Greeter deployed at 0x5FbDB2315678afecb367f032d93F642f64180aa3
```

See in the terminal where hardhat network has been launched:

```bash
  Contract deployment: <UnrecognizedContract>
  Contract address:    0x5fbdb2315678afecb367f032d93f642f64180aa3
  Transaction:         0x2228515667d0b69fae9fdb8cd0480fcffcad6d5ecc616b5eb0c7e5fbf92243d7
  From:                0xf39fd6e51aad88f6f4ce6ab8827279cfffb92266
  Value:               0 ETH
  Gas used:            383401 of 421741
  Block #1:            0x2c66d2dbcadb8d035ef314a78827e50fc604f5296bec1ec25ca5f77e0e4acd16

  console.log:
    Deploying a Greeter with greeting: Hello
```

Interact with the deployed contract from the brownie console:

```bash
brownie console
```

```Solidity
>>> Greeter[-1].setGreeting("Hello brownie",{"from":accounts[0]})
Transaction sent: 0x5c3948e35a45e15b704b419ca5b82a99393e1a8840466ce440067fb0551c4e59
  Gas price: 1.0 gwei   Gas limit: 38155   Nonce: 1
  Greeter.setGreeting confirmed   Block: 2   Gas used: 34419 (90.21%)

<Transaction '0x5c3948e35a45e15b704b419ca5b82a99393e1a8840466ce440067fb0551c4e59'>
```

See in the terminal where hardhat network has been launched:

```Solidity
eth_sendTransaction
  Contract call:       <UnrecognizedContract>
  Transaction:         0x5c3948e35a45e15b704b419ca5b82a99393e1a8840466ce440067fb0551c4e59
  From:                0xf39fd6e51aad88f6f4ce6ab8827279cfffb92266
  To:                  0x5fbdb2315678afecb367f032d93f642f64180aa3
  Value:               0 ETH
  Gas used:            34419 of 38155
  Block #2:            0x854fd459c2bc13f8ba8a05548b1ef628333297335c07becf67ae809e0d29ca01

  console.log:
    Changing greeting from 'Hello' to 'Hello brownie'
```

So now we can debug smart contracts by adding console.log() in the Solidity code and deploy,test and interact with contracts from brownie.
