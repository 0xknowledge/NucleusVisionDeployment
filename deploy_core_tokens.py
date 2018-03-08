# solc zeppelin-solidity=$CODEPATH/NucleusVisionTokenSale/node_modules/zeppelin-solidity/ --optimize --bin $CONTRACTCODE/NucleusVisionCoreToken.sol

# Address of the deployed NucleusVisionCoreToken contract
CORE_TOKEN_ADDRESS = "0x5230e3bEe0b09d64c1A4302DC3457CD4b690d2EE"
# File containing list of airdrop ethereum addresses
WHITELIST_AIRDROP_FILE = "whitelist.airdrop.txt"
# Gas price for each batch transaction
GAS_PRICE_IN_GWEI = 4
GAS_PRICE = GAS_PRICE_IN_GWEI * 1000000000;
# Batch size
BATCH_SIZE = 200

from solc import compile_source
from web3 import Web3, HTTPProvider

import data
import constants
import time
import binascii

raw_address_list = [i.strip() for i in open(WHITELIST_AIRDROP_FILE).read().split() if i.strip()]
address_list = []
total_invalid_addresses = 0
for _, i in enumerate(raw_address_list):
  if Web3.isAddress(i):
    if Web3.isChecksumAddress(i):
      address_list.append(i)
    else:
      address_list.append(Web3.toChecksumAddress(i))
  else:
    print ('Invalid Address {}'.format(i))
    total_invalid_addresses += 1

print ('Deploying Core Token For {} Addresses. Read {} Addresses and Found {} of them to be invalid'.format(len(address_list), len(raw_address_list), total_invalid_addresses))
batches = [address_list[i: i + BATCH_SIZE] for i in range(0, len(address_list), BATCH_SIZE)]
print ('At batch size of {} got {} batches. So {} transactions will be made'.format(BATCH_SIZE, len(batches), len(batches)))


w3 = Web3(HTTPProvider(constants.INFURA_BACKEND))

def get_abi(contract_name, filepath):
  contract_source_code = open(filepath).read()
  compiled_sol = compile_source(contract_source_code)
  contract_interface = compiled_sol['<stdin>:' + contract_name]
  return contract_interface['abi']

abi = get_abi('NucleusVisionCoreToken', 'NucleusVisionCoreToken.sol')
core_token = w3.eth.contract(CORE_TOKEN_ADDRESS, abi=abi)

for batch in batches:
  nonce = w3.eth.getTransactionCount(constants.PUBLIC_KEY)
  txn = core_token.functions.mintCoreToken(batch).buildTransaction({'from': constants.PUBLIC_KEY, 'nonce': nonce, 'gasPrice': GAS_PRICE})

  signed_txn = w3.eth.account.signTransaction(txn, private_key=constants.PRIVATE_KEY)
  txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

  print ('Sent Transaction {}.'.format(binascii.hexlify(txn_hash)))
  while w3.eth.getTransactionReceipt(txn_hash) == None:
    time.sleep(10)
  print ('Done Transaction {}.'.format(binascii.hexlify(txn_hash)))
  print (w3.eth.getTransactionReceipt(txn_hash))
  print ('\n\n\n')
