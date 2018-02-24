from solc import compile_source
from web3 import Web3, HTTPProvider

import data
import constants
import time
import binascii

w3 = Web3(HTTPProvider(constants.INFURA_BACKEND))

# days to seconds
def days(val):
  return val * hours(24)

# hours to seconds
def hours(val):
  return val * 60 * 60

def get_abi(contract_name, filepath):
  contract_source_code = open(filepath).read()
  compiled_sol = compile_source(contract_source_code)
  contract_interface = compiled_sol['<stdin>:' + contract_name]
  return contract_interface['abi']

abi = get_abi('NucleusVisionAllocation', 'NucleusVisionAllocation.sol')
allocator = w3.eth.contract(constants.ALLOCATION_CONTRACT, abi=abi)


nonce = w3.eth.getTransactionCount(constants.PUBLIC_KEY)
txn = allocator.functions.unlockToken().buildTransaction({'from': constants.PUBLIC_KEY, 'nonce': nonce})
signed_txn = w3.eth.account.signTransaction(txn, private_key=constants.PRIVATE_KEY)
txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

print ('Sent Transaction {}.'.format(binascii.hexlify(txn_hash)))
while w3.eth.getTransactionReceipt(txn_hash) == None:
  time.sleep(10)
print ('Done Transaction {}.'.format(binascii.hexlify(txn_hash)))
print (w3.eth.getTransactionReceipt(txn_hash))
print ('\n\n\n')
