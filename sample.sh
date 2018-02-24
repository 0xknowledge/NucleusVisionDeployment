
# directory in which the repos where cloned
CODEPATH=/home/prathab
CONTRACTCODE=$CODEPATH/NucleusVisionTokenSale/contracts
DEPLOYMENTCODE=$CODEPATH/NucleusVisionDeployment

###
### Deploying the contract
###
cd NucleusVisionTokenSale
# install node dependencies
npm install

# compile allocation/main token
solc zeppelin-solidity=$CODEPATH/NucleusVisionTokenSale/node_modules/zeppelin-solidity/ --optimize --bin $CONTRACTCODE/NucleusVisionAllocation.sol

# In the output copy the binary from contracts/NucleusVisionAllocation.sol
# Use https://www.myetherwallet.com/#contracts to deploy the contract

solc zeppelin-solidity=$CODEPATH/NucleusVisionTokenSale/node_modules/zeppelin-solidity/ --optimize --bin $CONTRACTCODE/NucleusVisionCoreToken.sol

# In the output copy the binary from contracts/NucleusVisionCoreToken.sol
# Use https://www.myetherwallet.com/#contracts to deploy the contract

# Create single contract files to get abi
# Core toke
python3 $CODEPATH/solidity-flattener/flattener/core.py --solc-paths=zeppelin-solidity=$CODEPATH/NucleusVisionTokenSale/node_modules/zeppelin-solidity/ $CONTRACTCODE/NucleusVisionAllocation.sol --output $DEPLOYMENTCODE/NucleusVisionAllocation.sol

python3 $CODEPATH/solidity-flattener/flattener/core.py --solc-paths=zeppelin-solidity=$CODEPATH/NucleusVisionTokenSale/node_modules/zeppelin-solidity/ $CONTRACTCODE/NucleusVisionCoreToken.sol --output $DEPLOYMENTCODE/NucleusVisionCoreToken.sol

python3 $CODEPATH/solidity-flattener/flattener/core.py --solc-paths=zeppelin-solidity=$CODEPATH/NucleusVisionTokenSale/node_modules/zeppelin-solidity/ $CONTRACTCODE/NucleusVisionToken.sol --output $DEPLOYMENTCODE/NucleusVisionToken.sol
