# Basic Sample Hardhat Project with brownie

This project demonstrates how to configure brownie and hardhat in order to use the console.log() option available in Hardhat Network in python scripts and console from brownie

Create a folder

```shell
mkdir brownie_with_hardhat
cd brownie_with_hardhat/
```

First, init brownie as it requests the folder to be empty

```shell
brownie init
Brownie v1.17.2 - Python development framework for Ethereum

SUCCESS: A new Brownie project has been initialized at /brownie_with_hardhat
```

Initialise git
git init

```shell
git init
Initialized empty Git repository in /brownie_with_hardhat/.git/
```

Initialize npm
npm init -y

```shell
npm init -y
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
npm install --save-dev hardhat

```shell
npm install --save-dev hardhat
npm WARN deprecated debug@3.2.6: Debug versions >=3.2.0 <3.2.7 || >=4 <4.3.1 have a low-severity ReDos regression when used in a Node.js environment. It is recommended you upgrade to 3.2.7 or 4.3.1. (https://github.com/visionmedia/debug/issues/797)

added 336 packages, and audited 337 packages in 32s

61 packages are looking for funding
  run `npm fund` for details

9 moderate severity vulnerabilities

To address all issues, run:
  npm audit fix

Run `npm audit` for details.
```

Create a basic project in hardhat:

```shell
npx hardhat
Welcome to Hardhat v2.8.4

✔ What do you want to do? · Create a basic sample project
✔ Hardhat project root: · /brownie_with_hardhat

✔ Do you want to add a .gitignore? (Y/n) · y
✔ Do you want to install this sample project's dependencies with npm (@nomiclabs/hardhat-waffle ethereum-waffle chai @nomiclabs/hardhat-ethers ethers)? (Y/n) · y



npm install --save-dev @nomiclabs/hardhat-waffle@^2.0.0 ethereum-waffle@^3.0.0 chai@^4.2.0 @nomiclabs/hardhat-ethers@^2.0.0 ethers@^5.0.0
npm WARN deprecated ganache-core@2.13.2: ganache-core is now ganache; visit https://trfl.io/g7 for details
npm WARN deprecated ganache-core@2.13.2: ganache-core is now ganache; visit https://trfl.io/g7 for details
npm WARN deprecated testrpc@0.0.1: testrpc has been renamed to ganache-cli, please use this package from now on.
npm WARN deprecated har-validator@5.1.5: this library is no longer supported
npm WARN deprecated querystring@0.2.0: The querystring API is considered Legacy. new code should use the URLSearchParams API instead.
npm WARN deprecated uuid@3.4.0: Please upgrade  to version 7 or higher.  Older versions may use Math.random() in certain circumstances, which is known to be problematic.  See https://v8.dev/blog/math-random for details.
npm WARN deprecated request@2.88.2: request has been deprecated, see https://github.com/request/request/issues/3142
npm WARN deprecated @ensdomains/ens@0.4.5: Please use @ensdomains/ens-contracts
npm WARN deprecated @ensdomains/resolver@0.2.4: Please use @ensdomains/ens-contracts

added 1098 packages, and audited 1438 packages in 44s

119 packages are looking for funding
  run `npm fund` for details

56 vulnerabilities (5 low, 20 moderate, 31 high)

To address issues that do not require attention, run:
  npm audit fix

Some issues need review, and may require choosing
a different dependency.

Run `npm audit` for details.

Project created
See the README.md file for some example tasks you can run.
```

Modify hardhat.config.js to setup the hardhat network
vi hardhat.config.js

```shell
module.exports = {
defaultNetwork: "hardhat",
networks: {
hardhat: {
initialBaseFeePerGas: 0
}
},
solidity: "0.8.4",
};
```

Add a "Live" network in brownie, to connect to the hardhat network

brownie networks add Ethereum hardhat-local host=http://127.0.0.1:8545 chainid=3133

```shell
brownie networks add Ethereum hardhat-local host=http://127.0.0.1:8545 chainid=31337
Brownie v1.17.2 - Python development framework for Ethereum

SUCCESS: A new network 'hardhat-local' has been added
  └─hardhat-local
    ├─id: hardhat-local
    ├─chainid: 31337
    └─host: http://127.0.0.1:8545
```

Create brownie-config.yaml to declare hardhat-local as a default network
vi brownie-config.yaml

```shell
vi brownie-config.yaml
networks:
default: hardhat-local
development:
verify: True
```

Start the hardhat-local blockchain network:
npx hardhat node

```shell
npx hardhat node
Started HTTP and WebSocket JSON-RPC server at http://127.0.0.1:8545/

Accounts
========

WARNING: These accounts, and their private keys, are publicly known.
Any funds sent to them on Mainnet or any other live network WILL BE LOST.

Account #0: 0xf39fd6e51aad88f6f4ce6ab8827279cfffb92266 (10000 ETH)
...........

```

In contracts/Greeter.sol, modify the import console statement:

```shell
import "../node_modules/hardhat/console.sol";
```

Launch another terminal and brownie compile the Greeter contract

```shell
brownie compile
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
vi deploy.py

```shell
vi deploy.py

from brownie import accounts, Greeter


def main():
    greeter = Greeter.deploy("Hello",{"from": accounts[0]})
    print(f"Greeter deployed at {greeter}")
```

Deploy with brownie
brownie run scripts/deploy.py

```shell
brownie run scripts/deploy.py
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

```shell
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
brownie console
Greeter[-1].setGreeting("Hello brownie",{"from":accounts[0]})

```shell
>>> Greeter[-1].setGreeting("Hello brownie",{"from":accounts[0]})
Transaction sent: 0x5c3948e35a45e15b704b419ca5b82a99393e1a8840466ce440067fb0551c4e59
  Gas price: 1.0 gwei   Gas limit: 38155   Nonce: 1
  Greeter.setGreeting confirmed   Block: 2   Gas used: 34419 (90.21%)

<Transaction '0x5c3948e35a45e15b704b419ca5b82a99393e1a8840466ce440067fb0551c4e59'>
```

See in the terminal where hardhat network were launched :

```shell
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
