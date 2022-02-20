# Basic Sample Hardhat Project with brownie

This project demonstrates how to configure brownie and hardhat in order to use the console.log() option available in Hardhat Network in python scripts and console from brownie

Create a folder

```
mkdir brownie_with_hardhat
cd brownie_with_hardhat/
```

First, init brownie as it requests the folder to be empty

```
brownie init
```

```
Brownie v1.17.2 - Python development framework for Ethereum

SUCCESS: A new Brownie project has been initialized at /brownie_with_hardhat

```

Initialize npm

```
npm init -y
```

```
Wrote to /brownie_with_hardhat/package.json:

{
  "name": "brownie_with_hardhat",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "directories": {
    "test": "tests"
  },
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}
```

Install hardhat

```
npm install --save-dev hardhat
```

Create a basic project in hardhat:

```
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

Modify hardhat.config.js to setup the hardhat network

```
vi hardhat.config.js
```

```
module.exports = {
  defaultNetwork: "hardhat",
  networks: {
    hardhat: {
      initialBaseFeePerGas: 0,
    },
  },
  solidity: {
    version: "0.8.12",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
    },
  },
};
```

Add a "Live" network in brownie, to connect to the hardhat network

```
brownie networks add Ethereum hardhat-local host=http://127.0.0.1:8545 chainid=31337
```

```
Brownie v1.17.2 - Python development framework for Ethereum

SUCCESS: A new network 'hardhat-local' has been added
  └─hardhat-local
    ├─id: hardhat-local
    ├─chainid: 31337
    └─host: http://127.0.0.1:8545
```

Create brownie-config.yaml to declare hardhat-local as a default network

```
vi brownie-config.yaml
```

```
networks:
default: hardhat-local
development:
verify: True
```

Start the hardhat-local blockchain network:

```
npx hardhat node
```

```
Started HTTP and WebSocket JSON-RPC server at http://127.0.0.1:8545/

Accounts
========

WARNING: These accounts, and their private keys, are publicly known.
Any funds sent to them on Mainnet or any other live network WILL BE LOST.

Account #0: 0xf39fd6e51aad88f6f4ce6ab8827279cfffb92266 (10000 ETH)
...........
```

In contracts/Greeter.sol, modify the import console statement:

```
vi contracts/Greeter.sol
```

```
import "../node_modules/hardhat/console.sol";
```

Launch another terminal and brownie compile the Greeter contract

```
brownie compile
```

```
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

In the scripts folder, create the deployment script in brownie

```
vi scripts/deploy.py
```

```
from brownie import accounts, Greeter


def main():
    greeter = Greeter.deploy("Hello",{"from": accounts[0]})
    print(f"Greeter deployed at {greeter}")
```

Deploy with brownie

```
brownie run scripts/deploy.py
```

```
Brownie v1.17.2 - Python development framework for Ethereum

BrownieWithHardhatProject is the active project.

Running 'scripts/deploy.py::main'...
Transaction sent: 0x2228515667d0b69fae9fdb8cd0480fcffcad6d5ecc616b5eb0c7e5fbf92243d7
  Gas price: 1.0 gwei   Gas limit: 421741   Nonce: 0
  Greeter.constructor confirmed   Block: 1   Gas used: 383401 (90.91%)
  Greeter deployed at: 0x5FbDB2315678afecb367f032d93F642f64180aa3

Greeter deployed at 0x5FbDB2315678afecb367f032d93F642f64180aa3
```

See in the terminal where hardhat network were launched :

```
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

Interacting with the deployed contract from brownie console:

```
brownie console
```

```
>>> Greeter[-1].setGreeting("Hello brownie",{"from":accounts[0]})
Transaction sent: 0x5c3948e35a45e15b704b419ca5b82a99393e1a8840466ce440067fb0551c4e59
  Gas price: 1.0 gwei   Gas limit: 38155   Nonce: 1
  Greeter.setGreeting confirmed   Block: 2   Gas used: 34419 (90.21%)

<Transaction '0x5c3948e35a45e15b704b419ca5b82a99393e1a8840466ce440067fb0551c4e59'>
```

See in the terminal where hardhat network were launched :

```
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

So now we can debug smartcontracts by adding console.log() in the Solidity code and deploy,test scripts and interact with contracts from the brownie console.
