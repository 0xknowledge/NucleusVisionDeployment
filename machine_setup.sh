sudo apt-get update -y
sudo apt-get install -y build-essential
sudo apt-get install -y python3-dev
sudo apt-get install -y autoconf
sudo apt-get install -y virtualenv

virtualenv -p python3 ~/nd-venv3
source ~/nd-venv3/bin/activate

# latest version for web3
pip install web3==4.0.0b10
pip install py-solc

###
### Setting up the environment
###

# install solc
sudo add-apt-repository -y ppa:ethereum/ethereum
sudo apt-get update -y
sudo apt-get install -y solc

# clone the contract repo
git clone https://github.com/0xknowledge/NucleusVisionTokenSale.git
# clone solidity flattener
git clone https://github.com/BlockCatIO/solidity-flattener.git
